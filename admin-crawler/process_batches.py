import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from copy import deepcopy

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def read_json(file_path):
    """
    JSON 파일을 읽어 내용을 반환합니다.

    Parameters:
    file_path (str): JSON 파일의 경로.

    Returns:
    list: JSON 파일의 내용.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def prepare_batch_requests(content_list, start_id, base_filename):
    """
    Batch 요청을 준비합니다.

    Parameters:
    content_list (list): 처리할 콘텐츠 리스트.
    start_id (int): custom_id의 시작 값.
    base_filename (str): 파일 경로의 기본 이름.

    Returns:
    str: 생성된 JSONL 파일 경로.
    """
    init_template = {
        "custom_id": None,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": '''
                    #지침
                    - 너는 {article}에 대한 내용을 정리하는 기계야. 
                    - 새로운 문장을 창작하는 것보다, 기존에 있는 내용을 옮기는게 중요해.
                    - 핵심 문단은 3개 이어야해!! 그리고 각각 400자가 넘어야 해!!
                    
                    #제약사항
                    - 핵심 문단은 문단 전체 내용을 구성해야해. 길면 길수록 좋아, 새로운 문장을 만들라는게 아니라 기존에 {article}에서 핵심 문단을 그대로 옮기라는 뜻이야.
                    - 핵심 문단이 만약 짧으면, 주변 문단을 이어붙어줘야해. 왜냐하면 해당 핵심 문단으로 문제를 생성할텐데 더욱 풍부한 문제를 만들기 위함이야.
                    - 핵심 문단은 400자가 넘어야해, 만약 넘지 않으면 400자가 넘을 때까지 주변 문단을 이어붙여야해. 핵심 문단들이 겹치는 문제는 상관없어.
                    - 핵심 문단은 3개 이어야해. 만약 3개가 넘는다면, 이어 붙여서 3개를 만들어주면 돼.   
                    - article에 관련된 category는 다음 중 하나로 정해져야해: politics, economy, society, culture, life, it, science, entertainments, sports, global, etc.
                    
                    #입력문
                    지침에 따라 {article}을 이해하고, 제약사항에 맞게 출력문을 작성해줘 제목은 {title}이야
                    
                    #출력문
                   {{\n    \"title\": \"제목\",\n    \"category\": \"카테고리\",\n    \"core\": [\n        \"핵심 문단 1\",\n        \"핵심 문단 2\",\n        \"핵심 문단 3\"\n    ],\n    \"description\": \"전체 내용 요약\"\n}}
                    '''
                }
            ]
        }
    }

    batches = []
    for id, content in enumerate(content_list, start=start_id):
        temp = deepcopy(init_template)
        temp['custom_id'] = f'{id}'
        temp['body']['messages'].append({"role": "user", "content": content})
        batches.append(temp)

    batch_file_path = f'batch/proceed_{base_filename}_batchinput_{start_id}.jsonl'
    with open(batch_file_path, 'w') as file:
        for item in batches:
            json_string = json.dumps(item)
            file.write(json_string + '\n')

    return batch_file_path

def create_batch(batch_file_path):
    """
    Batch 요청을 생성합니다.

    Parameters:
    batch_file_path (str): JSONL 파일 경로.

    Returns:
    str: 생성된 Batch ID.
    """
    batch_input_file = client.files.create(
        file=open(batch_file_path, "rb"),
        purpose="batch"
    )

    batch_input_file_id = batch_input_file.id

    batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": "nightly eval job"
        }
    )

    return batch.id

def get_batch_status(batch_id):
    """
    Batch 요청의 상태를 확인합니다.

    Parameters:
    batch_id (str): Batch ID.

    Returns:
    dict: Batch 상태 정보.
    """
    batch_status = client.batches.retrieve(batch_id)
    return batch_status

def get_batch_results(batch_id):
    """
    Batch 요청의 결과를 가져옵니다.

    Parameters:
    batch_id (str): Batch ID.

    Returns:
    list: Batch 결과 리스트.
    """
    batch_results = client.batches.retrieve(batch_id).result
    return batch_results

def process_batches(file_path, limit_per_batch=20):
    """
    파일 경로에 대한 콘텐츠를 처리하고 Batch 요청을 생성합니다.

    Parameters:
    file_path (str): JSON 파일 경로.
    limit_per_batch (int): 각 Batch 요청당 최대 콘텐츠 수.
    """
    data = read_json(file_path)

    content_list = []
    for idx, item in enumerate(data):
        title = item['content']['title']
        body = item['content']['body']
        content = f"지침에 따라 {body}을 이해하고, 제약사항에 맞게 출력문을 작성해줘 제목은 {title}이야"
        content_list.append(content)

    total_batches = (len(content_list) + limit_per_batch - 1) // limit_per_batch

    batch_ids = []
    base_filename = os.path.basename(file_path).split('.')[0]
    for batch_num in range(total_batches):
        start_index = batch_num * limit_per_batch
        end_index = start_index + limit_per_batch
        batch_contents = content_list[start_index:end_index]
        batch_file_path = prepare_batch_requests(batch_contents, start_id=start_index, base_filename=base_filename)
        batch_id = create_batch(batch_file_path)
        print(f"Batch {batch_num + 1}/{total_batches} ID: {batch_id}")
        batch_ids.append(batch_id)

    # Batch ID를 JSON 파일로 저장
    output_file = f'batch/proceed_{base_filename}_batch_ids.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(batch_ids, file, ensure_ascii=False, indent=4)

    print(f"Batch IDs가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    file_paths = [
        'pensionletter.json'
    ]
    for file_path in file_paths:
        process_batches(file_path)
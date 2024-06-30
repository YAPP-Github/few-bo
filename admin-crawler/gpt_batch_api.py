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


def prepare_batch_requests(content_list):
    """
    Batch 요청을 준비합니다.

    Parameters:
    content_list (list): 처리할 콘텐츠 리스트.

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
                    - 너는 article에 대한 내용으로 문제를 생성해주는 기계야.
                    - 너는 좀 더 좋은 문제를 생성해내려고 노력해야해. 내용을 잘 읽었으면 이해할 수 있을 법한 문제여야해.

                    #제약사항
                    - article의 문제는 단순 암기식이 아니라 창의적이고 article의 내용을 잘 이해했는제 확인해볼 수 있는 좋은 문제들로 구성되어야 해.
                    - 3개의 문제와 4개의 선지, 해설을 포함해야해.
                    - 해설은 지문에서의 핵심 근거인 문장이 들어있으면 좋겠어.
                    - article에 관련된 category는 다음 중 하나로 정해져야해: politics, economy, society, culture, life, it, science, entertainments, sports, global, etc.

                    #입력문
                    지침에 따라 {article}을 이해하고, 제약사항에 맞게 출력문을 작성해줘

                    #출력문
                    {{\n    \"category\": \"카테고리\",\n    \"questions\": [\n        {{\n            \"title\": \"질문1\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문2\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문3\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }}\n    ]\n}}
                    '''
                }
            ]
        }
    }

    batches = []
    for id, content in enumerate(content_list):
        temp = deepcopy(init_template)
        temp['custom_id'] = f'{id}'
        temp['body']['messages'].append({"role": "user", "content": content})
        batches.append(temp)

    batch_file_path = 'batchinput.jsonl'
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


def main(file_path, limit=None):
    # JSON 파일 경로
    file_path = file_path

    # JSON 파일 읽기
    data = read_json(file_path)

    # 각 콘텐츠에 대해 질문 생성
    content_list = []
    for idx, item in enumerate(data):
        if limit is not None and idx >= limit:
            break

        title = item['content']['title']
        body = item['content']['body']
        content = f"{title}\n\n{body}"
        content_list.append(content)

    # Batch 요청을 준비하고 생성
    batch_file_path = prepare_batch_requests(content_list)
    batch_id = create_batch(batch_file_path)
    print(f"Batch ID: {batch_id}")

    results = [batch_id]

    # 결과를 JSON 파일로 저장
    output_file = 'batch_ids.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print(f"질문이 생성되고 {output_file}에 저장되었습니다.")


if __name__ == "__main__":
    import time
    # limit 값을 설정하여 테스트할 아티클 수를 제한할 수 있습니다.
    file_paths = [
        'telescope.json',
        'gdmontly.json'
    ]
    for file_path in file_paths:
        main(file_path)
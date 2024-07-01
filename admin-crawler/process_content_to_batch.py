import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from copy import deepcopy

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def process_content_to_batch(file_path, limit_per_batch=20):
    """
    파일 경로에 대한 콘텐츠를 처리하고 Batch 요청을 생성합니다.

    Parameters:
    file_path (str): JSON 파일 경로.
    limit_per_batch (int): 각 Batch 요청당 최대 콘텐츠 수.
    """
    def read_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def prepare_batch_requests(content_list, start_id, base_filename):
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
                        - 너는 좀 더 좋은 문제를 생성해내려고 노력해야해. 내용을 잘 읽었으면 이해할 수 있을 법한 문제여야 해.

                        #제약사항
                        - article의 문제는 단순 암기식이 아니라 창의적이고 article의 내용을 잘 이해했는제 확인해볼 수 있는 좋은 문제들로 구성되어야 해.
                        - 3개의 문제와 4개의 선지, 해설을 포함해야해.
                        - 해설은 지문에서의 핵심 근거인 문장이 들어있으면 좋겠어.
                        - 요약은 전체 지문에 대한 요약이 들어가야 해.
                        - article에 관련된 category는 다음 중 하나로 정해져야해: politics, economy, society, culture, life, it, science, entertainments, sports, global, etc.

                        #입력문
                        지침에 따라 {article}을 이해하고, 제약사항에 맞게 출력문을 작성해줘. 제목은 {title}이야

                        #출력문
                        {{\n  \"title\": \"제목\",  \"category\": \"카테고리\", \"description\": \"요약\", \n    \"questions\": [\n        {{\n            \"title\": \"질문1\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문2\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문3\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }}\n    ]\n}}
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

        batch_file_path = f'batch/{base_filename}_batchinput.jsonl'
        with open(batch_file_path, 'w') as file:
            for item in batches:
                json_string = json.dumps(item)
                file.write(json_string + '\n')

        return batch_file_path

    def create_batch(batch_file_path):
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

    data = read_json(file_path)

    content_list = []
    for idx, item in enumerate(data):
        title = item['content']['title']
        body = item['content']['body']
        content = f"지침에 따라 {body}을 이해하고, 제약사항에 맞게 출력문을 작성해줘. 제목은 {title}이야"
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
    output_file = f'batch/{base_filename}_batch_ids.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(batch_ids, file, ensure_ascii=False, indent=4)

    print(f"Batch IDs가 {output_file}에 저장되었습니다.")

# 사용 예시
if __name__ == "__main__":
    process_content_to_batch('cleaned/pensionletter.json_cleaned.json')
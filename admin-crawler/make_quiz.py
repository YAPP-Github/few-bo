import json
import os
import re
import time
from dotenv import load_dotenv
from openai import OpenAI
from copy import deepcopy

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def remove_links_and_format(text):
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 이미지 링크 제거
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # 일반 링크 제거
    text = re.sub(r'http\S+', '', text)  # URL 제거
    text = re.sub(r'<.*?>', '', text)  # HTML 태그 제거
    text = re.sub(r'\n+', ' ', text)  # 여러 줄바꿈을 하나의 공백으로 대체
    return text.strip()  # 앞뒤 공백 제거

def prepare_batch_requests(content_list):
    init_template = {
        "custom_id": None,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": '''
                    #지침
                    - 너는 article에 대한 내용으로 문제를 생성해주는 기계야.
                    - article을 잘 읽었으면 이해할 수 있을 법한 문제여야 해. 
                    - artilce의 핵심 내용을 잘 읽었는지를 확인해볼 수 있는 수준 높고 흥미로운 문제들로 구성해야해. 날짜를 물어보거나, 단어 철자를 물어보는 문제는 내지 말아줘.

                    #제약사항
                    - 3개의 문제 질문(question_title)와 4개의 선지(question_content), 해설(question_explanation)을 포함해야해.
                    - question_explanation은 article에서의 핵심 근거인 문장이 들어있으면 좋겠어.
                    - 문제의 질문(question_title)은 자세하게 작성해줘. 
                    - 요약(description)은 전체 article에 대한 요약이 들어가야 해.
                    - 카테고리(category)는 대문자 영어여야해. 다음 중 하나로 정해져야해 : ECONOMY, IT, MARKETING, CULTURE, SCIENCE
                    - 출력문에만 맞게 작성해줘 ``` 이런 코드블록을 절대 사용하지마
                    - answer에는 오직 숫자만 들어가야해.

                    #입력문
                    지침에 따라 {article}을 이해하고, 제약사항에 맞게 출력문을 작성해줘. 제목은 {title} 이야

                    #출력문
                    {{\n  \"title\": \"제목\",  \"category\": \"카테고리\", \"description\": \"요약\", \n    \"questions\": [\n        {{\n            \"title\": \"질문1\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문2\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문3\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"number\",\n            \"explanation\": \"해설\"\n        }}\n    ]\n}}
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

    return batches

def create_and_submit_batches(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    content_list = []
    for article in data:
        title = article['content']['title']
        body = article['content']['body']
        cleaned_body = remove_links_and_format(body)
        article['content']['body'] = cleaned_body
        content = f"지침에 따라 {cleaned_body}을 이해하고, 제약사항에 맞게 출력문을 작성해줘. 제목은 {title}이야"
        content_list.append(content)

    print("Preparing batch requests...")
    batches = prepare_batch_requests(content_list)
    batch_ids = []

    for batch_num, batch in enumerate(batches):
        batch_file_path = f'batch_temp_{batch_num}.jsonl'
        with open(batch_file_path, 'w') as file:
            json_string = json.dumps(batch)
            file.write(json_string + '\n')

        batch_input_file = client.files.create(file=open(batch_file_path, "rb"), purpose="batch")
        batch_input_file_id = batch_input_file.id
        created_batch = client.batches.create(input_file_id=batch_input_file_id, endpoint="/v1/chat/completions",
                                              completion_window="24h", metadata={"description": "nightly eval job"})
        batch_ids.append(created_batch.id)
        os.remove(batch_file_path)  # 임시 파일 삭제
        print(f"Submitted batch {batch_num + 1}/{len(batches)} with ID: {created_batch.id}")

    return batch_ids, data

def retrieve_batch_results(batch_ids):
    result_list = []
    for batch_id in batch_ids:
        output_file_id = None
        print(f"Retrieving results for batch ID: {batch_id}")
        while output_file_id is None:
            batch_info = client.batches.retrieve(batch_id)
            if batch_info.status == "completed":
                output_file_id = batch_info.output_file_id
            else:
                print("Batch not completed yet. Waiting for 30 seconds...")
                time.sleep(30)  # 30초 대기 후 재시도

        result = client.files.content(output_file_id).content
        result_str = result.decode('utf-8')

        for line in result_str.strip().split('\n'):
            response_body = json.loads(line)
            if 'response' in response_body and 'body' in response_body['response']:
                message_content = response_body['response']['body']['choices'][0]['message']['content']
                try:
                    result_data = json.loads(message_content)
                    result_list.append(result_data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from message content: {message_content}")

    return result_list

def merge_data(original_data, batch_results):
    required_fields = ['title', 'category', 'description', 'questions']
    merged_data = []

    for item in original_data:
        title = item['content']['title']
        corresponding_batch_result = next((result for result in batch_results if result.get('title') == title), None)
        if corresponding_batch_result and all(field in corresponding_batch_result for field in required_fields):
            item['content'].update(corresponding_batch_result)
            merged_data.append(item)
        else:
            print(f"Skipping item with title '{title}' due to missing required fields")

    return merged_data

def main():
    base_filename = input("Enter the base filename (e.g., pensionletter): ")
    json_file_path = f'origin/{base_filename}.json'

    try:
        print("Creating and submitting batches...")
        batch_ids, original_data = create_and_submit_batches(json_file_path)
    except Exception as e:
        print(f"An error occurred while creating batch requests: {e}")
        return

    try:
        print("Retrieving batch results...")
        batch_results = retrieve_batch_results(batch_ids)
    except Exception as e:
        print(f"An error occurred while retrieving batch results: {e}")
        return

    try:
        print("Merging data...")
        merged_data = merge_data(original_data, batch_results)
        output_file_path = f'result/{base_filename}_result.json'
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(merged_data, file, ensure_ascii=False, indent=4)
        print(f"Merged JSON file has been saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while merging JSON files: {e}")

if __name__ == "__main__":
    main()
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
                    - 너는 뉴스레터 인스타그램 홍보 용 템플릿 봇이야
                    - 사람들에게 이목을 끌만한 컨텐츠를 제작해야해.
                    - 문제 퀄리티를 높이는데에 집중해야해. 단순 암기식이 아니라 내용이해 문제를 내줘야해
                    - 수준 높은 문제를 내줘
                    - \n(줄내림), **(볼드) 등을 제거하고 순수한 텍스트로 답변을 해야해 이모지는 허용

                    #제약사항
                    - {아티클 DATA}를 천천히 그리고 처음부터 끝까지 이해하고 다음의 제약사항을 지켜야해.
                    - article과 body에는 아티클에 있는 내용이 들어가야해. 생성과 요약을 하는게 아니야. 컨텐츠를 옮기는 작업이야.
                    - body에는 미리보기로 제공되어야 할 아티클의 본문 제목과 컨텐츠가 들어가야해.
                    - body_content는 글자 길이가 각각 500자 이상으로 구성해줘.
                    - questionData에는 아티클 전체가 아니라, 미리보기로 제공되어야 할 body의 내용에 관한 이해 관련 문제를 생성해줘.
                    - questionData는 외워서 풀거나, 단순히 숫자를 매칭시키는 문제가 아니라. 참신하고 흥미로운 내용이어야해.
                    - questionData에는 하나의 문제로 구성되어있고, title은 문제 제목이고, choices들은 문제에 대한 선지이고 answer은 문제에 대한 정답, explanation은 문제에 대한 설명이야. 선지와 답은 A. 이런식으로 대문자 영어 인덱스로 시작해야해
                    - questionData의 explanation은 body에 들어가 있는 내용이 포함되면 좋겠어.

                    #입력문
                    {아티클 DATA}

                    #출력문
                    - json 형식으로 정렬해서 출력해줘 코드 복사할 수 있도록 해줘 ```코드 블록을 사용해
                    {{
                        "article_title": "", 
                        "body_title1": "", 
                        "body_content1": "", 
                        "body_title2": "", 
                        "body_content2": "", 
                        "body_title3": "", 
                        "body_content3": "", 
                        "questionData": {{
                            "title": "", 
                            "choices": [
                                "", 
                                "", 
                                "", 
                                "", 
                            ],
                            "answer": "", 
                            "explanation": "" 
                        }}
                    }}
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

    if not os.path.exists('batch'):
        os.makedirs('batch')

    for batch_num, batch in enumerate(batches):
        batch_file_path = f'batch/batch_temp_{batch_num}.jsonl'
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

    return batch_ids

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
                    cleaned_message_content = message_content.replace('\n', '').replace('```json', '').replace('```', '').strip()
                    result_data = json.loads(cleaned_message_content)
                    result_list.append(result_data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from message content: {message_content}")

    return result_list

def main():
    base_filename = input("Enter the base filename (e.g., pensionletter): ")
    json_file_path = f'origin/{base_filename}.json'

    try:
        print("Creating and submitting batches...")
        batch_ids = create_and_submit_batches(json_file_path)
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
        print("Reading result file and creating insta_feed file...")
        insta_feed_data = []
        for item in batch_results:
            try:
                insta_feed_data.append(item)
            except json.JSONDecodeError:
                print(f"Skipping item due to JSON decode error: {item}")

        if not os.path.exists('insta_feed'):
            os.makedirs('insta_feed')

        insta_feed_file_path = f'insta_feed/{base_filename}_insta_feed.json'
        with open(insta_feed_file_path, 'w', encoding='utf-8') as file:
            json.dump(insta_feed_data, file, ensure_ascii=False, indent=4)
        print(f"Insta feed JSON file has been saved to {insta_feed_file_path}")
    except Exception as e:
        print(f"An error occurred while creating insta feed file: {e}")

if __name__ == "__main__":
    main()
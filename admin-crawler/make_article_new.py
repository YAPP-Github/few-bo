import json
import os
import time
from copy import deepcopy
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def prepare_batch_requests(content_list):
    """Prepare batch requests based on content list."""
    # The initial template structure is defined here but skipped with comments
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
                    - 너는 뉴스레터 봇이야.
                    

                    #제약사항
                    - 3개의 문제 질문(question_title)와 4개의 선지(question_content), 해설(question_explanation)을 포함해야해.
                    - 문제, 질문, 선지, 해설의 퀄리티는 이전보다 높았으면 좋겠어. 
                    - body를 이전과 수정해야하는데, 글의 원본 내용은 수정하지말고, 포맷이 이상한 부분만 수정해줘.
                    - body에는 줄내림이 너무 심하게 되어있거나, 제목 (#)태그가 붙어있지 않는 경우에 붙여줘. 

                    #입력문
                    지침에 따라 {article}을 이해하고, 제약사항에 맞게 출력문을 작성해줘.

                    #출력문
                    {{\n  \"title\": \"제목\", \"body\": \"기존 body에서 수정된 body\", \"category\": \"카테고리\", \"description\": \"요약\", \n    \"questions\": [\n        {{\n            \"title\": \"질문1\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문2\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문3\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"number\",\n            \"explanation\": \"해설\"\n        }}\n    ]\n}}
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


def create_and_submit_batches(json_data):
    """Create and submit batch requests."""
    content_list = []
    for article in json_data:
        # title = article['content']['title']
        # body = article['content']['body']
        content = f"지침에 따라 {article}을 이해하고, 제약사항에 맞게 출력문을 작성해줘."
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
        os.remove(batch_file_path)  # Remove temporary file
        print(f"Submitted batch {batch_num + 1}/{len(batches)} with ID: {created_batch.id}")

    return batch_ids


def retrieve_batch_results(batch_ids):
    """Retrieve results for the submitted batches."""
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
                time.sleep(30)  # Wait 30 seconds before retrying

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
    """Merge the original JSON data with the batch results."""
    required_fields = ['title', 'body', 'category', 'description', 'questions']
    merged_data = []

    for item in original_data:
        title = item['content']['title']
        corresponding_batch_result = next((result for result in batch_results if result.get('title') == title), None)
        print(corresponding_batch_result)
        if corresponding_batch_result and all(field in corresponding_batch_result for field in required_fields):
            item['content'].update(corresponding_batch_result)
            merged_data.append(item)
        else:
            print(f"Skipping item with title '{title}' due to missing required fields")

    return merged_data


def update_json_results(input_file_path, output_file_path):
    """Read the batch results JSON, merge with original data, and save as a new file."""
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    try:
        print("Creating and submitting batches...")
        batch_ids = create_and_submit_batches(json_data)
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
        merged_data = merge_data(json_data, batch_results)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(merged_data, file, ensure_ascii=False, indent=4)
        print(f"Merged JSON file has been saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while merging JSON files: {e}")


def main():
    input_file_path = input("Enter the path to the JSON result file (e.g., result/diggin_result.json): ")
    input_file_path = f"result/{input_file_path}_result.json"
    output_file_path = input_file_path.replace('.json', '_new.json')

    update_json_results(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
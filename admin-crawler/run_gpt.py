import json
import os
from dotenv import load_dotenv
from openai import OpenAI

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


def generate_questions_and_category(content):
    """
    GPT-4를 사용하여 객관식 질문 3개와 카테고리를 생성합니다.

    Parameters:
    content (str): 질문을 생성할 내용.

    Returns:
    dict: 생성된 질문과 카테고리.
    """
    messages = [
        {
            "role": "system",
            "content": '''
            #지침
            - 너는 article에 대한 내용으로 문제를 생성해주는 기계야.

            #제약사항
            - article의 문제는 단순 암기식이 아니라 창의적이고 article의 내용을 잘 이해했는제 확인해볼 수 있는 좋은 문제들로 구성되어야 해.
            - 3개의 문제와 4개의 선지, 해설을 포함해야해.
            - ans
            - article에 관련된 category는 다음 중 하나로 정해져야해: politics, economy, society, culture, life, it, science, entertainments, sports, global, etc.

            #입력문
            {article}을 이해하고, 제약사항에 맞게 출력문을 작성해줘

            #출력문
            {{\n    \"category\": \"카테고리\",\n    \"questions\": [\n        {{\n            \"title\": \"질문1\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문2\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }},\n        {{\n            \"title\": \"질문3\",\n            \"contents\": [\n                {{\"number\": 1, \"content\": \"선지1\"}},\n                {{\"number\": 2, \"content\": \"선지2\"}},\n                {{\"number\": 3, \"content\": \"선지3\"}},\n                {{\"number\": 4, \"content\": \"선지4\"}}\n            ],\n            \"answer\": \"선지 number\",\n            \"explanation\": \"해설\"\n        }}\n    ]\n}}
            '''
        },
        {"role": "user", "content": f"{content}을 이해하고, 제약사항에 맞게 출력문을 작성해줘"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    questions_and_category = response.choices[0].message.content
    # JSON 형식으로 변환
    try:
        questions_and_category = json.loads(questions_and_category)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return None

    return questions_and_category


def main(limit=None):
    # JSON 파일 경로
    file_path = 'telescope.json'

    # JSON 파일 읽기
    data = read_json(file_path)

    # 결과를 저장할 리스트 초기화
    results = []

    # 각 콘텐츠에 대해 질문 생성
    for idx, item in enumerate(data):
        if limit is not None and idx >= limit:
            break

        title = item['content']['title']
        body = item['content']['body']
        content = f"{title}\n\n{body}"

        generated_content = generate_questions_and_category(content)
        if not generated_content:
            continue

        category = generated_content['category']
        questions = generated_content['questions']

        problem_data = []
        for question in questions:
            problem_data.append({
                "title": question["title"],
                "contents": [
                    {"number": idx + 1, "content": choice["content"]}
                    for idx, choice in enumerate(question["contents"])
                ],
                "answer": question["answer"],
                "explanation": question["explanation"]
            })

        results.append({
            'link': item['link'],
            'title': title,
            'content': body,
            'category': category,
            'problemData': problem_data
        })

    # 결과를 JSON 파일로 저장
    output_file = 'generated_questions.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print(f"질문이 생성되고 {output_file}에 저장되었습니다.")


if __name__ == "__main__":
    # limit 값을 설정하여 테스트할 아티클 수를 제한할 수 있습니다.
    limit = 2  # 예: 3개의 아티클만 처리
    main(limit)
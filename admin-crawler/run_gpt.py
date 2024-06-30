import json
import openai

# OpenAI API 키 설정
openai.api_key = 'YOUR_OPENAI_API_KEY'

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
    GPT-3를 사용하여 객관식 질문 3개와 카테고리를 생성합니다.

    Parameters:
    content (str): 질문을 생성할 내용.

    Returns:
    dict: 생성된 질문과 카테고리.
    """
    prompt = f"""
    다음 내용에 기반하여 적절한 카테고리를 지정하고, 창의적인 객관식 문제 3개를 만들어줘. 각 문제는 선지 4개와 해설을 포함해야해. 카테고리는 다음 중 하나로 정해져야해: politics, economy, society, culture, life, it, science, entertainments, sports, global, etc.

    내용:
    {content}

    결과 형식:
    {{
        "category": "카테고리",
        "questions": [
            {{
                "title": "질문1",
                "contents": [
                    {{"number": 1, "content": "선지1"}},
                    {{"number": 2, "content": "선지2"}},
                    {{"number": 3, "content": "선지3"}},
                    {{"number": 4, "content": "선지4"}}
                ],
                "answer": "정답 선지",
                "explanation": "해설"
            }},
            {{
                "title": "질문2",
                "contents": [
                    {{"number": 1, "content": "선지1"}},
                    {{"number": 2, "content": "선지2"}},
                    {{"number": 3, "content": "선지3"}},
                    {{"number": 4, "content": "선지4"}}
                ],
                "answer": "정답 선지",
                "explanation": "해설"
            }},
            {{
                "title": "질문3",
                "contents": [
                    {{"number": 1, "content": "선지1"}},
                    {{"number": 2, "content": "선지2"}},
                    {{"number": 3, "content": "선지3"}},
                    {{"number": 4, "content": "선지4"}}
                ],
                "answer": "정답 선지",
                "explanation": "해설"
            }}
        ]
    }}
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    questions_and_category = response.choices[0].text.strip()
    return json.loads(questions_and_category)

def main():
    # JSON 파일 경로
    file_path = 'telescope.json'

    # JSON 파일 읽기
    data = read_json(file_path)

    # 결과를 저장할 리스트 초기화
    results = []

    # 각 콘텐츠에 대해 질문 생성
    for item in data:
        title = item['content']['title']
        body = item['content']['body']
        content = f"{title}\n\n{body}"

        generated_content = generate_questions_and_category(content)
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
    main()
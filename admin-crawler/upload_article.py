import json
import requests


def send_request(json_path, url, writer_email):
    with open(json_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)

    for data in data_list:
        # 입력 JSON에서 필요한 정보 추출
        article_image_url = data['thumbnailImageURL']
        title = data['content']['title']
        category = data['content']['category']
        content_type = "md"
        content_source = data['content']['body']  # body 내용 사용

        # 문제 데이터 생성
        problem_data = []
        for question in data['content']['questions']:
            problem = {
                "title": question['title'],
                "contents": question['contents'],
                "answer": question['answer'],
                "explanation": question['explanation']
            }
            problem_data.append(problem)

        # 요청에 대한 페이로드 생성
        payload = {
            "writerEmail": writer_email,
            "articleImageUrl": article_image_url,
            "title": title,
            "category": category,
            "contentType": content_type,
            "contentSource": content_source,
            "problemData": problem_data
        }
        # POST 요청 전송
        response = requests.post(url, json=payload)

        # 응답 출력
        if response.status_code == 200:
            print("요청이 성공적으로 전송되었습니다!")
        else:
            print(f"요청 전송 실패. 상태 코드: {response.status_code}")
            print(response.text)

# 사용 예제
json_path = "result/devpill_result.json"  # JSON 파일의 실제 경로로 교체
endpoint_url = "https://api.fewletter.site/api/v1/admin/articles"
writer_email = "dev.redpill@gmail.com"  # 실제 작성자 이메일로 교체
send_request(json_path, endpoint_url, writer_email)
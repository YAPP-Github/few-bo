import json
import requests


def send_request(title, main_image_url, category, description):
    payload = {
        "title": title,
        "mainImageUrl": main_image_url,
        "category": category,
        "description": description
    }
    response = requests.post("https://api.fewletter.site/api/v1/admin/workbooks", json=payload)
    if response.status_code == 200:
        print("요청이 성공적으로 전송되었습니다!")
    else:
        print(f"요청 전송 실패. 상태 코드: {response.status_code}")
        print(response.text)

send_request("봄코치의 코칭노트", "https://eehhqckznniu25210545.cdn.ntruss.com/images/2024-07-27/TO05tgL5oQ8MsSu7.png", "CULTURE", "여전히 낯설지만, 우리의 일과 삶에 꼭 필요한 코칭적 시선과 대화를 위하여.")
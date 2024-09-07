import json
import requests


def send_request(title, main_image_url, category, description):
    payload = {
        "title": title,
        "mainImageUrl": main_image_url,
        "category": category,
        "description": description
    }
    response = requests.post("https://api.fewletter.shop/api/v1/admin/workbooks", json=payload)
    if response.status_code == 200:
        print("요청이 성공적으로 전송되었습니다!")
    else:
        print(f"요청 전송 실패. 상태 코드: {response.status_code}")
        print(response.text)

send_request("도쿄워크앤라이프의 일본 배우기 - 로컬처럼", "https://d3ex4vlh373syu.cloudfront.net/images/2024-07-28/pi2HZxOQ4zInb3oX.webp", "CULTURE", "도쿄에 사는 외항사 마케터의 일본어와 도쿄 워크&라이프에 대한 이야기를 나눕니다.")
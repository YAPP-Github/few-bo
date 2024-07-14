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

send_request("Top 1% 개발자로 거듭나는 확실한 처방전", "https://eehhqckznniu25210545.cdn.ntruss.com/images/2024-07-11/UhS4u1BnAPVB2yeO.png", "IT", "해외 IT 업계 개발자 커리어 번역글을 제공합니다.")
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

send_request("자산 관리에 특화된 인모스트투자자문의 연금 노하우", "https://eehhqckznniu25210545.cdn.ntruss.com/images/2024-07-05/znOmoWr8JIjOudwW.png", "ECONOMY", "이 학습지는 IRP와 ISA 선택과 활용 방법, 퇴직소득세 절세 방안, 그리고 연금저축 세액공제 같은 유용한 세제 혜택에 대해 다뤄요. 또한, 최신 연금제도 변화뿐만 아니라 ETF를 포함한 다양한 연금투자 전략과 소득 공백기 동안의 연금자산 인출 계획에 대해서도 깊이 있게 설명해드립니다. 이를 통해 연금 및 투자 관리를 효율적으로 수행하고, 안전한 노후 준비를 계획하는 데 필요한 지식을 체계적으로 배우실 수 있을 거예요.")

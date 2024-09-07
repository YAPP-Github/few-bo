import requests


def send_post_requests(post_url, workbook_id, article_ids):
    for i, article_id in enumerate(article_ids):
        # 추가 요청 payload 생성
        post_payload = {
            "workbookId": workbook_id,
            "articleId": article_id,
            "dayCol": i + 1
        }

        # 추가 POST 요청 전송
        post_response = requests.post(post_url, json=post_payload)

        # 추가 응답 출력
        if post_response.status_code == 200:
            print("추가 요청이 성공적으로 전송되었습니다!")
        else:
            print(f"추가 요청 전송 실패. 상태 코드: {post_response.status_code}")
            print(post_response.text)

# 사용 예제
post_url = "https://api.fewletter.shop/api/v1/admin/relations/articles"  # 추가 요청을 위한 URL
workbook_id = 20 # 실제 workbookId로 교체
article_ids = list(range(290, 300))#   # 실제 articleId 리스트로 교체
article_ids.reverse()
send_post_requests(post_url, workbook_id, article_ids)
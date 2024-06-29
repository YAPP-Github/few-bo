import sys
import json

# 필요한 모듈을 임포트하기 위해 경로 추가
sys.path.append('/mnt/data')

# get_maily_posts와 get_maily_content 함수 임포트
from get_maily_posts import get_maily_posts
from get_maily_content import get_maily_content

# get_maily_posts 함수 호출하여 링크 목록 가져오기
links = get_maily_posts()

# links가 None인지 확인
if links is None:
    print("get_maily_posts 함수가 None을 반환했습니다.")
    sys.exit(1)

# 결과를 저장할 리스트 초기화
results = []

# 각 링크에 대해 get_maily_content 함수 호출하여 콘텐츠 가져오기
for link in links:
    content = get_maily_content(link)
    results.append({
        'link': link,
        'content': content
    })

# 결과를 JSON 파일로 저장
output_file = 'result/maily_contents1.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print(f"콘텐츠가 {output_file}에 저장되었습니다.")
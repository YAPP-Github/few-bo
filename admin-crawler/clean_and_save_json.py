import json
import re
import os

def remove_links_and_format(text):
    """
    주어진 텍스트에서 이미지 링크, 일반 링크, URL 및 HTML 태그를 제거하고,
    여러 줄바꿈을 하나의 공백으로 대체한 후 앞뒤 공백을 제거합니다.

    Parameters:
    text (str): 처리할 텍스트.

    Returns:
    str: 처리된 텍스트.
    """
    # 이미지 링크 제거
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 일반 링크 제거
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    # URL 제거
    text = re.sub(r'http\S+', '', text)
    # HTML 태그 제거
    text = re.sub(r'<.*?>', '', text)
    # 여러 줄바꿈을 하나의 공백으로 대체
    text = re.sub(r'\n+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    return text

def clean_and_save_json(json_file_path, output_dir='cleaned'):
    """
    JSON 파일의 내용을 정리하고 새로운 파일로 저장합니다.

    Parameters:
    json_file_path (str): 입력 JSON 파일 경로.
    output_dir (str): 출력 폴더 경로 (기본값: 'cleaned').
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for article in data:
        original_body = article['content']['body']
        cleaned_body = remove_links_and_format(original_body)
        article['content']['body'] = cleaned_body

    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_filename = os.path.basename(json_file_path).split('.')[0]
    output_file_path = os.path.join(output_dir, f'{base_filename}_cleaned.json')

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"정리된 JSON 파일이 {output_file_path}에 저장되었습니다.")

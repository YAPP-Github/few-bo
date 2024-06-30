# -*- coding: utf-8 -*-
import json
from get_notion_posts import get_notion_posts
from get_notion_content import get_notion_content, save_content_as_json


def run_notion_post_contents(url):
    # Get all the notion posts links from the provided URL
    links = get_notion_posts(url)
    print(f"Found {len(links)} links")

    # List to store all the contents
    all_contents = []

    for link in links:
        content = get_notion_content(link)
        if content:
            all_contents.append(content)
            print(f"Processed content from {link}")
        else:
            print(f"Failed to process content from {link}")

    # Define the output file path
    output_file_path = 'notion_contents.json'

    # Save all contents to a single JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(all_contents, file, ensure_ascii=False, indent=4)

    print(f"All content saved to {output_file_path}")


# Example usage
if __name__ == "__main__":
    target_url = 'https://www.fig1.kr/history'
    run_notion_post_contents(target_url)
import json
import os

def extract_content(prefix):
    batch_file_path = f'batch/{prefix}_batch_ids.json'
    output_file_path = f'output/{prefix}_output.json'

    with open(batch_file_path, 'r') as batch_file:
        batch_ids = json.load(batch_file)

    result_list = []
    for batch_id in batch_ids:
        input_file_path = f"batch/batch_results_{batch_id}.json"

        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            data = json.load(input_file)

        for item in data:
            content_str = item["response"]["body"]["choices"][0]["message"]["content"]
            try:
                content_dict = json.loads(content_str)
                item["content"] = content_dict
                result_list.append(content_dict)
            except json.JSONDecodeError as e:
                print(f"Error parsing content for item {item['id']}: {e}")
                item["content"] = content_str
                result_list.append({"error": str(e), "content": content_str})

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(result_list, output_file, ensure_ascii=False, indent=4)

    print(f"Extracted content has been saved to {output_file_path}")
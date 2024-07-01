import json
import os


def merge_json_files(pensionletter_path, pensionletter_output_path, output_dir='result'):
    # Load the JSON files
    with open(pensionletter_path, 'r', encoding='utf-8') as file:
        pensionletter_data = json.load(file)

    with open(pensionletter_output_path, 'r', encoding='utf-8') as file:
        pensionletter_output_data = json.load(file)

    # Create a dictionary from the output data for quick lookup
    output_dict = {item['title']: item for item in pensionletter_output_data}

    # Merge the data based on the title
    merged_data = []
    for item in pensionletter_data:
        title = item['content']['title']
        if title in output_dict:
            merged_item = item
            merged_item['content'].update(output_dict[title])
            merged_data.append(merged_item)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the output file path
    base_filename = os.path.basename(pensionletter_path).split('.')[0]
    output_file_path = os.path.join(output_dir, f'{base_filename}_result.json')

    # Save the merged data to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

    print(f"Merged JSON file has been saved to {output_file_path}")
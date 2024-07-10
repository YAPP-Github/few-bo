import json
import os

def merge_json_files(pensionletter_path, pensionletter_output_path, output_dir='result'):
    try:
        # Load the JSON files
        with open(pensionletter_path, 'r', encoding='utf-8') as file:
            pensionletter_data = json.load(file)
    except Exception as e:
        print(f"An error occurred while loading pensionletter JSON: {e}")
        return

    try:
        with open(pensionletter_output_path, 'r', encoding='utf-8') as file:
            pensionletter_output_data = json.load(file)
    except Exception as e:
        print(f"An error occurred while loading pensionletter output JSON: {e}")
        return

    # Create a dictionary from the output data for quick lookup
    output_dict = {}
    for item in pensionletter_output_data:
        try:
            title = item['title']
            output_dict[title] = item
        except KeyError:
            print(f"An item in pensionletter_output_data does not have a 'title' key and will be skipped: {item}")

    # Merge the data based on the title
    merged_data = []
    for item in pensionletter_data:
        try:
            title = item['content']['title']
            if title in output_dict:
                merged_item = item
                merged_item['content'].update(output_dict[title])
                merged_data.append(merged_item)
        except KeyError:
            print(f"An item in pensionletter_data does not have a 'title' key in 'content' and will be skipped: {item}")
        except Exception as e:
            print(f"An error occurred while merging item with title '{item['content'].get('title', 'Unknown')}': {e}")

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the output file path
    base_filename = os.path.basename(pensionletter_path).split('.')[0]
    output_file_path = os.path.join(output_dir, f'{base_filename}_result.json')

    # Save the merged data to the output file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(merged_data, file, ensure_ascii=False, indent=4)
        print(f"Merged JSON file has been saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the merged JSON file: {e}")
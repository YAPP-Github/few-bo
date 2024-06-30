# -*- coding: utf-8 -*-
import json
from markdownify import markdownify as md

def html_to_md(html_string):
    """
    Converts an HTML string to a Markdown string.

    Parameters:
    html_string (str): The HTML content to convert.

    Returns:
    str: The converted Markdown content.
    """
    return md(html_string)

def process_json_file(json_file_path, output_file_path):
    """
    Reads a JSON file, converts HTML content to Markdown, and saves each entry to a new JSON file with Markdown content.

    Parameters:
    json_file_path (str): The file path of the JSON file to process.
    output_file_path (str): The file path to save the processed JSON file.
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for entry in data:
        html_body = entry['content']['body']

        # Convert HTML to Markdown
        md_body = html_to_md(html_body)

        # Update the body content with Markdown
        entry['content']['body'] = md_body

    # Save the updated content to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Processed JSON file saved to {output_file_path}")

def process_json_files(json_file_paths):
    """
    Processes multiple JSON files, converting HTML content to Markdown for each and saving to new JSON files.

    Parameters:
    json_file_paths (list): A list of file paths of the JSON files to process.
    """
    for json_file_path in json_file_paths:
        output_file_path = json_file_path.replace(".json", "_processed.json")
        process_json_file(json_file_path, output_file_path)

# Example usage
json_file_paths = [
    "output.json",
]

process_json_files(json_file_paths)
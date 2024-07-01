import json
import os
from dotenv import load_dotenv
from openai import OpenAI

def retrieve_batch_results(batch_file_path):
    # Load environment variables
    load_dotenv()

    # Get OpenAI API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # Read batch ids from the provided file path
    with open(batch_file_path, 'r') as batch_file:
        batch_ids = json.load(batch_file)

    for batch_id in batch_ids:
        # Retrieve output file id from batch id
        output_file_id = client.batches.retrieve(batch_id).output_file_id

        # Retrieve the content of the output file
        result = client.files.content(output_file_id).content

        # Decode the content from bytes to string
        result_str = result.decode('utf-8')

        # Split the string by lines and parse each line as a JSON object
        result_list = []
        for line in result_str.strip().split('\n'):
            result_list.append(json.loads(line))

        # Define result file name based on batch id
        result_file_name = f"batch/batch_results_{batch_id}.json"

        # Write the result to a local JSON file
        with open(result_file_name, 'w', encoding='utf-8') as file:
            json.dump(result_list, file, ensure_ascii=False, indent=4)
import os
from dotenv import load_dotenv
from process_content_to_batch import process_content_to_batch
from clean_and_save_json import clean_and_save_json
from retrieve_batch_results import retrieve_batch_results
from merge_json_files import merge_json_files
from extract_content import extract_content

# Load environment variables
load_dotenv()

def main():
    while True:
        print("\nSelect an option:")
        print("1. Clean and save JSON")
        print("2. Process content to batch")
        print("3. Retrieve batch results")
        print("4. Merge JSON files")
        print("5. Extract content")
        print("6. Exit")

        choice = input("Enter your choice (1, 2, 3, 4, 5, or 6): ")

        if choice == '1':
            base_filename = input("Enter the base filename (e.g., pensionletter): ")
            json_file_path = f'origin/{base_filename}.json'
            try:
                clean_and_save_json(json_file_path)
            except Exception as e:
                print(f"An error occurred while cleaning and saving JSON: {e}")
        elif choice == '2':
            base_filename = input("Enter the base filename (e.g., pensionletter): ")
            json_file_path = f'cleaned/{base_filename}_cleaned.json'
            try:
                process_content_to_batch(json_file_path)
            except Exception as e:
                print(f"An error occurred while processing content to batch: {e}")
        elif choice == '3':
            base_filename = input("Enter the base filename (e.g., pensionletter): ")
            batch_file_path = f'batch/{base_filename}_batch_ids.json'
            try:
                retrieve_batch_results(batch_file_path)
            except Exception as e:
                print(f"An error occurred while retrieving batch results: {e}")
        elif choice == '4':
            base_filename = input("Enter the base filename (e.g., pensionletter): ")
            json_file_path = f'origin/{base_filename}.json'
            output_file_path = f'output/{base_filename}_cleaned_output.json'
            try:
                merge_json_files(json_file_path, output_file_path)
            except Exception as e:
                print(f"An error occurred while merging JSON files: {e}")
        elif choice == '5':
            base_filename = input("Enter the base filename (e.g., pensionletter): ")
            try:
                extract_content(base_filename+"_cleaned")
            except Exception as e:
                print(f"An error occurred while extracting content: {e}")
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

if __name__ == "__main__":
    main()
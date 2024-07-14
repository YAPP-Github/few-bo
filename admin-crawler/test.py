def md_file_to_string(md_file_path):
    """
    Converts a Markdown file to a string.

    Parameters:
    md_file_path (str): The path to the Markdown file.

    Returns:
    str: The content of the Markdown file as a string.
    """
    with open(md_file_path, 'r', encoding='utf-8') as file:
        md_string = file.read()
    return md_string

# Example usage
md_file_path = 'test.md'
md_string = md_file_to_string(md_file_path)
print(md_string)
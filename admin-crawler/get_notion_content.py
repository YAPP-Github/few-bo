# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

def get_notion_content(link):
    # Set the path to the ChromeDriver
    chrome_driver_path = '/Users/annapo/Develop/few-bo/admin-crawler/chromedriver'

    # Configure Chrome options
    options = Options()
    options.add_argument('headless')        # Run in headless mode
    options.add_argument('no-sandbox')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')     # Disable GPU acceleration
    options.add_argument('lang=ko_KR')      # Set language to Korean
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

    # Initialize the Chrome WebDriver with the Service and Options
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Open the website
    driver.get(link)
    driver.implicitly_wait(3)

    # Extract the title and body content
    title_xpath = '//*[@id="__next"]/div/div/div[1]/div/div/div[2]/div[1]/div/div[3]/h1'
    body_xpath = '//*[@id="__next"]/div/div/div[1]/div/div/div[2]/div[3]'

    try:
        title_element = driver.find_element(By.XPATH, title_xpath)
        body_element = driver.find_element(By.XPATH, body_xpath)

        title_text = title_element.text
        body_html = body_element.get_attribute('innerHTML')

        # Create a dictionary to store the data
        data = {
            'title': title_text,
            'body': body_html
        }

        print("Content extracted successfully")
        return data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

    finally:
        # Close the driver
        driver.quit()

def save_content_as_json(content, output_file_path):
    """
    Saves the content to a JSON file.

    Parameters:
    content (dict): The content to save.
    output_file_path (str): The file path to save the JSON file.
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)
    print(f"Content saved to {output_file_path}")

# Example usage
link = 'https://www.fig1.kr/a2e9a158-26bb-4cb3-8f40-351c1cf11f03'
content = get_notion_content(link)
if content:
    save_content_as_json(content, 'output.json')
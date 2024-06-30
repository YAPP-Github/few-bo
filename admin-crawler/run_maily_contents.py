import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from markdownify import markdownify as md

CHROME_DRIVER_PATH = '/Users/annapo/Develop/few-bo/admin-crawler/chromedriver'


def configure_driver():
    options = Options()
    options.add_argument('headless')  # Run in headless mode
    options.add_argument('no-sandbox')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')  # Disable GPU acceleration
    options.add_argument('lang=ko_KR')  # Set language to Korean
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def html_to_md(html_string):
    """
    Converts an HTML string to a Markdown string.

    Parameters:
    html_string (str): The HTML content to convert.

    Returns:
    str: The converted Markdown content.
    """
    return md(html_string)


def get_maily_posts(url):
    driver = configure_driver()

    # Open the website
    driver.get(url)
    driver.implicitly_wait(3)

    # List to store links and thumbnails
    posts = []

    # Scroll and collect links and thumbnails until no more new links are found
    previous_length = -1
    while previous_length < len(posts):
        previous_length = len(posts)

        # Find all elements matching the link pattern
        link_elements = driver.find_elements(By.XPATH, '//*[@id="preRenderedPosts"]/div/a')
        # Find all elements matching the thumbnail pattern
        thumbnail_elements = driver.find_elements(By.XPATH, '//*[@id="preRenderedPosts"]/div/a/div[2]/div')

        for link_element, thumbnail_element in zip(link_elements, thumbnail_elements):
            href = link_element.get_attribute('href')
            thumbnail_url = thumbnail_element.value_of_css_property('background-image')
            thumbnail_url = thumbnail_url.split('"')[1] if 'url("' in thumbnail_url else None

            if href not in [post['link'] for post in posts]:
                posts.append({'link': href, 'thumbnailImageURL': thumbnail_url})

        # Scroll to the bottom to load more content
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)  # Wait for new content to load

    # Close the driver
    driver.quit()

    # Return the collected posts
    return posts


def get_maily_content(link):
    driver = configure_driver()

    # Open the website
    driver.get(link)
    driver.implicitly_wait(3)

    # Extract the title and body content
    title_xpath = '//*[@id="appContainer"]/div/div/div[2]/div[1]/h1'
    body_xpath = '//*[@id="appContainer"]/div/div/div[2]/div[3]/article'

    try:
        title_element = driver.find_element(By.XPATH, title_xpath)
        body_element = driver.find_element(By.XPATH, body_xpath)

        title_text = title_element.text
        body_html = body_element.get_attribute('innerHTML')

        # Convert HTML to Markdown
        body_md = html_to_md(body_html)

        # Create a dictionary to store the data
        data = {
            'title': title_text,
            'body': body_md
        }

        print("Content extracted and converted to Markdown successfully")
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


def main(url):
    # Get the list of posts
    links = get_maily_posts(url)

    if links is None:
        print("get_maily_posts 함수가 None을 반환했습니다.")
        return
    elif not links:
        print("get_maily_posts 함수가 빈 링크 목록을 반환했습니다.")
        return
    else:
        print(f"get_maily_posts 함수가 {len(links)}개의 링크를 반환했습니다.")

    # Store results
    results = []

    # Get content for each link
    for link in links:
        content = get_maily_content(link['link'])
        if content:
            results.append({
                'link': link['link'],
                'thumbnailImageURL': link['thumbnailImageURL'],
                'content': content
            })

    # Save results to a JSON file
    # Generate output filename based on URL
    output_filename = url.split('/')[-1] + '.json'
    output_file = f"{output_filename}"
    save_content_as_json(results, output_file)


if __name__ == "__main__":
    # URL list
    urls = [
        'https://maily.so/telescope',
        'https://maily.so/gdmontly',
        'https://maily.so/diggin',
        'https://maily.so/meowpunch',
        'https://maily.so/pensionletter'
    ]

    # Call main function for each URL
    for url in urls:
        main(url)
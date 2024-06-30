from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_notion_posts(url):
    # Set the path to the ChromeDriver
    chrome_driver_path = '/Users/annapo/Develop/few-bo/admin-crawler/chromedriver'

    # Configure Chrome options
    options = Options()
    options.add_argument('headless')  # Run in headless mode
    options.add_argument('no-sandbox')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')  # Disable GPU acceleration
    options.add_argument('lang=ko_KR')  # Set language to Korean
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

    # Initialize the Chrome WebDriver with the Service and Options
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Open the website
    driver.get(url)
    driver.implicitly_wait(3)

    # List to store links
    links = []

    # Scroll and collect links until no more new links are found
    previous_length = -1
    while previous_length < len(links):
        previous_length = len(links)

        # Find all <a> elements matching the pattern
        elements = driver.find_elements(By.XPATH, '//*[@id="__next"]//a')

        for element in elements:
            href = element.get_attribute('href')
            if href and href not in links:
                links.append(href)

        # Scroll to the bottom to load more content
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)  # Wait for new content to load

    # Close the driver
    driver.quit()

    # Return the collected links
    return links

# Example usage
url = 'https://www.fig1.kr/history'
notion_links = get_notion_posts(url)
for link in notion_links:
    print(link)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import clickhouse_connect
import re
import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ClickHouse connection details
CLICK_HOUSE_HOST = "l1klbatlht.ap-south-1.aws.clickhouse.cloud"
CLICK_HOUSE_PORT = "8443"
CLICK_HOUSE_USER = "default"
CLICK_HOUSE_PASSWORD = "BBwfYXH.OyBY2"
CLICK_HOUSE_DATABASE = "Dealwallet"
CLICK_HOUSE_TABLE = "Product"

# Establishing a connection to ClickHouse
try:
    client = clickhouse_connect.get_client(
        host=CLICK_HOUSE_HOST,
        port=CLICK_HOUSE_PORT,
        username=CLICK_HOUSE_USER,
        password=CLICK_HOUSE_PASSWORD,
        database=CLICK_HOUSE_DATABASE,
    )
    print("Connected to ClickHouse.")
except Exception as e:
    print(f"Failed to connect to ClickHouse: {e}")
    exit(1)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://www.ebay.com/b/Apple/bn_21819543'
driver.get(url)

# Allow time for the page to load
time.sleep(15)

data_to_insert = []

while True:
    # Get page source and parse it
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.find_all('li', class_='s-item s-item--large')

    for item in items:
        id = str(uuid.uuid4())
        name = item.find('h3', class_='s-item__title').get_text(strip=True) if item.find('h3', class_='s-item__title') else 'N/A'
        price = item.find('span', class_='s-item__price').get_text(strip=True) if item.find('span', class_='s-item__price') else 'N/A'
        image = item.find('img', class_="s-item__image-img")['src'] if item.find('img', class_="s-item__image-img") else 'N/A'
        shipping_cost = item.find('span', class_='s-item__logisticsCost').text.strip() if item.find('span', class_='s-item__logisticsCost') else 'N/A'
        sold_count = item.find('span', class_='s-item__itemHotness').text.strip() if item.find('span', class_='s-item__itemHotness') else 'N/A'
        Description = item.find('span', class_='s-item__certified-refurbished').text.strip() if item.find('span', class_='s-item__certified-refurbished') else 'N/A'
        product_link = item.find('a', class_='s-item__link')['href'] if item.find('a', class_='s-item__link') else 'N/A'

        data_to_insert.append((id, name, price, image, shipping_cost, sold_count, Description, product_link))

    # Try to find the 'Next' button and click it
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagination__next'))
        )
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
    except Exception as e:
        print("No more pages to scrape or error occurred.")
        break
print(data_to_insert)
if data_to_insert: 
    try:
        client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=["id","name","price","image", "original_price","discount","Description","product_link"])
        print("Data insertion completed.")
    except Exception as e:
        print(f"An error occurred during data insertion: {e}")
else:
    print("No data to insert.")

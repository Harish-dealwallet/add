from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import clickhouse_connect
import uuid

# # ClickHouse configuration
# CLICK_HOUSE_HOST = "l1klbatlht.ap-south-1.aws.clickhouse.cloud"
# CLICK_HOUSE_PORT = "8443"
# CLICK_HOUSE_USER = "default"
# CLICK_HOUSE_PASSWORD = "BBwfYXH.OyBY2"
# CLICK_HOUSE_DATABASE = "Dealwallet"
# CLICK_HOUSE_TABLE = "Amazon"

# Connect to ClickHouse
# try:
#     client = clickhouse_connect.get_client(
#         host=CLICK_HOUSE_HOST,
#         port=CLICK_HOUSE_PORT,
#         username=CLICK_HOUSE_USER,
#         password=CLICK_HOUSE_PASSWORD,
#         database=CLICK_HOUSE_DATABASE,
#     )
#     print("Connected to ClickHouse.")
# except Exception as e:
#     print(f"Failed to connect to ClickHouse: {e}")
#     exit(1)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url = 'https://www.amazon.in/gcx/Gifts-for-Everyone/gfhz/?ref_=nav_cs_giftfinder&scrollState=eyJpdGVtSW5kZXgiOjAsInNjcm9sbE9mZnNldCI6MTMwLjU2MjV9&sectionManagerState=eyJzZWN0aW9uVHlwZUVuZEluZGV4Ijp7ImFtYWJvdCI6MH19'
driver.get(url)

# Use WebDriverWait for better element handling
time.sleep(20)  # Consider replacing this with WebDriverWait

soup = BeautifulSoup(driver.page_source, 'html.parser')

products = soup.find_all('div', class_='puis-card-container')
data_to_insert = []

for product in products:
    id = str(uuid.uuid4())
    title = product.find('span', class_='a-size-base-plus')
    title_text = title.get_text(strip=True) if title else 'N/A'
    
    link = product.find('a', class_='a-link-normal')
    product_link = link['href'] if link else 'N/A'
    
    img_tag = product.find('img', class_='s-image')
    img_url = img_tag['src'] if img_tag else 'N/A'
    
    rating = product.find('span', class_='a-icon-alt')
    rating_text = rating.get_text(strip=True) if rating else 'N/A'
    
    num_ratings = product.find('span', class_='a-size-base')
    num_ratings_text = num_ratings.get_text(strip=True) if num_ratings else 'N/A'
    
    price = product.find('span', class_='a-offscreen')
    price_text = price.get_text(strip=True) if price else 'N/A'
    
    original_price = product.find('span', class_='a-text-price')
    original_price_text = original_price.get_text(strip=True) if original_price else 'N/A'

    data_to_insert.append((id, title_text, product_link, img_url, rating_text, num_ratings_text, price_text, original_price_text))
    print(data_to_insert)
    print('-' * 40)

# if data_to_insert:
#     try:
#         client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=["id", "title", "link", "image_url", "rating", "number_of_ratings", "price", "original_price"])
#         print("Data insertion completed.")
#     except Exception as e:
#         print(f"An error occurred during data insertion: {e}")
# else:
#     print("No data to insert.")

driver.quit()

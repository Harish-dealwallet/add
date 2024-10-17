from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import clickhouse_connect
import uuid

# ClickHouse configuration
CLICK_HOUSE_HOST = "l1klbatlht.ap-south-1.aws.clickhouse.cloud"
CLICK_HOUSE_PORT = "8443"
CLICK_HOUSE_USER = "default"
CLICK_HOUSE_PASSWORD = "BBwfYXH.OyBY2"
CLICK_HOUSE_DATABASE = "Dealwallet"
CLICK_HOUSE_TABLE = "Amazon"

# Connect to ClickHouse
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

# Function to scrape Amazon page using Selenium
def scrape_amazon():
    url = 'https://www.amazon.in/events/greatindianfestival?ref_=nav_cs_gb&discounts-widget=%2522%257B%255C%2522state%255C%2522%253A%257B%255C%2522refinementFilters%255C%2522%253A%257B%257D%257D%252C%255C%2522version%255C%2522%253A1%257D%2522'

    # Set up Selenium options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Navigate to the page
    driver.get(url)
    time.sleep(15)  # Wait for the page to load completely

    # Find product cards
    product_cards = driver.find_elements(By.CLASS_NAME, 'ProductCard-module__card_uyr_Jh7WpSkPx4iEpn4w')

    data_to_insert = []

    for product_card in product_cards:
        # Extract title
        title_element = product_card.find_element(By.CLASS_NAME, 'a-truncate-cut')
        name= title_element.text if title_element else 'N/A'

        # Extract price
        try:
            price_element = product_card.find_element(By.CLASS_NAME, 'a-size-mini')
            price = price_element.text
        except:
            price = 'N/A'

        # Extract original price
        try:
            original_price_element = product_card.find_element(By.CLASS_NAME, 'ProductCard-module__originalPrice')
            original_price = original_price_element.text
        except:
            original_price = 'N/A'

        # Extract link
        link_element = product_card.find_element(By.CLASS_NAME, 'a-link-normal')
        link = link_element.get_attribute('href') if link_element else 'N/A'

        # Extract image
        image_element = product_card.find_element(By.TAG_NAME, 'img')
        image = image_element.get_attribute('src') if image_element else 'N/A'

        # Generate UUID for each product
        id = str(uuid.uuid4())

        # Append data to list
        data_to_insert.append((id, name, price, original_price, link, image))

        # Print the extracted details
        print("Title:", name)
        print("Price:", price)
        print("Original Price:", original_price)
        print("Link:", link)
        print("Image:", image)
        print("---")

    # Close the WebDriver
    driver.quit()

    # Insert data into ClickHouse
    if data_to_insert:
        try:
            client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=["id", "name", "price", "original_price", "link", "image"])
            print("Data insertion completed.")
        except Exception as e:
            print(f"An error occurred during data insertion: {e}")
    else:
        print("No data to insert.")

# Main function to run the scraping
if __name__ == "__main__":
    scrape_amazon()

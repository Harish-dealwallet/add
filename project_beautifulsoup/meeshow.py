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


CLICK_HOUSE_HOST = "l1klbatlht.ap-south-1.aws.clickhouse.cloud"
CLICK_HOUSE_PORT = "8443"
CLICK_HOUSE_USER = "default"
CLICK_HOUSE_PASSWORD = "BBwfYXH.OyBY2"
CLICK_HOUSE_DATABASE = "Dealwallet"
CLICK_HOUSE_TABLE = "Product"

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

url = 'https://www.meesho.com/baby-care/pl/3tj'
driver.get(url)

wait = WebDriverWait(driver, 160)

data_to_insert = []

# Set a variable to track the previous height of the page
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-dkrFOg.ProductList__GridCol-sc-8lnc8o-0.cokuZA.eCJiSA")))
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', class_='sc-dkrFOg ProductList__GridCol-sc-8lnc8o-0 cokuZA eCJiSA')

    for product in products:
        id = str(uuid.uuid4())
        image = product.find('img')['src'] if product.find('img') else 'No image'
        product_link = product.find("a")["href"]
        name = product.find('p', class_='NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5').text.strip() if product.find('p', class_='NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5') else 'No name'
        price = product.find('h5', class_='dwCrSh').text.strip() if product.find('h5', class_='dwCrSh') else 'No price'
        Description = product.find('span', class_='fkvMlU').text if product.find('span', class_='fkvMlU') else 'No delivery info'
        ratings = product.find('span', class_='laVOtN').text if product.find('span', class_='laVOtN') else 'No rating'
        
        data_to_insert.append((id, image, name, price, Description, ratings, product_link))

    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(15)  # Wait for new products to load

    # Check if new products have loaded by comparing the height of the page
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print("No more products to load.")
        break
    last_height = new_height

if data_to_insert:
    try:
        client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=["id", "image", "name", "price", "Description", "ratings", "product_link"])
        print("Data insertion completed.")
    except Exception as e:
        print(f"An error occurred during data insertion: {e}")
else:
    print("No data to insert.")

driver.quit()

import requests
from bs4 import BeautifulSoup
import clickhouse_connect
import uuid


# ClickHouse connection details
CLICK_HOUSE_HOST = "l1klbatlht.ap-south-1.aws.clickhouse.cloud"
CLICK_HOUSE_PORT = "8443"
CLICK_HOUSE_USER = "default"
CLICK_HOUSE_PASSWORD = "BBwfYXH.OyBY2"
CLICK_HOUSE_DATABASE = "Dealwallet"
CLICK_HOUSE_TABLE = "Deals"

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

# URL to scrape
url = 'https://www.ebay.com/globaldeals'

# Fetch the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    
    category_title = soup.find('h2', class_='dne-pattern-title').get_text(strip=True)
    item_tiles = soup.find_all('div', class_='dne-itemtile')
    print(f"Category: {category_title}\n")

    # List to hold item details
    elements = []
    
    for tile in item_tiles:
        id = str(uuid.uuid4())

        title_element = tile.find('h3', class_='dne-itemtile-title')
        name = title_element.get_text(strip=True) if title_element else "N/A"
        
        price_element = tile.find('span', itemprop='price')
        price = price_element.get_text(strip=True) if price_element else "N/A"
        
        original_price_element = tile.find('span', class_='itemtile-price-strikethrough')
        original_price = original_price_element.get_text(strip=True) if original_price_element else "N/A"
        
        link_element = tile.find('a', itemprop='url')
        link = link_element['href'] if link_element else "N/A"
        
        image_element = tile.find('img')
        image = image_element['src'] if image_element else "N/A"
        
        # Append as a tuple
        elements.append((id,name, price, original_price, link, image))  

    # Print each item's details
    for id,name, price, original_price, link, image in elements:
        print("Item Details:")
        print(f"name: {name}")
        print(f"Price: {price}")
        print(f"Original Price: {original_price}")
        print(f"Link: {link}")
        print(f"Image: {image}\n")
    
    # Count of items
    item_count = len(elements)
    print(f"Total items found: {item_count}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


if elements: 
    try:
        client.insert(CLICK_HOUSE_TABLE, elements, column_names=["id","name","price","original_price","link","image"])
        print("Data insertion completed.")
    except Exception as e:
        print(f"An error occurred during data insertion: {e}")
else:
    print("No data to insert.")

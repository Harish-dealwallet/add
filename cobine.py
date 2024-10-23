import time
import uuid
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import clickhouse_connect

# URL and selector mappings
url_selector_mapping = {
    "https://www.ebay.com/b/adidas/bn_21818843": {
        "product_container": "li.s-item.s-item--large",
        "product_name": "h3.s-item__title",
        "product_price": "span.s-item__price",
        "image": "img.s-item__image-img",
        "product_link": "a.s-item__link",
        "base_url": "https://www.adidas.com"
    },
    "https://www.meesho.com/baby-care/pl/3tj": {
        "product_container": "div.sc-dkrFOg.ProductList__GridCol-sc-8lnc8o-0.cokuZA.eCJiSA",
        "product_name": "p.NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5",
        "product_price": "h5.dwCrSh",
        "image": "img",
        "product_link": "a",
        "base_url": "https://www.meesho.com"
    },
    "https://www.amazon.in/gcx/Gifts-for-Everyone/gfhz/?ref_=nav_cs_giftfinder": {
        "product_container": "div.puis-card-container",
        "product_name": "span.a-size-base-plus",
        "product_price": "span.a-offscreen",
        "image": "img.s-image",
        "product_link": "a.a-link-normal",
        "base_url": "https://www.amazon.in"
    }
}

def scrape_and_insert():
    urls = list(url_selector_mapping.keys())
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    data = []

    # Connect to ClickHouse
    client = clickhouse_connect.get_client(
        host="l1klbatlht.ap-south-1.aws.clickhouse.cloud",
        port="8443",
        username="default",
        password="BBwfYXH.OyBY2",
        database="Dealwallet"
    )

    for url in urls:
        driver.get(url)
        selectors = url_selector_mapping[url]
        time.sleep(15)  # Wait for the page to load
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.select(selectors["product_container"])

        for product in products:
            product_name = product.select_one(selectors["product_name"]).text.strip() if product.select_one(selectors["product_name"]) else "No Name"
            product_price = product.select_one(selectors["product_price"]).text.strip() if product.select_one(selectors["product_price"]) else "Price Not Available"
            image = product.select_one(selectors["image"])['src'] if product.select_one(selectors["image"]) else "Image Not Available"
            product_link = product.select_one(selectors["product_link"])['href'] if product.select_one(selectors["product_link"]) else "Link Not Available"
            if selectors["base_url"] and product_link.startswith('/'):
                product_link = selectors["base_url"] + product_link

            # Create a unique ID for each product
            data.append({
                "id": str(uuid.uuid4()),  # Unique ID for each product
                "name": product_name,
                "price": product_price,
                "image": image,
                "product_link": product_link
            })

    driver.quit()

    # Prepare data for insertion
    mapped_data = [
        (
            product["id"],
            product["name"],
            product["price"],
            product["image"],
            product["product_link"]
        )
        for product in data
    ]

    print("Mapped Data for Insertion:", mapped_data)

    if mapped_data:
        try:
            client.insert('Dealwallet.Product', mapped_data, column_names=['id', 'name', 'price','image', 'product_link'])
            print("Data inserted successfully.")
        except Exception as e:
            print("Error inserting data:", e)
    else:
        print("No data to insert.")

if __name__ == "__main__":
    scrape_and_insert()

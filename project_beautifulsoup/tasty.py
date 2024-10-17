from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

service = Service('C:/Users/YourUsername/Downloads/chromedriver.exe')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.meesho.com/baby-care/pl/3tj') 

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-dkrFOg.ProductList__GridCol-sc-8lnc8o-0.cokuZA.eCJiSA")))

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

product_info = {}
image_src = soup.find('img')['src'] if soup.find('img') else None
product_info["src"]=image_src

product_title = soup.find('p', class_='NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5').text
product_info['Title'] = product_title

product_price = soup.find('h5', class_="sc-eDvSVe dwCrSh").text.strip()
product_info['Price'] = product_price

delivery_info = soup.find('span', class_='fkvMlU').text.strip()
product_info['Delivery'] = delivery_info

product_rating = soup.find('span', class_='laVOtN').text.strip()
product_info['Rating'] = product_rating

review_count = soup.find('span', class_='XndEO').text.strip()
product_info['Reviews'] = review_count

for key, value in product_info.items():
    print(f'{key}: {value}')

driver.quit()

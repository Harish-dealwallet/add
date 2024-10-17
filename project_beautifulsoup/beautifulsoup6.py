import requests
from bs4 import BeautifulSoup


url = "http://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"
responce= requests.get(url)
responce=responce.content
# print(r)


soup = BeautifulSoup(responce,"html.parser")
# print(soup)

# boxes = soup.find_all("div",class_ = "col-sm-4 col-lg")

names = soup.find_all("a",class_ ="title")

for i in names:
    print(i.text)

price = soup.find_all("h4",class_ = "pull-right price") 

for i in price:
    print(i.text)
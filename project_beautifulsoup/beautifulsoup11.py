import requests
from bs4 import BeautifulSoup

url="https://www.ebay.com/globaldeals"

respond=requests.get(url)
respond=respond.content

soup=BeautifulSoup(respond,"html.parser")

h2tag=soup.find("h2")
h2tag=h2tag.text
print(h2tag)

spantag=soup.find("h3")
spantag=spantag.text
print(spantag)

price_tag = soup.find('span', class_='first', itemprop='price')
price_tag=price_tag.text
print(price_tag)

tett = soup.find('span', class_='dne-itemcard-badge-text')
tett=tett.text
print(tett)

h02=soup.find("div",class_="ebayui-dne-banner-text")
h02=h02.text
print(h02)

itempro=soup.find("span",itemprop="name",class_="ebayui-ellipsis-2")
itempro=itempro.text
print(itempro)

price_tag = soup.find('span', class_='first', itemprop='price')
price_tag=price_tag.text
print(price_tag)
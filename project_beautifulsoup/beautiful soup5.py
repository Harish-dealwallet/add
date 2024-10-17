import requests
from bs4 import BeautifulSoup

url="https://books.toscrape.com/catalogue/page-2.html"

responsce=requests.get(url)
responsce=responsce.content
soup=BeautifulSoup(responsce,'html.parser')
print(soup)
ol=soup.find("ol")
articles=ol.find_all("article",class_="product_pod")
books=[]
for article in articles:
    image=article.find("image")
    title=article.find("h3")
    title=title.text
    stars=article.find("p")
    stars=stars["class"][1]
    price=article.find(class_="product_price")
    price=price.find("p").text
    books.append([ title,image,stars,price])



import requests
from bs4 import BeautifulSoup


url="https://tsssinfotech.com/services"

responce=requests.get(url)
responce=responce.content

soup=BeautifulSoup(responce,"html.parser")

headlines= soup.find_all("h1")
paragraphs = soup.find_all("p")

a = [h1.text.strip() for h1 in headlines]
b = [p.text.strip() for p in paragraphs]

for x in range(min(len(a), len(b))):
    print(f"{a[x]}: {b[x]}")
















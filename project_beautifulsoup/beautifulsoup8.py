import requests
from bs4 import BeautifulSoup

url = "https://tsssinfotech.com/process"

response = requests.get(url)
response = response.content
soup = BeautifulSoup(response, "html.parser")

headlines = soup.find_all("h2")
paragraphs = soup.find_all("p")

a = [h2.text.strip() for h2 in headlines]
b = [p.text.strip() for p in paragraphs]

for x in range(min(len(a), len(b))):
    print(f"{a[x]}: {b[x]}")

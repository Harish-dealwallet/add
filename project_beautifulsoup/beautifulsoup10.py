import requests
from bs4 import BeautifulSoup

url="https://tsssinfotech.com/technologies"

respond=requests.get(url)
respond=respond.content

soup=BeautifulSoup(respond,"html.parser")

tech=soup.find("h2")
tech=tech.text
print(tech)

para=soup.find("p")
para=para.text
print(para)

frontend=soup.find("h2",class_="text-center font-bold text-xl md:text-2xl lg:text-3xl mb-4")
frontend=frontend.text
print(frontend)

allh1=soup.find_all("h1",class_="text-sm md:text-base lg:text-xl font-bold text-center")
for h1 in allh1:
    print(h1.text)

other=soup.find("h2",class_="text-black font-bold text-[22px] lg:text-3xl text-center mt-0 md:mt-1 lg:mt-0 mb-4 md:mb- lg:mb-4")
other=other.text
print(other)

div_tags = soup.find_all('div', class_='collapse-title text-lg md:text-xl font-bold')

for div in div_tags:
     print(div.get_text(strip=True))
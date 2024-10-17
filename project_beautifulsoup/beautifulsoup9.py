import requests  
from bs4 import BeautifulSoup

url='https://tsssinfotech.com/works'
respond=requests.get(url)
respond=respond.content

soup=BeautifulSoup(respond,"html.parser")

headlines=soup.find("h1")
headlines=headlines.text
print(headlines)

agency=soup.find("p")
agency=agency.text
print(agency)

agency2=soup.find("p",class_="text-sm md:text-base lg:text-lg mt-1")
agency2=agency2.text
print(agency2)


h2tag=soup.find("h2")
h2tag=h2tag.text
print(h2tag)

images = soup.find_all('img', {'class': 'w-[10rem] lg:w-[13rem]', 'data-nimg': '1'})
print(images)
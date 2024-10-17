import bs4
import requests

text="geeksforgeeks"
url="https://google.com/search?q=" + text

result=requests.get(url)

soup=bs4.BeautifulSoup(result.text,"html.parser")

heading_object=soup.find_all( 'h3' ) 

for x in heading_object: 
    print(x.getText()) 
  
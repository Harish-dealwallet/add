import requests  
import bs4  
  
city = "Imphal"
  
url = "https://google.com/search?q=weather+in+" + city 
  

request_result = requests.get( url ) 
    
soup = bs4.BeautifulSoup( request_result.text  
                         , "html.parser" ) 
  
# Finding temperature in Celsius. 
# The temperature is stored inside the class "BNeawe".  
temp = soup.find( "div" , class_='BNeawe' ).text  
    
print( temp )  
from bs4 import BeautifulSoup
import requests
content = BeautifulSoup(get("www.twitter.com"), "html.parser")
tweet = content.findAll('p', attrs={"class": "content"}).text
print(tweet)

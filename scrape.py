#Scraping data from ksoutdoors.com

from bs4 import BeautifulSoup
import requests

url = "http://ksoutdoors.com/Fishing/Fishing-Reports/Northeast-Region"

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")





#Scraping data from ksoutdoors.com

from bs4 import BeautifulSoup
import requests

url = "http://ksoutdoors.com/Fishing/Fishing-Reports/Northeast-Region"

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")
count = 1
for i in soup.find_all('a'):
    if '/Fishing/Where-to-Fish-in-Kansas/Fishing-Locations-Public-Waters/Northeast-Region/' in i.attrs['href'].strip():
        print ('Found ' + str(count)
         + ':')
        count = count + 1
        print (i.contents[0])
        print('')

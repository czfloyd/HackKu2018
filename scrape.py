#Scraping data from ksoutdoors.com

from bs4 import BeautifulSoup
import requests

url = "http://ksoutdoors.com/Fishing/Fishing-Reports/Northeast-Region"

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")
count = int(0)
for i in soup.find_all('a'):
    if '/Fishing/Where-to-Fish-in-Kansas/Fishing-Locations-Public-Waters/Northeast-Region/' in i.attrs['href'].strip():
        fish = [[0 for x in range(100)] for y in range(100)] 
        if 'CLINTON RESERVOIR' in i.contents[0]:
            print (i.contents[0])
            infoTable = i.find_next('table')
            for info in infoTable.find_all('tr'):
                index = int(0)
                for specificInfo in info.find_all('td'):
			fish[count][i] = specificInfo.getText().strip()
			i = i + 1
            print(str(fish[count][0]) + str(fish[count][1]) + str(fish[count][2]) + str(fish[count][3]))
            count = count + 1

#Scraping data from ksoutdoors.com

from bs4 import BeautifulSoup
import requests

def fishscrape(lake):

    url = "http://ksoutdoors.com/Fishing/Fishing-Reports/Northeast-Region"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    count = int(0)
    skip = 0
    fish = [['' for x in range(50)] for y in range(50)]
    for i in soup.find_all('a'):
        if '/Fishing/Where-to-Fish-in-Kansas/Fishing-Locations-Public-Waters/Northeast-Region/' in i.attrs['href'].strip():
            if 'clinton'.lower() in lake.lower():
                if 'clinton'.lower() in i.contents[0].lower():
                    infoTable = i.find_next('table')
                    for info in infoTable.find_all('tr'):
                        if skip < 4:
                            skip = skip + 1
                            continue
                        index = int(0)
                        if info.getText().strip() == '':
                            continue
                        for specificInfo in info.find_all('td'):
                            if 'Water level' in specificInfo.getText().strip():
                                count = count - 1
                                break
                            if 'Newsletter' in specificInfo.getText().strip():
                                count = count - 1
                                break
                            if specificInfo.getText().strip() == '':
                                if index == 0:
                                    count = count - 1
                                    break
                                fish[count][index] = 'Unknown'
                                index = index + 1
                                continue
                            fish[count][index] = specificInfo.getText().strip()
                            index = index + 1
                        count = count + 1
    returnfish = [['' for y in range(3)] for x in range(count-1)]
    print (count-1)
    for x in range(count-1):
        for y in range(3):
            returnfish[x][y] = fish[x][y]
    return returnfish[x][y]

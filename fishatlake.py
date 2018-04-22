#Scraping data from ksoutdoors.com

from bs4 import BeautifulSoup
import requests

def fishatlake(fishtype, lake):

	url = "http://ksoutdoors.com/Fishing/Fishing-Reports/Northeast-Region"

	r = requests.get(url)

	soup = BeautifulSoup(r.text, "html.parser")
	count = int(0)
	for i in soup.find_all('a'):
	    if '/Fishing/Where-to-Fish-in-Kansas/Fishing-Locations-Public-Waters/Northeast-Region/' in i.attrs['href'].strip():
		if lake == 'clinton':
			if 'CLINTON RESERVOIR' in i.contents[0]:
			    infoTable = i.find_next('table')
			    for info in infoTable.find_all('tr'):
				index = int(0)
				for specificInfo in info.find_all('td'):
					if fishtype in specificInfo.getText().strip().lower():
						if specificInfo.find_next().getText().strip() =='Slow' or specificInfo.find_next().getText().strip() == 'Fair' or specificInfo.find_next().getText().strip() =='Good' or specificInfo.find_next().getText().strip() =='Poor' or specificInfo.find_next().getText().strip() =='Excellent':
							return(specificInfo.find_next().getText().strip())
		if lake == 'perry':
			if 'PERRY RESERVOIR' in i.contents[0]:
				infoTable = i.find_next('table')
				for info in infoTable.find_all('tr'):
					index = int(0)
					if fishtype == 'bass':
						for specificInfo in info.find_all('a'):
							if fishtype in specificInfo.getText().strip().lower():
								if specificInfo.find_next().getText().strip() =='Slow' or specificInfo.find_next().getText().strip() == 'Fair' or specificInfo.find_next().getText().strip() =='Good' or specificInfo.find_next().getText().strip() =='Poor' or specificInfo.find_next().getText().strip() =='Excellent':
									return(specificInfo.find_next().getText().strip())
					else:
						for specificInfo in info.find_all('a'):
							if fishtype in specificInfo.getText().strip().lower():
								if specificInfo.find_next().getText().strip() =='Slow' or specificInfo.find_next().getText().strip() == 'Fair' or specificInfo.find_next().getText().strip() =='Good' or specificInfo.find_next().getText().strip() =='Poor' or specificInfo.find_next().getText().strip() =='Excellent':
									return(specificInfo.find_next().getText().strip())
						
		if lake == 'milford':
			if 'MILFORD RESERVOIR' in i.contents[0]:
				infoTable = i.find_next('table')
				for info in infoTable.find_all('tr'):
					index = int(0)
					for specificInfo in info.find_all('td'):
						if fishtype in specificInfo.getText().strip().lower():
							if specificInfo.find_next().getText().strip() =='Slow' or specificInfo.find_next().getText().strip() == 'Fair' or specificInfo.find_next().getText().strip() =='Good' or specificInfo.find_next().getText().strip() =='Poor' or specificInfo.find_next().getText().strip() =='Excellent':
								return(specificInfo.find_next().getText().strip())



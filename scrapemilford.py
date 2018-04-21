#Scraping data for water temps at perry lake

from bs4 import BeautifulSoup
import requests

def milfordtemp():
	url = "http://www.nwk.usace.army.mil/Locations/District-Lakes/Milford-Lake/Daily-Lake-Info-2/"

	r = requests.get(url)

	soup = BeautifulSoup(r.text, "html.parser")

	for i in soup.find_all('span'):
		if i.getText() == 'Lake Water Surface Temperature:':
			return (int(i.find_next().getText().strip()))




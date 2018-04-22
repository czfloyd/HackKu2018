#Scraping data for water temps at perry lake

from bs4 import BeautifulSoup
import requests

def clintontemp():
	url = "http://www.nwk.usace.army.mil/Locations/District-Lakes/Clinton-Lake/Daily-Lake-Info-2/"

	r = requests.get(url)

	soup = BeautifulSoup(r.text, "html.parser")

	for i in soup.find_all('p'):
		if 'Water' in i.getText():
			return (int(i.getText()[28] + i.getText()[29]))

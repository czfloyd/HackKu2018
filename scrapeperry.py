#Scraping data for water temps at perry lake

from bs4 import BeautifulSoup
import requests

def perrytemp():
	url = "http://www.nwk.usace.army.mil/Locations/District-Lakes/Perry-Lake/Daily-Lake-Info-2/"

	r = requests.get(url)

	soup = BeautifulSoup(r.text, "html.parser")
	
	temp = 0
	
	for i in soup.find_all('p'):
		if 'Water Surface Temperature:' in i.contents[0]:
			return (int(str(i.getText()[28])+str(i.getText()[29])))




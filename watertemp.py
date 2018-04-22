#returns the water temp of given lake
from scrapeclinton import clintontemp
from scrapeperry import perrytemp
from scrapemilford import milfordtemp

def watertemp(lake):
	if lake == 'perry':
		return perrytemp()
	elif lake == 'clinton':
		return clintontemp()
	else:
		return milfordtemp()

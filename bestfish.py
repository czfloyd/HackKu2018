#returns the lake with the best fishing for a given fish

from fishatlake import fishatlake

def bestfish(fishtype):
	val1 = fishatlake(fishtype, 'clinton')
	val2 = fishatlake(fishtype, 'perry')
	val3 = fishatlake(fishtype, 'milford')
	
	first = toranking(val1[0])
	second = toranking(val2[0])
	third = toranking(val3[0])

	D = ["first", "second", "third"]

	if(third > second):
		temp = second
		second = third
		third = temp

		temp = D[2]
		D[2] = D[1]
		D[1] = temp

	if(second > first):
		temp = first
		first = second
		second = temp
		
		temp = D[0]
		D[0] = D[1]
		D[1] = temp

	if(D[0] == "first"):
		return "clinton"
	elif(D[1] == "second"):
		return "perry"
	else:
		return "milford"
	


def toranking(entry):
	if(entry == 'Poor'):
		return 0
	elif(entry == 'Slow'):
		return 1
	elif(entry == 'Fair'):
		return 2
	elif(entry == 'Good'):
		return 3
	else:
		return 4

print(bestfish('catfish'))

#function defining lure/bait to use based on fishtype, watertemp, and season

def luretype(fish, season, watertemp):
	if fish == "bass":
		if season == "fall":
			if watertemp > 65:
				return " use crankbaits, spinnerbaits, jigs, or frogs"
			elif watertemp <= 65 and watertemp > 60:
				return " use buzzbaits, crankbaits, jigs, or worms"
			elif watertemp <= 60 and watertemp > 55:
				return " use bladebaits, crankbaits, spoons, or topwater"
			else:
				return " use bladebaits, spoons, jigs, or jerkbaits"
		elif season == "summer":
			if watertemp > 75:
				return " use topwaters, frogs, spoons, or deep diving crankbaits"
			else:
				return " use shallow crankbaits, jigs, small worms, or buzzbaits"
		elif season == "spring":
			if watertemp < 65:
				return " use jerkbaits, plastics, tubes, or spinners"
			else:
				return " use topwaters, plastics, frogs, or swimbaits"
		else:
			if watertemp > 55:
				return " use jerkbaits, crankbaits, or plastics"
			elif watertemp <= 55 and watertemp > 50:
				return " use spoons jerkbaits, crankbaits, or jigs"
			elif watertemp <= 50 and watertemp > 40:
				return " use spoons, jerkbaits, or grubs"
			else:
				return " use jigs, spoons, or grubs"
	else:
		if season == "spring":
			return " use fresh herring or shad"
		elif season == "summer":
			return " use fresh sucker or stink bait"
		elif season == "fall":
			return " use crayfish, frogs, or grasshoppers"
		else:
			return " use jigs or live bait"



print(luretype("bass", "winter", 50))



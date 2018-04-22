from __future__ import print_function
from datetime import date, datetime
import json
from bs4 import BeautifulSoup
from botocore.vendored import requests

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(output, should_end_session):
	return {
		'outputSpeech': {
			'type': 'PlainText',
			'text': output
		},
		'shouldEndSession': should_end_session
	}

def build_response(session_attributes, speechlet_response):
	return {
		'version': '1.0',
		'sessionAttributes': session_attributes,
		'response': speechlet_response
	}


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
	session_attributes = {}
	card_title = "Welcome"
	speech_output = "Hello Andre and Nathan "
	reprompt_text = None
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def handle_session_end_request():
	card_title = "Session Ended"
	speech_output = "Goodbye "
	should_end_session = True
	return build_response({}, build_speechlet_response(speech_output, should_end_session))


def by_place(intent, session):
    session_attributes = {}
    fish_type = intent['slots']['fish']['value']
    reprompt_text = None
    speech_output = 'I would now say where to catch {}'.format(fish_type)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def by_lake(intent, session):
    session_attributes = {}
    lake_name = intent['slots']['lake']['value']
    reprompt_text = None
    speech_output = 'I would now report about the fishing conditions at {}'.format(lake_name)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def bait_type(intent, session):
    session_attributes = {}
    fish_type = intent['slots']['fish']['value']
    location = intent['slots']['lake']['value']
    reprompt_text = None
    bait_type = luretype(fish_type, findseason(), watertemp(location))
    speech_output = 'You should {}'.format(bait_type)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def bait_not_type(intent, session):
    session_attributes = {}
    fish_type = intent['slots']['fish']['value']
    reprompt_text = None
    bait_type = luretype(fish_type, findseason(), watertemp('clinton'))
    speech_output = 'You should {}'.format(bait_type)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def fish_at_place(intent, session):
    session_attributes = {}
    fish_type = intent['slots']['fish']['value']
    location = intent['slots']['lake']['value']
    reprompt_text = None
    status = 'good'
    #status = getStatus(fish_type, location)
    speech_output = 'You should {}'.format(status)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def hello_name(intent, session):
	session_attributes = {}
	firstname = intent['slots']['firstname']['value']
	reprompt_text = None
	speech_output = 'Hello {} Nice to Meet You'.format(firstname)
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))




# --------------- Specific Events ------------------

def on_intent(intent_request, session):
	print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
	intent = intent_request['intent']
	intent_name = intent_request['intent']['name']
	if intent_name == "ByPlace":
		return by_place(intent, session)
	elif intent_name == "ByLake":
	    return by_lake(intent, session)
	elif intent_name == "BaitType":
	    return bait_type(intent, session)
	elif intent_name == "BaitNotPlace":
	    return bait_not_type(intent, session)
	elif intent_name == "FishAtPlace":
	    return fish_at_place(intent, session)
	elif intent_name == "AMAZON.HelpIntent":
		return get_welcome_response()
	elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
		return handle_session_end_request()
	else:
		raise ValueError("Invalid intent")

# --------------- Generic Events ------------------

def on_session_started(session_started_request, session):
	print("on_session_started requestId=" + session_started_request['requestId']+ ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
	print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
	return get_welcome_response()

def on_session_ended(session_ended_request, session):
	print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])


# --------------- Main handler -------------------

def lambda_handler(event, context):
	print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
	if event['session']['new']:
		on_session_started({'requestId': event['request']['requestId']}, event['session'])
	if event['request']['type'] == "LaunchRequest":
		return on_launch(event['request'], event['session'])
	elif event['request']['type'] == "IntentRequest":
		return on_intent(event['request'], event['session'])
	elif event['request']['type'] == "SessionEndedRequest":
		return on_session_ended(event['request'], event['session'])

#------------- Handling Data ---------------------

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

#determines the season based on today's date
Y = 2000
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

def findseason():
	return (get_season(date.today()))

#gets Milford's Temperature
def milfordtemp():
	url = "http://www.nwk.usace.army.mil/Locations/District-Lakes/Milford-Lake/Daily-Lake-Info-2/"

	r = requests.get(url)

	soup = BeautifulSoup(r.text, "html.parser")

	for i in soup.find_all('span'):
		if i.getText() == 'Lake Water Surface Temperature:':
			return (int(i.find_next().getText().strip()))

#gets Perry's Temperature
def perrytemp():
	url = "http://www.nwk.usace.army.mil/Locations/District-Lakes/Perry-Lake/Daily-Lake-Info-2/"

	r = requests.get(url)

	soup = BeautifulSoup(r.text, "html.parser")

	temp = 0

	for i in soup.find_all('p'):
		if 'Water Surface Temperature:' in i.contents[0]:
			return (int(str(i.getText()[28])+str(i.getText()[29])))

#gets Clinton's Temperature
def clintontemp():
	url = "http://www.nwk.usace.army.mil/Locations/District-Lakes/Clinton-Lake/Daily-Lake-Info-2/"

	r = requests.get(url)

	soup = BeautifulSoup(r.text, "html.parser")

	for i in soup.find_all('p'):
		if 'Water' in i.getText():
			return (int(i.getText()[28] + i.getText()[29]))

#finds water temperature from lake lake_name
def watertemp(lake):
	if lake == 'perry':
		return perrytemp()
	elif lake == 'clinton':
		return clintontemp()
	else:
		return milfordtemp()

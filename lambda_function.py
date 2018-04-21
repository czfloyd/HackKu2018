from __future__ import print_function
from datetime import date, datetime
import json
from bs4 import BeautifulSoup
import requests
from luretype import luretype
from findseason import findseason
from watertemp import watertemp

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
    reprompt_text = None

    speech_output = 'I would now say what to use to catch {}'.format(fish_type)
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

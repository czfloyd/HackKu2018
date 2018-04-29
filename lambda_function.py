from __future__ import print_function
from datetime import date, datetime
import json
from bs4 import BeautifulSoup
from botocore.vendored import requests

supported_lakes = ["milford", "perry", "clinton"]
supported_fish = ["catfish", "bass"]

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
    speech_output = "Welcome to Kansas fishing. Are you looking for information about lakes or fish? "
    reprompt_text = "I can help you get information on various fishing conditions nearby. I'll ask questions to help you get the information you need. To start, would you like information on lakes or fish?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def get_help():
    session_attributes = {}
    speech_output = "Currently, kansas fishing can give you status updates on the fishing conditions at a lake including fish ratings and weights, help you choose which bait to use for a type of fish at a lake,  "
    speech_output += "tell you which lake is best for catching a specific fish, and tell you how a specific fish is rated at a lake."
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def sample_commands():
    session_attributes = {}
    speech_output = "Sample commands include: Ask kansas fishing where I can catch catfish. Ask kansas fishing how all the fish are rated at Milford lake. "
    speech_output += "Ask kansas fishing what I should use to catch bass at Clinton. Ask kansas fishing how catfish are at Perry lake."
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Goodbye "
    should_end_session = True
    return build_response({}, build_speechlet_response(speech_output, should_end_session))


def fish_menu():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "I currently have information on bass and catfish. "
    speech_output += "I can answer what bait to use and where is best to catch them. "
    speech_output += "What would you like to hear? "
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def lakes_menu():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "I currently have information on clinton, perry and milford lakes. "
    speech_output += "I can tell you how the fishing is at one or give you an in depth report for one. "
    speech_output += " What would you like to hear? "
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def by_place(intent, session):
    session_attributes = {}
    if not fish_checker(intent):
       return fish_error_handler()
    fish_type = handlesyns(intent['slots']['fish']['value'])
    reprompt_text = None
    lake = bestfish(fish_type)
    speech_output = 'The best place to catch {} is at {}.'.format(fish_type, lake)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def by_lake(intent, session):
    session_attributes = {}
    if not lakes_checker(intent):
       return lakes_error_handler()
    location = handlesyns(intent['slots']['lake']['value']).lower()
    reprompt_text = None
    fish = fishscrape(location)
    speech_output = 'For {}, '.format(location.lower())
    for x in range(len(fish)-1):
        speech_output += ' {} is rated to be {} and their likely weight will be {}. '.format(fish[x][0], fish[x][1], fish[x][2])
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def by_lake_rates_only(intent, session):
    session_attributes = {}
    if not lakes_checker(intent):
       return lakes_error_handler()
    location = handlesyns(intent['slots']['lake']['value']).lower()
    reprompt_text = None
    fish = fishscrape(location)
    speech_output = 'For {}, '.format(location.lower())
    for x in range(len(fish)-1):
        speech_output += ' {} is rated to be {}. '.format(fish[x][0], fish[x][1])
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def by_lake_weights_only(intent, session):
    session_attributes = {}
    if not lakes_checker(intent):
       return lakes_error_handler()
    location = handlesyns(intent['slots']['lake']['value']).lower()
    reprompt_text = None
    fish = fishscrape(location)
    speech_output = 'For {}, '.format(location.lower())
    for x in range(len(fish)-1):
        speech_output += ' {} is expected to have a weight of {}.. '.format(fish[x][0], fish[x][2])
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def bait_type(intent, session):
    session_attributes = {}
    if not fish_checker(intent):
       return fish_error_handler()
    if not lakes_checker(intent):
       return lakes_error_handler()
    fish_type = handlesyns(intent['slots']['fish']['value']).lower()
    location = handlesyns(intent['slots']['lake']['value']).lower()
    reprompt_text = None
    bait_type = luretype(fish_type, findseason(), watertemp(location))
    speech_output = 'You should {}'.format(bait_type)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def bait_not_type(intent, session):
    session_attributes = {}
    if not fish_checker(intent):
       return fish_error_handler()
    fish_type = handlesyns(intent['slots']['fish']['value']).lower()
    reprompt_text = None
    bait_type = luretype(fish_type, findseason(), watertemp('clinton'))
    speech_output = 'You should {}'.format(bait_type)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def fish_at_place(intent, session):
    session_attributes = {}
    if not fish_checker(intent):
       return fish_error_handler()
    if not lakes_checker(intent):
       return lakes_error_handler()
    fish_type = handlesyns(intent['slots']['fish']['value']).lower()
    location = handlesyns(intent['slots']['lake']['value']).lower()
    reprompt_text = None
    status = fishatlake(fish_type.lower(), location.lower())
    speech_output = 'The condition of {} at {} is {}'.format(status[1], location, status[0])
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))



# --------------- Specific Events ------------------

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "ByPlace":
        return by_place(intent, session)
    elif intent_name == "FishMenu":
        return fish_menu()
    elif intent_name == "LakesMenu":
        return lakes_menu()
    elif intent_name == "ByLakeRateVerbose":
        return by_lake(intent, session)
    elif intent_name == "ByLake":
        return by_lake_rates_only(intent, session)
    elif intent_name == "ByLakeWeightOnly":
        return by_lake_weights_only(intent, session)
    elif intent_name == "BaitType":
        return bait_type(intent, session)
    elif intent_name == "BaitNotPlace":
        return bait_not_type(intent, session)
    elif intent_name == "SampleCommands":
        return sample_commands()
    elif intent_name == "FishAtPlace":
        return fish_at_place(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
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

#------------- Error Handling --------------------

def lake_checker(intent):
    if 'lake' in intent['slots']:
        if 'value' not in intent['slots']['lake']:
            return False
    return True

def fish_checker(intent):
    if 'fish' in intent['slots']:
        if 'value' not in intent['slots']['fish']:
            return False
    return True

def lakes_error_handler():
    speech_output = "I didn't catch that. We currently have information for the following lakes: "
    for i in supported_lakes:
        speech_output += i + ", "
    speech_output += ". Please ask again. "
    should_end_session = False
    return build_response({}, build_speechlet_response(speech_output, should_end_session))

def fish_error_handler():
    speech_output = "I didn't catch that. We currently have information for the following fish: "
    for i in supported_fish:
        speech_output += i + ", "
    speech_output += ". Please ask again. "
    should_end_session = False
    return build_response({}, build_speechlet_response(speech_output, should_end_session))

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

#finds the condition of a type of fish at a lake
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
                                    D = [specificInfo.find_next().getText().strip(), specificInfo.getText().strip()]
                                    return(D)
            if lake == 'perry':
                if 'PERRY RESERVOIR' in i.contents[0]:
                    infoTable = i.find_next('table')
                    for info in infoTable.find_all('tr'):
                        index = int(0)
                        if fishtype == 'bass':
                            for specificInfo in info.find_all('a'):
                                if fishtype in specificInfo.getText().strip().lower():
                                    if specificInfo.find_next().getText().strip() =='Slow' or specificInfo.find_next().getText().strip() == 'Fair' or specificInfo.find_next().getText().strip() =='Good' or specificInfo.find_next().getText().strip() =='Poor' or specificInfo.find_next().getText().strip() =='Excellent':
                                        D = [specificInfo.find_next().getText().strip(), specificInfo.getText().strip()]
                                        return(D)
                        else:
                            for specificInfo in info.find_all('a'):
                                if fishtype in specificInfo.getText().strip().lower():
                                    if specificInfo.find_next().getText().strip() =='Slow' or specificInfo.find_next().getText().strip() == 'Fair' or specificInfo.find_next().getText().strip() =='Good' or specificInfo.find_next().getText().strip() =='Poor' or specificInfo.find_next().getText().strip() =='Excellent':
                                        D = [specificInfo.find_next().getText().strip(), specificInfo.getText().strip()]
                                        return(D)
            if lake == 'milford':
                if 'MILFORD RESERVOIR' in i.contents[0]:
                    infoTable = i.find_next('table')
                    for info in infoTable.find_all('tr'):
                        index = int(0)
                        for specificInfo in info.find_all('td'):
                            if fishtype in specificInfo.getText().strip().lower():
                                if specificInfo.find_next().getText().strip() =='Slow' or specificInfo.find_next().getText().strip() == 'Fair' or specificInfo.find_next().getText().strip() =='Good' or specificInfo.find_next().getText().strip() =='Poor' or specificInfo.find_next().getText().strip() =='Excellent':
                                    D = [specificInfo.find_next().getText().strip(), specificInfo.getText().strip()]
                                    return(D)


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
            if 'perry'.lower() in lake.lower():
                if 'perry'.lower() in i.contents[0].lower():
                    infoTable = i.find_next('table')
                    for info in infoTable.find_all('tr'):
                        if skip < 2:
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
                            if 'Largemouth BassSmallmouth Bass' in specificInfo.getText().strip():
                                fish[count][index] = 'Largemouth Bass and Smallmouth Bass'
                            if 'FairFair' in specificInfo.getText().strip():
                                fish[count][index] = 'Fair'
                            if 'up to 5.0 lbs.up to 3.0 lbs.' in specificInfo.getText().strip():
                                fish[count][index] = 'up to 5.0 lbs and 3.0 lbs respectively.'
                            index = index + 1
                        count = count + 1
                    count = count - 1
            if 'milford'.lower() in lake.lower():
                if 'milford'.lower() in i.contents[0].lower():
                    infoTable = i.find_next('table')
                    for info in infoTable.find_all('tr'):
                        if skip < 1:
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
                    count = count - 1
    returnfish = [['' for y in range(3)] for x in range(count-1)]
    for x in range(count-1):
        for y in range(3):
            returnfish[x][y] = fish[x][y]
    return returnfish


def bestfish(fishtype):

    val1 = fishatlake(fishtype, 'clinton')
    val2 = fishatlake(fishtype, 'perry')
    val3 = fishatlake(fishtype, 'milford')

    first = toranking(val1[0])
    second = toranking(val2[0])
    third = -10

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

def handlesyns(word):
    if not word:
        return word
    if word.lower() == 'cat fish':
        return 'catfish'
    elif word.lower() == 'paris':
        return 'perry'
    elif word.lower() == 'mill ford':
        return 'milford'
    else:
        return word

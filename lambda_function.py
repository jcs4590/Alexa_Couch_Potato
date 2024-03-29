"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import HttpHelper
import TvShow
import json, re
import Enums



def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent_name)
    # Dispatch to your skill's intent handlers
    if intent_name == "NextAirDate":
        return get_tv_show(intent, session)
    elif intent_name == "TvShowNetwork":
        return search_network(intent, session)
    elif intent_name == "ShowsOnDate":
        return get_shows_for_date_intent(intent, session)
    elif intent_name == "FilterAllSHows":
        return filter_shows(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------

def add_shows_to_session(shows):
    return {"shows": json.dumps([ob.__dict__ for ob in shows])}
def add_text_to_session(key, text):
    return {key: text}



def add_sml_tag(text):
    return "<speak>" + text + "</speak>"

############# intent handlers ##############################
### MEthod gets called when multiple shows found#####
## TRYing to filter by network #####

def filter_shows(intent, session):
    session_attributes = {}
    reprompt_text = None
    print("filters in intents slots : {}".format(intent["slots"]))

    # if "favoriteColor" in session.get('attributes', {}):
    if "Filter" in intent["slots"] and "value" in intent["slots"]["Filter"]:
        filter_text = intent["slots"]["Filter"]["value"]

        print("session in filter intents : {}".format(session))

        date = "2015-12-20" #intent['slots']['ShowForDate']['value']
        print(date)

        shows = get_shows_for_date(date)
        show_count = len(shows)


        ## returns tuple
        results = get_list_for_shows_text(shows, 15, filter_text=filter_text)
        session_attributes.update(results[1])
        speech_output = "<p>Shows only on {}</p> are {}" .format(filter_text,results[0])


        should_end_session = True
    else:
        speech_output = "I was not able to understand the netowrk to filter by. Just say Alexa, filter by HBO"
        reprompt_text = "I was not able to understand the netowrk to filter by. Just say Alexa, filter by HBO"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
            intent['name'], add_sml_tag(speech_output), reprompt_text, should_end_session))


def get_shows_for_date(date):
    ## get shows
    request_helper = HttpHelper.HttpHelper()
    request_helper.add_urls([Enums.API_URLS["shows_for_date"].format(date)])
    request_helper.start_minions(request_helper.get_tv_shows)
    return request_helper.shows


def search_network(intent, session):
    session_attributes = {}
    reprompt_text = None

    # if "favoriteColor" in session.get('attributes', {}):
    if "network" in intent["slots"]:
        print("network in intents slots : {}".format(intent["slots"]))
        network = intent["slots"]["network"]["value"]

        ##get shows from session
        if "shows" in session.get("attributes", {}):
            shows = HttpHelper.HttpHelper().get_shows_objects_from_session(
                json.loads(session['attributes']["shows"]))  ##show objects
            print("LAkers!! network = {}".format(network))
            for show in shows:
                if show.is_network_match(network):
                    speech_output = get_next_episode_date_text(show)
                    break
                else:
                    speech_output = "No tv show was found for the network {}.".format(network)

        else:
            speech_output = "Having session issues. Sorry!"
        should_end_session = True
    else:
        speech_output = "I wasn't able to understand what network that was. You can " \
                        "Tell me which network by saying. The tv show is on FOX."
        reprompt_text = "Tell me which network by saying. The tv show is on FOX."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
            intent['name'], add_sml_tag(speech_output), reprompt_text, should_end_session))
def get_next_episode_date_text(show):
    date = show.get_next_episode_date()
    if date is None:
        if show.status.lower() == "ended":
            date = show.get_prev_episode_date()
            if date is None:
                speech_output = "The tv show {} is no longer running".format(show.name)
            else:
                speech_output = "The TV Show {} is no longer running. " \
                                "It lasted {} seasons and The last " \
                                "episode aired on {}".format(show.name,
                                                             show.prev_episode["season"],
                                                             date)
        else:
            speech_output = "I do not have a date for the next {} episode. but, I do know it" \
                            " is still active.".format(show.name)
        return speech_output
    return "The new episode of {} will air on {} on {}".format(show.name, date, show.network["name"])


def get_tv_show(intent, session):
    """ get single tv show
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    print(intent['slots'])
    if 'value' in intent['slots']["Show"]:
        print("inside this bitch")
        ## get tv show name
        tv_show = intent['slots']['Show']['value']

        tv_show = clean_tv_show(tv_show)
        ## check if tv show is one that has numbers in it
        if tv_show in Enums.SHOWS_WITH_NUMBERS:
            tv_show = Enums.SHOWS_WITH_NUMBERS[tv_show]

        ## get shows
        request_helper = HttpHelper.HttpHelper()
        request_helper.add_urls([Enums.API_URLS["show_search"].format(tv_show)])
        request_helper.start_minions(request_helper.get_tv_shows)
        shows = request_helper.shows
        show_count = len(shows)

        ##more than one show found
        if show_count > 1:
            session_attributes = add_shows_to_session(shows)
            speech_output = "I found {} tv shows matching the title {}. ".format(show_count, tv_show) + \
                            "What network is the show on?"
            print( speech_output)
        ##one show found
        elif show_count == 1:
            show = shows[0]
            speech_output = get_next_episode_date_text(show)
        ## no show found
        else:
            speech_output = "Sorry. I did not find any results"

        reprompt_text = None
    else:
        speech_output = "I wasn't able to get that. You can tell me to search for a show by saying. " \
                        "when does The Walking Dead air next?"
        reprompt_text = "You can tell me to search for a show by saying. when does The Walking Dead air next?"
    return build_response(session_attributes, build_speechlet_response(
            card_title, add_sml_tag(speech_output), reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello, I am couch potato. I can search for a show and tell you when it will air next. I can also " \
                    "recommend similar shows. " \
                    "and save your favorite shows and give you updates"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
            card_title, add_sml_tag(speech_output), reprompt_text, should_end_session))

def clean_tv_show(tv_show):
    tv_show = tv_show.replace("when does the show", "").strip()
    tv_show = tv_show.replace("when is the new episode of", "").strip()
    tv_show = tv_show.replace("when is the next episode of", "").strip()
    tv_show = tv_show.replace("when is the new", "").strip()
    tv_show = tv_show.replace("when is the next", "").strip()
    tv_show = tv_show.replace("when is","").strip()
    tv_show = tv_show.replace("when does", "").rstrip("next").strip()

    print("clean show title: {}".format(tv_show))
    return tv_show

def get_shows_for_date_intent(intent, session):
    network, date, time = None
    card_title = "Guide LookUp"
    session_attributes = {}
    should_end_session = False
    if "ShowsForDate" in intent["slots"] and "value" in intent["slots"]["ShowsForDate"]:
        ## get date
        date = intent['slots']['ShowsForDate']['value']
        session_attributes.update(add_text_to_session("search_date",date))
        print(date)
    if "TimeForShow" in intent["slots"] and "value" in intent["slots"]["TimeForShow"]:
        time = intent["slots"]["TimeForShow"]["value"]
        session_attributes.update(add_text_to_session("search_time",time))
    if "NetworkForDate" in intent["slots"] and "value" in intent["slots"]["NetworkForDate"]:
        network = intent["slots"]["NetworkForDate"]["value"]
        session_attributes.update(add_text_to_session("search_network",network))

    if network is not None or time is not None or date is not None:
        ##get shows
        shows = get_shows_for_date(date)
        show_count = len(shows)

        ##more than one show found
        if show_count > 0:
            #session_attributes = add_shows_to_session(shows)
            text = "<p>I found {} tv shows matching playing on {}.</p> ".format(show_count, date) + \
                            "<p>You can filter your choices any time by saying Alexa, filter by HBO</p> <p>or if you want" \
                            " more information on a specific show just say Alexa, more info on Grey's Anatomy</p>  <p>Here " \
                            "are the shows:</p> {}"

            response_text ,sessh = get_list_for_shows_text(shows,len(text))
            session_attributes.update(sessh)
            speech_output = text.format(response_text)
        else:
            speech_output = "Sorry. I did not find any results"

        reprompt_text = None

    else:

        text = "I wasn't able to get that. You can tell me to search for a show on any given date by saying. " \
                        "What shows or on December 10, 2015? or saying What shows are on Today?"
        speech_output = text
        reprompt_text = text
    return build_response(session_attributes, build_speechlet_response(
            card_title, add_sml_tag(speech_output), reprompt_text, should_end_session))


def get_list_for_shows_text(shows, char_count, filter_text=None):
    session_attribute = {}
    if filter_text is not None:
        shows = filter(lambda x: filter_text.upper() in x.network["name"], shows)
    if len(shows) == 0:
        return "<p>Did not find any shows for that netowrk. Sorry</p>", session_attribute

    prev_time = shows[0].get_current_episode_time()
    text = "<p>Shows starting at {}</p>".format(prev_time)
    char_count += len(text)
    for index, show in enumerate(shows):
        if char_count > 6000:
            session_attribute = add_text_to_session("last_index", index)
            break
        current_time = show.get_current_episode_time()
        char_count += len(text)
        #
        if prev_time.replace(" ","") != current_time.replace(" ",""):
            text += "<p>Shows starting at {} are: {} on {} </p>".format(current_time,
                                                                        fix_string(show.name),
                                                                        fix_string(show.network["name"]))
            prev_time = current_time

        else:
            text += "<p>Playing on {}  is {}</p> ".format(fix_string(show.network["name"]), fix_string(show.name))
    return text, session_attribute
############## end intent handlers

def fix_string(text):
    return text.encode('utf-8').strip().replace("&"," and " )

#  --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

from alexa.ask.utils import VoiceHandler, ResponseBuilder as r
from markov.markov import get_rhyme, get_model
import json
import os
import tinys3

chains = {}
for file in os.listdir("models"):
    chains[file[:-5]] = get_model("models/%s" % file)

with open("KEYS") as keyfile:
    S3_ACCESS_KEY = f.readline().strip()
    S3_SECRET_KEY = f.readline().strip()
    conn = tinys3.Connection(S3_ACCESS_KEY, S3_SECRET_KEY, tls=True)

"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015

Each VoiceHandler function receives a ResponseBuilder object as input and outputs a Response object
A response object is defined as the output of ResponseBuilder.create_response()
"""

def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return r.create_response(message="Rap like who?")


@VoiceHandler(request_type="LaunchRequest")
def launch_request_handler(request):
    """
    Annoatate functions with @VoiceHandler so that they can be automatically mapped
    to request types.
    Use the 'request_type' field to map them to non-intent requests
    """
    return r.create_response(message="Hello Welcome to My Recipes!")


@VoiceHandler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return r.create_response(message="Goodbye!")


@VoiceHandler(intent='StartLike')
def get_rapper_intent_handler(request):
    """
    Use the 'intent' field in the VoiceHandler to map to the respective intent.
    You can insert arbitrary business logic code here
    """

    # Get variables like userId, slots, intent name etc from the 'Request' object
    rapper = request.get_slot_value("Rapper")
    rapper = rapper if rapper else ""

    with open("models/intros.json") as file:
        intros = json.load(file)

    try:
        intro = intros[rapper]
    except KeyError:
        intro = ""

    try:
        rap = get_rhyme(chains[rapper], 8)
    except KeyError:
        return r.create_response(message="I heard, %s, but I don't know that rapper." % rapper, end_session=False)

    rap = "<speak>Yo my name is {}. ".format(rapper) + intro + " " + rap + '<audio src="https://s3.amazonaws.com/danielgwilson.com/MLG+Horns+Sound+Effect.mp3" /></speak>'

    upload_rap(rap[7:-94])

    # Use ResponseBuilder object to build responses and UI cards
    card = r.create_card(title="Rapping",
                         subtitle=None,
                         content=rap)


    return r.create_response(message=rap,
                             is_ssml=True,
                             end_session=False,
                             card_obj=card)


@VoiceHandler(intent="Start")
def call_back_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    rap = get_rhyme(chains["toponehundredraps"], 8)
    upload_rap(rap[7:-94])
    return r.create_response(is_ssml=True, message="<speak>Aight yo I'm gonna rap. "  + rap + '<audio src="https://s3.amazonaws.com/danielgwilson.com/MLG+Horns+Sound+Effect.mp3" /></speak>')


def upload_rap(rap):
    """
    Saves rap to json and uploads it, so it can be read
    """
    with open("rap", "w") as file:
        file.write(rap)
    with open("rap", "rb") as file:
        conn.upload('rap', file, 'rapbattlealexa', public=True)

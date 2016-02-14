from alexa.ask.utils import VoiceHandler, ResponseBuilder as r
from markov.markov import get_rhyme

"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015

Each VoiceHandler function receives a ResponseBuilder object as input and outputs a Response object
A response object is defined as the output of ResponseBuilder.create_response()
"""

def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return r.create_response(message="Just ask")


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

    intros = {'eminem':'Yo I\'m the real shady the real slim shady, here I go.', 'drake':'Jump man jump man jump man what.', 'yeezus':'I\'m gonna let you finish. but Beyonce, is the best singer, of all time'}

    intro = intros[rapper] if intros[rapper] else ""

    rap = get_rhyme("models/top100raps.json", 8)
    # rap = "hi"

    #Use ResponseBuilder object to build responses and UI cards
    card = r.create_card(title="Rapping",
                         subtitle=None,
                         content=("Yo my name is {}. ".format(rapper)) + intro + " Alexa, drop me a fat beat. " + rap)


    return r.create_response(message=("Yo my name is {}. ".format(rapper) + intro + " Alexa, drop me a fat beat. " + rap),
                             end_session=False,
                             card_obj=card)


@VoiceHandler(intent="Start")
def call_back_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    rap = get_rhyme("models/top100raps.json", 8)
    # rap = "hi"
    return r.create_response(message="Aight yo I'm gonna rap. Alexa, drop me a fat beat. " + rap)

@VoiceHandler(intent="DropBeat")
def drop_beat_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    return r.create_response(message="boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and ")

from alexa.ask.utils import VoiceHandler, ResponseBuilder as r

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

@VoiceHandler(intent="DropBeat")
def drop_beat_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    return r.create_response(message="boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and ")

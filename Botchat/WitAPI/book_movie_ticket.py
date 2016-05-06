from wit import Wit
import logging
logging.captureWarnings(True)


# Weather example
# See https://wit.ai/patapizza/example-weather

access_token = 'E4MRWR475N2EYBCUCHJZEEMDSKR7N2YT'
def say(session_id, msg):
    print('>> Bot: %s' % msg)

def merge(context, entities):
    if 'movie_name' in entities:
        context['movie_name'] = entities['movie_name'][0]['value']
    if 'location' in entities:
        context['location'] = entities['location'][0]['value']
    if 'ticket_number' in entities:
        context['ticket_number'] = entities['ticket_number'][0]['value']
    if 'watch_datetime' in entities:
        context['watch_datetime'] = entities['watch_datetime'][0]['value']
    if 'bye' in entities:
        context['bye'] = entities['bye'][0]['value']
    return context

def error(session_id, msg):
    print('Oops, I don\'t know what to do.')

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    }
client = Wit(access_token, actions)

session_id = '570e093c-d32c-4859-85af-626afdc69d9c'
context = {}
while 'bye' not in context:
    mess = raw_input(">> You: ")
    client.run_actions(session_id, mess, context)


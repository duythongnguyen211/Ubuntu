# -- coding: cp1252 --
#  Simple app ask for weather
# https://wit.ai/duythongnguyen211/SimpleWeather

from wit import Wit
import requests
import datetime
from geopy import geocoders
import dateutil.parser
import logging
logging.captureWarnings(True)


session_id = '570f0896-1b49-411e-851f-92132b58d369'
access_token = 'P4BCO7CGU3EKXJXTLDM7CDDXC3TWSJKA'
weatherAPI = 'e95f625e65417dbb3ef357053c799592'


def say(session_id, context, msg):
    print(">> Bot: %s" % msg)


def merge(session_id, context, entities, user_msg):
    if 'query' in entities:
        context['query'] = entities['query'][0]['value']
    if 'location' in entities:
        context['location'] = entities['location']
    if 'datetime' in entities:
        context['datetime'] = entities['datetime']
    if 'my_name' in entities:
        context['my_name'] = entities['my_name'][0]['value']
    if 'thank' in entities:
        context['thank'] = entities['thank'][0]['value']
    if 'hello' in entities:
        context['hello'] = entities['hello'][0]['value']
    if 'about_you' in entities:
        context['about_you'] = entities['about_you'][0]['value']
    if 'help' in entities:
        context['help'] = entities['help'][0]['value']
    return context


def error(session_id, context, msg):
    print(">> Bot: Oops, I don\'t know what to do. Enter \'help\' to get help. Thanks.")


def parse_datetime(date):
    results = []
    for d in date:
        r = {}
        if 'value' in d:
            _from = dateutil.parser.parse(d['value'])
            r['from'] = _from
            r['to'] = _from
            results.append(r)
        elif 'from' in d:
            r['from'] = dateutil.parser.parse(d['from']['value'])
            r['to'] = dateutil.parser.parse(d['to']['value'])
            results.append(r)

    return results


def get_tz_from_location(location):
    g = geocoders.GoogleV3()
    _, (lat, lng) = g.geocode(location)
    tz = g.timezone((lat, lng))
    return tz


def convert_datetime(location, date=datetime.datetime.utcnow()):
    newtz = get_tz_from_location(location)
    oldtz = date.tzinfo
    oldtz_now = datetime.datetime.now(oldtz)
    date = date.replace(hour=oldtz_now.hour, minute=oldtz_now.minute, second=oldtz_now.second)
    date = date.astimezone(newtz)
    return date


def parse_simple_weather(data):
    weathers = []
    weather = {}
    weather['weather'] = data['weather'][0]['description']
    weather['main'] = data['main']
    weathers.append(weather)
    return weathers


def parse_weather(data, start, end):
    weathers = []
    for i in range(start, end):
        if i >= len(data['list']):
            break
        d = data['list'][i]
        weather = {}
        weather['weather'] = d['weather'][0]['description']
        main = {}
        main['temp'] = d['temp']['day']
        main['pressure'] = d['pressure']
        main['humidity'] = d['humidity']
        main['temp_min'] = d['temp']['min']
        main['temp_max'] = d['temp']['max']
        weather['main'] = main
        weathers.append(weather)
    return weathers


def get_weather(location, date):
    _now = datetime.datetime.now(tz=get_tz_from_location(location))
    days = date['to'].date() - _now.date()
    days2 = date['from'].date() - _now.date()
    url = ""
    if days.days == 0:
        url = ('http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=%s' % (location, weatherAPI))
    elif days.days > 0:
        url = ('http://api.openweathermap.org/data/2.5/forecast/daily?'
               'q=%s&units=metric&cnt=%d&appid=%s' % (location, days.days + 1, weatherAPI))
    else:
        return []
    r = requests.get(url)
    if days.days == 0:
        return parse_simple_weather(r.json())
    else:
        return parse_weather(r.json(), days2.days, days.days + 1)


def weather2string(weather):
    return (u'\nWeather: %s\nTemp: %s\u2103\nTemp_min: %s\u2103\nTemp_max: %s\u2103\nPressure: %s hPa\nHumidity: %s%%' %
            (weather['weather'], weather['main']['temp'],
             weather['main']['temp_min'],
             weather['main']['temp_max'],
             weather['main']['pressure'],
             weather['main']['humidity']))


def get_weather_info(session_id, context):
    context['result'] = "None"
    if 'location' not in context and 'datetime' not in context:
        say('', {}, 'Where and when would you like the forecast for?')
        return context
    if 'location' not in context:
        say('', {}, 'Where would you like the forecast for?')
        return context
    if 'datetime' not in context:
        say('', {}, 'When would you like the forecast for?')
        return context
    locations = context['location']
    dates = parse_datetime(context['datetime'])
    say('', {}, 'Please wait...')
    for loc in locations:
        for date in dates:
            date['from'] = convert_datetime(loc['value'], date['from'])
            date['to'] = convert_datetime(loc['value'], date['to'])
            weather = get_weather(loc['value'], date)
            if len(weather) > 0:
                for d in range(len(weather)):
                    say('', {}, ('The forecast for %s on %s is %s' %
                                 (loc['value'], (date['from'] + datetime.timedelta(days=d)).date().strftime('%B %d, %Y')
                                  , weather2string(weather[d]))))
                if len(weather) < (date['to'].date() - date['from'].date()).days + 1:
                    if len(weather) > 1:
                        say('', {}, 'Sorry, I can only get forecast up to %d days now' % len(weather))
                    else:
                        say('', {}, 'Sorry, I can only get forecast up to 1 day now')
            else:
                say('', {}, ('I cannot get forecast for %s' % loc['value']))
    context = {}
    say(None, None, 'Would you like the forecast for other location?')
    return context

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'get_weather_info': get_weather_info,
    }

if __name__ == '__main__':
    bot = Wit(access_token, actions)
    msg = ''
    context = {}
    print 'Tip: enter \'end\' to exit..ahihi'
    while True:
        msg = raw_input(">> You: ")
        if msg == 'end':
            break
        context = bot.run_actions(session_id, msg, context)

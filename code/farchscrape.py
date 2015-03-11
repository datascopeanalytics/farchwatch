import sys
import json

import pprint; pp = pprint.PrettyPrinter()
import requests

CONDITIONS_KEY = {
    'Clear': 3,
    'Sunny': 3,
    'Mostly Sunny': 3,
    'Partly Cloudy': 3,
    'Mostly Cloudy': 2,
    'Cloudy': 2,
    'Fog': 2,
    'Hazy': 2,
    'Partly Sunny': 2,
    'Overcast': 2,
    'Chance of': 1,
    'Flurries': 1,
    'Sleet':1,
    'Snow': 1,
    'Thunderstorms': 1,
    'Tstorms': 1,
    'T-storms': 1,
}

def get_yesterday():
    r = requests.get("http://api.wunderground.com/api/1498e6b240ba15f0/yesterday/q/IL/Chicago.json")
    data = r.json()


    yesterday = data['history']['dailysummary'][0]

    datapoint = {}

    # mapping NOAA to Wunderground
    datapoint["TMIN"] = float(yesterday["mintempi"])
    datapoint["TMAX"] = float(yesterday["maxtempi"])
    datapoint["SNOW"] = float(yesterday["snowfallm"])
    datapoint["RAIN"] = float(yesterday["rain"])
    datapoint["month"] = float(yesterday["date"]['mon'])
    datapoint["FOG"] = float(yesterday["fog"])
    datapoint["AWND"] = float(yesterday["meanwindspdm"])
    datapoint["year"] = int(yesterday["date"]['year'])
    datapoint["DATE"] = "-".join([yesterday["date"]['year'],
                                  yesterday["date"]['mon'],
                                  yesterday["date"]['mday']])
    datapoint["PRCP"] = float(yesterday["precipm"])*10
    datapoint["day"] = int(yesterday["date"]["mday"])

    pp.pprint(datapoint)

    # not gettable from Wunderground
    # "MIST" -> N/A
    # "is_nice" -> generated
    # "not_over" -> generated
    # "ADVERSE" -> N/A
    # "HAZE" 0, ->  N/A

    # TODO.. we need to do something with that datapoint

def get_forecast():
    r = requests.get("http://api.wunderground.com/api/1498e6b240ba15f0/forecast10day/q/IL/Chicago.json")
    data = r.json()
    # pp.pprint(data)
    forecast = []
    
    # this is a 10 day list of days
    for day in data['forecast']['simpleforecast']['forecastday']:
        datapoint = {}
        #potentially relevant fields:
        datapoint['weekday'] = day["date"]["weekday_short"]
        datapoint['date'] = day["date"]["day"]
        datapoint['month'] = int(day["date"]["month"])
        datapoint['year'] = int(day["date"]["year"])
        datapoint['high'] = float(day["high"]["fahrenheit"])
        datapoint['low'] = float(day["low"]["fahrenheit"])
        datapoint['snow'] = float(day["snow_allday"]["in"])
        datapoint['conditions'] = day["conditions"]
        datapoint['icon'] = day["icon"]
        datapoint['icon_url'] = day["icon_url"]
        datapoint['precip_prob'] = day["pop"] # -> probability of precipitation
        datapoint['precip'] = float(day["qpf_allday"]["in"])
        # pp.pprint(datapoint)

        #TODO.. we also need to do something with these datapoints
        datapoint['outlook'] = rate_datapoint(datapoint)


        forecast.append(datapoint)
    return forecast


def rate_datapoint(datapoint):
    high = datapoint['high']
    conditions = enumerate_conditions(datapoint['conditions'])

    if not conditions: 
        return 'FAIL'

    if high < 33:
        if conditions < 2:
            return 'ZOMG'
        elif conditions < 3: 
            return 'UGH'
        else:
            return 'BRR'

    elif high < 50:
        if conditions < 2: 
            return 'YUCK'
        elif conditions < 3:
            return 'UGH'
        else:
            return 'MEH'

    elif high < 60:
        if conditions < 2:
            return 'UGH'
        elif conditions < 3:
            return 'MEH'
        else:
            return 'AIGHT'
            
    else:
        if conditions < 2:
            return 'MEH'
        elif conditions < 3:
            return 'AIGHT'
        else:
            return 'NICE!'

def enumerate_conditions(cond):
    if cond.startswith('Chance of'):
        cond = 'Chance of'
    
    try:
        conditions = CONDITIONS_KEY[cond]
    except KeyError: 
        print >> sys.stderr, '"%s" not found, returning FAIL' % cond
        conditions = 0

    return conditions


forecast = get_forecast()
with open('../web/app/assets/forecast.json','w') as outfile:
    json.dump(forecast,outfile)




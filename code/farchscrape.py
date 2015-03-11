import requests
import pprint; pp = pprint.PrettyPrinter()
import json

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
        datapoint['day'] = int(day["date"]["day"])
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
        
        forecast.append(datapoint)
    return forecast

forecast = get_forecast()
with open('../web/app/assets/forecast.json','w') as outfile:
    json.dump(forecast,outfile)

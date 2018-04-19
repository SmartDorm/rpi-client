import urllib.request
import json
import pprint as pp

def getWeather():
    api_key = "ec6468538fccd2f63913d50b7ff81834"
    # base_url = "http://api.openweathermap.org/data/2.5/forecast?id=4928096&APPID="
    base_url = "http://api.openweathermap.org/data/2.5/weather?id=4928096&units=imperial&APPID="
    city_id = str(4928096)
    full_url = base_url + api_key
    weather = urllib.request.urlopen(full_url)
    out = weather.read().decode('utf-8')

    weather_dict = json.loads(out)
    weather.close()

    return weather_dict

if __name__ == "__main__":
    out = getWeather()
    temp = out.get('main').get('temp')
    condition = out['weather'][0]['main']
    pp.pprint(temp)
    pp.pprint(condition)

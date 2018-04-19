import urllib.request
import json
import requests
import random
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

def createResultString(response_dict):
    high = str(response_dict.get('main').get('temp_max'))
    low = str(response_dict.get('main').get('temp_min'))
    current = str(response_dict.get('main').get('temp'))
    conditions = response_dict['weather'][0]['main']

    return high + "," + low + "," + current + "," + conditions

def getNews():
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=us&'
           'apiKey=a8fc51c4713b4112973d8b577bc5e694')

    response = requests.get(url)
    parsed = json.loads(response.text)

    titles = []

    for i in parsed.get("articles"):
        titles.append(i.get("title"))

    return titles

if __name__ == "__main__":
    # out = getWeather()
    # temp = out.get('main').get('temp')
    # condition = out['weather'][0]['main']
    # max = out.get('main').get('temp_max')
    # min = out.get('main').get('temp_min')

    print(random.choice(getNews()))
    # print(createResultString(getWeather()))

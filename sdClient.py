# -*- coding: ASCII -*p
import urllib.request
import json
import requests
import random
import serial
import pprint as pp
import datetime
from time import sleep

class Client:
    def __init__(self):
        self.err = "ERR\n"
        self.rtc = datetime.datetime.now()
        self.port = serial.Serial(
            port = '/dev/serial0',
            baudrate = 115200,
            timeout = None,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE
        )
        if(not self.port.isOpen()):
            self.port.open()
        
        #self.weather = "60,65,55,Cloudy";
        #self.orig = ["Trump gives birth", "Trump gives birth again, except this time in 3D"]
        #self.headlines = [x for x in self.orig if len(x) < 25]
        try:
            self.weather = getWeather();
            self.headlines = getNews();
            self.headlines = [x for x in self.headlines if len(x) <= 60]
            print(self.headlines)
            self.updated = False
        except:
            self.write_serial(self.err)
            print("Error caught!")


    def update(self):
        curr = datetime.datetime.now()
        if (curr - self.rtc).total_seconds() >= 600: # 10 minutes
            self.rtc = curr
            self.weather = getWeather()
            tmp = getNews()
            self.headlines = getNews()
            print("Updated.")

    def write_serial(self, data_string):
        self.port.write(data_string.encode())
        self.port.write("\0".encode())


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

    return createResultString(weather_dict)

def createResultString(response_dict):
    high = str(int(response_dict.get('main').get('temp_max')))
    low = str(int(response_dict.get('main').get('temp_min')))
    current = str(int(response_dict.get('main').get('temp')))
    conditions = response_dict['weather'][0]['main']

    return current + "," + high + "," + low + "," + conditions

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

def main_loop(client):
    while(True):
        control_word = client.port.read(4)
        print(control_word)
        print(control_word == b'UPDT')
        sleep(.1)
        client.port.flush()
        if control_word == b'UPDT':
            try:
                client.write_serial(client.weather + ',' + client.headlines[-1])
                print(client.weather + ',' + client.headlines[-1])
                print("Data fetched")
                client.headlines.pop()
            except IndexError:
                client.write_serial(client.weather + ',' + "I hope you're having a great day!")
        
        if control_word == b'TIME':
            client.write_serial(client.rtc.strftime("%Y,%m,%d,%H,%M,%S"))
            sleep(.1)
            client.port.flush()
            print("Time written.")

        if str(control_word) == 'MUSC':
            subprocess.run(['play', 'temp.wav'])

        sleep(.1)
        client.port.flush()
        client.update()






def init():
    client = Client()
    return client


if __name__ == "__main__":
    # out = getWeather()
    # temp = out.get('main').get('temp')
    # condition = out['weather'][0]['main']
    # max = out.get('main').get('temp_max')
    # min = out.get('main').get('temp_min')
    # uart_setup()
    # print(random.choice(getNews()))
    # print(createResultString(getWeather()))
    main_loop(init())

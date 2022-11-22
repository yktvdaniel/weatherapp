from flask import Flask, render_template, request
import requests
import configparser
import time
import math
from datetime import datetime
from app.models import db


app = Flask(__name__)

app.config.from_object('config')
db.init_app(app)
db.create_all()
app.debug = True


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = get_api_key()
    if temp_units == 'F':
        data = get_weather_results_imperial(zip_code, api_key)
    else:
        data = get_weather_results_metric(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = f"{data['main']['feels_like']:.2f}"
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data["weather"][0]["icon"]
    icon_url = "http://openweathermap.org/img/w/" + icon + ".png"
    timestamp = 1661261478
    dt_obj = datetime.fromtimestamp(timestamp)
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    timestamp = int(data["timezone"]) + math.floor(time.time())
    print(timestamp)
    dt_obj = datetime.utcfromtimestamp(timestamp)
    local = datetime.fromtimestamp(math.floor(time.time()))
    return render_template('result.html',
                           location=location, temp=temp, dt_obj=dt_obj, temp_min=temp_min, temp_max=temp_max,
                           feels_like=feels_like, weather=weather, icon_url=icon_url, local_time=local)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


print(get_weather_results_imperial("95129", get_api_key()))
print(get_weather_results_metric("95129", get_api_key()))

if __name__ == '__main__':	app.run()
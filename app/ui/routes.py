from flask import Blueprint, render_template, request, redirect
from datetime import datetime
import time
import math
import requests
from app.models import db, Result



ui_bp = Blueprint(
   'ui_bp', __name__,
   template_folder='templates',
   static_folder='static'
)


@ui_bp.route('/')
def home():
   return render_template("home.html")


@ui_bp.route('/upload', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    temp_units = request.form['temp_units']
    api_key = '10da3e474eefe39b2c7629a7da529c6e'
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
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    created = datetime.now()
    created = datetime.timestamp(created)
    created_url = '<a href="/result/' + str(created) + '">' + str(created) + '</a>'
    result = Result(location=location, temp=temp, feels_like=feels_like, timestamp=timestamp, icon_url=icon_url,
        weather=weather, temp_min=temp_min, temp_max=temp_max, created=created, created_url=created_url)
    db.session.add(result)
    db.session.commit()
    return redirect('/results')


@ui_bp.route('/card', methods=['POST'])
def render_card():
    return render_template('result.html')



def get_weather_results_imperial(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

def get_weather_results_metric(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


@ui_bp.route('/results', methods=['POST', 'GET'])
def list_results():
    results = Result.query
    return render_template('results.html', results=results)


@ui_bp.route('/api/results')
def results_all():
    return {'data': [result.to_dict() for result in Result.query]}


@ui_bp.route('/result/<dt>', methods=['POST', 'GET'])
def list_result(dt):
    created = 1667868084.097243
    print(created)
    result = Result.query.filter_by(created=dt)
    print(result)
    return render_template('result.html', result=result)

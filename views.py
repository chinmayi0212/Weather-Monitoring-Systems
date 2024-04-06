from django.shortcuts import render
from datetime import date,datetime
import json
import requests
import geocoder
import calendar
import socket

apikey = "29a585ea1cd34b1aa8b82100210212"
baseurl = "http://api.weatherapi.com/v1/forecast.json"

def current_location():

	city = "Pune"
	
	return city

def todaydate():
	
	curr_date = date.today()
	day = calendar.day_name[curr_date.weekday()]
	day_name = day[0:3]

	#month name
	month_name = datetime.now()
	month_name = month_name.strftime('%b')

	return day_name,month_name

def data_request(request):
	if request.method == "POST":
		city = request.POST.get("city")
	else:
		city = current_location()
	
	api_request = requests.get(baseurl+'?'+'key='+apikey+'&q='+city+'&aqi=yes&days=10')
	api = json.loads(api_request.content)

	
	return api

def home(request):
	api = data_request(request)
	day_name,month_name = todaydate()
	context={}
	#try:
	city1 = api['location']['name']
	country = api['location']['country']
	weather_condition = api['current']['condition']['text']
	temp_today = api['current']['temp_c']
	image = api['current']['condition']['icon']
	time = api['location']['localtime']
	date = api['location']['localtime'][9:10]
	hours =  api['forecast']['forecastday'][0]['hour']
	hours_de = api['forecast']['forecastday'][0]['hour'][14]['time']
	real_feel = api['current']['feelslike_c']
	humidity = api['current']['humidity']
	chance_of_rain = api['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
	sunrise_time = api['forecast']['forecastday'][1]['astro']['sunrise']
	sunset_time = api['forecast']['forecastday'][1]['astro']['sunset']
	pressure = api['current']['pressure_mb'] 
	wind_speed = api['current']['wind_kph']
	uv_index = api['forecast']['forecastday'][0]['day']['uv']
	wind_direction = api['current']['wind_dir']
	aftedate = api['forecast']['forecastday'][1]['date']


	hello_list = []
	time1_list = []
	temp1_list = []
	image1_list = []

	split_time = time.split(" ")
	new_time = split_time[1]
	split_time = split_time[1].split(":")
	count = int(split_time[0])
	for i in range(0,15):
		count = count + 1

		for j in range(0, len(hours)):

			if(count <= 24 and count == j):
				time1 = api['forecast']['forecastday'][0]['hour'][j]['time']
				image1 = api['forecast']['forecastday'][0]['hour'][j]['condition']['icon']
				temp1 = api['forecast']['forecastday'][0]['hour'][j]['temp_c']

				time1 = time1[11:16]
				time1_list.append(time1)
				image1_list.append(image1)
				temp1_list.append(int(temp1))

		if(count == 24):
			time1 = api['forecast']['forecastday'][0]['hour'][0]['time']
			image1 = api['forecast']['forecastday'][0]['hour'][0]['condition']['icon']
			temp1 = api['forecast']['forecastday'][0]['hour'][0]['temp_c']

			time1 = time1[11:16]
			time1_list.append(time1)
			image1_list.append(image1)
			temp1_list.append(int(temp1))

			count = 0
		for x in zip(time1_list,image1_list,temp1_list):
			pass

		hello_list.append(x)

	context = {
		'city' : city1,
		'coun' : country,
		'cond' : weather_condition,
		'temp' : int(temp_today),
		'imag' : image,
		'time' : new_time,
		'days' : day_name,
		'mont' : month_name,
		'date' : date,
		'real_feel' : real_feel,		
		'humidity' : humidity,
		'rain' : chance_of_rain,
		'sunrise' : sunrise_time,
		'sunset' : sunset_time,
		'pressure' : int(pressure),
		'wind' : wind_speed,
		'uv' : uv_index,
		'wind_dir' : wind_direction,
		'hello_list' : hello_list,

	}

	return render(request, 'home.html', context)
	"""except:
		return render(request, 'invalidInput.html', context)
"""


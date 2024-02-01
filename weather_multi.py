'''adds n-number of weather records from randomly selected cities.


education purpose: call API, fetch results, adjust the results [fahrenheit()] and save results to datbase. Do this in a loop

'''

import requests 
import json 
from datetime import datetime, timedelta

import sqlite3
import random 
import argparse
import os


weather_token = "e9477384bab5d142650dd34f045ba4b0"

# Get the absolute path to the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))


# Specify the absolute path to the SQLite database file
database_path = os.path.join(script_directory, '/Users/cellis/craig_weather/weather.db')

parser = argparse.ArgumentParser(description = 'simple python script')
parser.add_argument('num')
args = parser.parse_args()


connection = sqlite3.connect(database_path)
cursor = connection.cursor()


def get_local_datetime(dt,offset):

	utc_dt = datetime.utcfromtimestamp(dt)
	local_dt = utc_dt + timedelta(seconds=offset)

	return local_dt 


def get_weather(lat,lon):

	weather_api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_token}"
	response = requests.get(weather_api)

	if response.status_code == 200: 
		data = response.json()

		name = data['name']

		weather_info = data['weather']
		weather_main = weather_info[0]['main']
		weather_desc = weather_info[0]['description']	

		temp = fahrenheit(data['main']['temp'])
		feels_like = fahrenheit(data['main']['feels_like'])

		wind_speed = data['wind']['speed']


		timezone_offset = data['timezone']
		local_sunrise = get_local_datetime(data['sys']['sunrise'],timezone_offset).strftime('%H:%M:%S')
		local_sunset = get_local_datetime(data['sys']['sunset'],timezone_offset).strftime('%H:%M:%S')
		local_dt = get_local_datetime(data['dt'],timezone_offset).strftime("%Y-%m-%d %H:%M:%S")

		return name, local_dt, weather_main, weather_desc, temp, feels_like, wind_speed, local_sunrise, local_sunset


	else: 
		print("there was an error.")



	return 

def fahrenheit(kelvin):
    # Conversion formula
    fahrenheit = round((kelvin - 273.15) * 9/5 + 32,2) 
    return fahrenheit

def random_city():

	sql_query = "SELECT MAX(city_id) FROM cities" 
	cursor.execute(sql_query)

	result = cursor.fetchone()
	max_id = result[0] if result is not None else None

	selected_id =  random.randint(1, max_id)

	print(f"selected city id {selected_id} from a max number of {max_id}")

	return selected_id


def get_location(city_id): 

	sql_query = f"SELECT city,state,latitude,longitude FROM cities WHERE city_id = {city_id}"
	cursor.execute(sql_query)
	select_city = cursor.fetchone()

	if select_city is not None:
		city, state, lat, lon = select_city

		return city, state, lat, lon 

	else:
		print("No city found for the random ID.")	


def insert_data(data):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
    	INSERT INTO weather_data (city_id, name, datetime, weather_main, weather_desc, temp, temp_feels,wind_speed, sunrise, sunset)
    	VALUES (?,?,?,?,?,?,?,?,?,?)
    ''', data)


    conn.commit()
    conn.close()

    return 

if __name__ == "__main__":

	quantity = int(args.num)

	if quantity <= 10: 
		print(f"Checking {quantity} locations for weather and adding to the database.")

		for _ in range (quantity):

			selected_id = random_city()
			city, state, lat, lon = get_location(selected_id)

			print("----------------")
			print(f"Checking weather for {city}, {state}")
			
			name, local_dt, weather_main, weather_desc, temp, feels_like, wind_speed, local_sunrise, local_sunset = get_weather(lat,lon)
			add_weather_db = (selected_id, name, local_dt,weather_main, weather_desc, temp, feels_like, wind_speed, local_sunrise, local_sunset)

			insert_data(add_weather_db)


			# Print the result
			print(f'Local City name: {name}')
			print(f'Weather report for date/time: {local_dt}')
			print(f'Weather: {weather_main}')
			print(f'Weather Details: {weather_desc}')
			print(f'Temperature: {temp} F')
			print(f'Feels Like: {feels_like} F')
			print(f'Wind Speed: {wind_speed} meters/sec')
			print(f'Sunrise: {local_sunrise}')
			print(f'Sunset: {local_sunset}')
			print(f'city id: {selected_id}')
			print("----------------")
			print()

	else: 

		print("that is too many.  Please enter a number 10 or less")



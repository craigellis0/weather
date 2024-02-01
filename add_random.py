'''selects 1 random city and add its to the cities table. 
use: python add_random.py 

Educational project: Randomly select a city based on zip code, make a simple API call, parse results, and save to a database.
'''

import requests
import json
import random 
import sqlite3 
import os
import sys
from dotenv import load_dotenv

load_dotenv()


zip_header = json.loads(os.getenv("zipcode_stack_apikey"))
weather_apikey = os.getenv("weather_stack_apikey")
sqlite3_url = os.path.join(os.getenv("sqlite3_path"), "weather.db")

# Get the absolute path to the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the absolute path to the SQLite database file
database_path = os.path.join(script_directory, sqlite3_url) #using absolute path so script can be called from Jenkins. 


def get_city():

	while True: 
		code = ("00" + str(random.randint(501,99949)))[-5:]
		url = f"http://api.zipcodestack.com/v1/search?codes={code}&country=us"

		response = requests.get(url,headers=zip_header)
		body = json.loads(response.text)
		response_data = body["results"]
		if response_data: 
			str_code = str(code)
			city = response_data[str_code][0]["city"]
			state = response_data[str_code][0]["state_en"]
			return city, state, str_code


def get_coords(zip_code): 

	geo_url = f"https://api.openweathermap.org/geo/1.0/zip?zip={zip_code},US&appid={weather_apikey}"

	response = requests.get(geo_url)

	if response.status_code == 200: 
		data = response.json()

		lat = data.get('lat')
		lon = data.get('lon')
	else:
		print(f'Error: {response.status_code}')

	return lat,lon 


def insert_data(data):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
    	INSERT INTO cities (city,state,zip,longitude,latitude)
    	VALUES (?,?,?,?,?)
    ''', data)

    conn.commit()
    conn.close()

    return 

print("looking up a valid random city.")
city,state,zip_code = get_city()
lat, lon = get_coords(zip_code)

print(f"{city}, {state} {zip_code} Latitude: {lat}  Longitude: {lon}")

new_city = (city,state,zip_code,lon,lat)
print(new_city)

insert_data(new_city)

print("end of script.")







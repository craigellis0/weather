'''This script will add n number of random cities to the cities table in the weather.db 
use: python city_multi.py n 

education purpose: project to take a parameter via command line, call an API in loop, parse results and save to database. 
'''

import requests
import json
import random 
import sqlite3 
import argparse
import sys

zip_header = {"apikey": "01HD7K9J8AANVHCEHZ2JJR9YXV"}

parser = argparse.ArgumentParser(description = 'simple python script')
parser.add_argument('num')
args = parser.parse_args()



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

	geo_url = f"https://api.openweathermap.org/geo/1.0/zip?zip={zip_code},US&appid=e9477384bab5d142650dd34f045ba4b0"

	response = requests.get(geo_url)

	if response.status_code == 200: 
		data = response.json()

		lat = data.get('lat')
		lon = data.get('lon')
	else:
		print(f'Error: {response.status_code}')

	return lat,lon 


def insert_data(data):
    conn = sqlite3.connect('/Users/cellis/craig_weather/weather.db')
    cursor = conn.cursor()

    cursor.execute('''
    	INSERT INTO cities (city,state,zip,longitude,latitude)
    	VALUES (?,?,?,?,?)
    ''', data)

    conn.commit()
    conn.close()

    return 



if __name__ == "__main__":

	quantity = int(args.num)

	if quantity <= 25: 

		print(f"Adding {quantity} locations to the database.")

		for _ in range(quantity+1):

			city,state,zip_code = get_city()
			lat, lon = get_coords(zip_code)
			print(f"{city}, {state} {zip_code} Latitude: {lat}  Longitude: {lon}")
			new_city = (city,state,zip_code,lon,lat)
			insert_data(new_city)

		sys.exit()

	else: 
		print("that is too many.  Please enter a number 25 or less.")
		sys.exit()











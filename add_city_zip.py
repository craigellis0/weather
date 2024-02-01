'''
takes zip code for a known city and adds details to the cities table. 
use: python add_city_zip.py 12345

education purpose: project to call an external API, fetch results, parse those results and then save to a database for future use. 
'''

import requests
import json
import sqlite3
import argparse 
import os
from dotenv import load_dotenv

load_dotenv() # load environment variables

zip_header = json.loads(os.getenv("zipcode_stack_apikey"))

parser = argparse.ArgumentParser(description = 'simple python script')
parser.add_argument('zip_code')
args = parser.parse_args()


def get_city(zip_code):

	while True: 
		
		url = f"http://api.zipcodestack.com/v1/search?codes={zip_code}&country=us"

		response = requests.get(url,headers=zip_header)
		body = json.loads(response.text)
		response_data = body["results"]
		if response_data: 
			str_code = str(zip_code)
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
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()

    cursor.execute('''
    	INSERT INTO cities (city,state,zip,longitude,latitude)
    	VALUES (?,?,?,?,?)
    ''', data)

    conn.commit()
    conn.close()

    return 


if __name__ == "__main__":

	zip_code = args.zip_code

	city,state,zip_code = get_city(zip_code)
	lat, lon = get_coords(zip_code)

	new_city = (city,state,zip_code,lon,lat)
	print(new_city)

	insert_data(new_city)









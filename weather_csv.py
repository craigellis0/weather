''' randomly select n number (defined by requested_entries) from the weather_data table and save as CSV file 
use: python weather_csv.py 

education purpose: This script was created as a mini project to confirm I can select some items from a datbase, and then do 
something with it.  In this case, save the SQL query results to as CSV file. 
'''

import sqlite3
import csv
import datetime
import sys

# Connect to the SQLite database
db_connection = sqlite3.connect('weather.db')
cursor = db_connection.cursor()


requested_entries = 10

def filename():
    return f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv" # create filename based on current date/time to preven over writing. 

def get_max(): 
    return cursor.execute("SELECT MAX(weather_id) FROM weather_data").fetchone()[0]   

def create_sql(num):

    # Execute your SQL query
    sql_query = """
        SELECT
            cities.city,
            cities.state,
            cities.zip,
            weather_data.name,
            weather_data.datetime,
            weather_data.weather_main,
            weather_data.temp,
            weather_data.wind_speed,
            weather_data.sunrise
        FROM
            weather_data
        JOIN
            cities ON weather_data.city_id = cities.city_id
        WHERE 
            weather_data.weather_id > {};
    """.format(num)

    return sql_query

low_num = get_max() - requested_entries
new_sql = create_sql(low_num)
print (new_sql)

cursor.execute(new_sql)

# Fetch all the results
results = cursor.fetchall()

# Close the database connection
db_connection.close()

# Specify the CSV file name
csv_file_name = f"output/{filename()}"

# Write the results to a CSV file
with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header (column names)
    column_names = [
        'City', 'State', 'ZIP', 'Name', 'Datetime', 
        'Weather Main', 'Temperature', 'Wind Speed', 'Sunrise'
    ]
    csv_writer.writerow(column_names)
    
    # Write the data rows
    csv_writer.writerows(results)


print(f"Weather data for {requested_entries} have been successfully exported to {csv_file_name}.")




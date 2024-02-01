''' randomly select n number (defined by requested_entries) from the weather_data table and SFTPs it elsewhere 

Educational project: select stuff from a database, save as a CSV file and send the results via SFTP to remote location. 

'''

import sqlite3
import csv
import datetime
import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

SFTP_HOST = os.getenv("sftp_host")
SFTP_USER = os.getenv("sftp_user")
SFTP_PASSWORD = os.getenv("sftp_password")


# Get the absolute path to the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

print(script_directory)


# Specify the absolute path to the SQLite database file
database_path = os.path.join(script_directory, '/Users/cellis/craig_weather/weather.db')


# Connect to the SQLite database
db_connection = sqlite3.connect(database_path)
cursor = db_connection.cursor()

requested_entries = 15

def sftp_details(filename):
    connection_details = {
        'hostname': SFTP_HOST,
        'port': 22,
        'username': SFTP_USER,
        'password': SFTP_PASSWORD,
        'remote_file_path': f'remote/{filename}',
    }
    return connection_details


def filename():
    return f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

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
# ---------------------------------

# def values for sql query 
low_num = get_max() - requested_entries
new_sql = create_sql(low_num)

# make request
cursor.execute(new_sql)

# Fetch all the results
results = cursor.fetchall()

# Close the database connection
db_connection.close()

fn = filename()
connection_details = sftp_details(fn)


# Create an SFTP session
transport = paramiko.Transport((connection_details['hostname'], connection_details['port']))
transport.connect(username=connection_details['username'], password=connection_details['password'])
sftp = paramiko.SFTPClient.from_transport(transport)

# Open a remote file for writing
with sftp.file(connection_details['remote_file_path'], 'w') as remote_file:
    for row in results:
        row_str = ','.join(str(element) for element in row)
        remote_file.write(row_str + '\n')


print(f"Weather data for {requested_entries} locations have been successfully sent via FTP to {connection_details['remote_file_path']}.")




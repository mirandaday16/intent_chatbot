# This file is used to get time zone data for the user
# Using Amdoren API: https://www.amdoren.com/time-zone-api/

import requests
import json

api_key = "vGSiWG7aTLBXuL2W9hPbxMU94u9Vb5"
base_url = "https://www.amdoren.com/api/timezone.php"


# Takes a string entered by the user and converts it into a usable format for the API call
def get_location_code(location):
    code = location.replace(" ", "+")
    return code


# Converts military time and date to more readable format
# Example of API timestamp result:"2016-11-04 23:18:46"
def convert_time_format(timestamp):
    # remove date and seconds
    time = timestamp[11:16]
    # check for military time (PM)
    if time[:1] > 12:
        hour = time[:1]
        converted_hour = int(hour) - 12
        minutes = time[1:]
        new_time = str(converted_hour) + minutes + " PM"
    else:
        new_time = time + " AM"
    return new_time


# Gets local time in user-entered location using API
# Location should be a city
def get_time(location):
    location_code = get_location_code(location)
    complete_url = base_url + "?key=" + api_key + "&format=xml&by=zone&zone=" + location_code
    response = requests.get(complete_url)
    # JSON method of response object
    x = response.json()
    if x["error"] == "0":
    # store time data
    time = x["time"]
    converted_time = convert_time_format(time)
    response = "Right now in " + location.capitalize() + " it is " + converted_time + "."
# This file is used to get weather data for the user
# Using OpenWeather API: https://openweathermap.org/

import requests
import json

api_key = "4b6a47117e2d2f39c4bc2ef32ae03abc"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather(location):
    complete_url = base_url + "appid=" + api_key + "&q=" + location
    response = requests.get(complete_url)
    # JSON method of response object
    x = response.json()
    # Check x nested list of dictionaries; 404 means city found
    if x["cod"] != "404":
        # store temp data in new variable y
        y = x["main"]
        current_temp_kelvin = y["temp"]
        # convert Kelvin temperature to Fahrenheit
        current_temp = str(round((current_temp_kelvin * 9 / 5) - 459.67))
        current_humidity = str(y["humidity"])
        # store weather data in new variable z
        z = x["weather"]
        description = z[0]["description"]
        reply = "Right now in " + location.capitalize() + ", the weather is " + description +\
                " with a temperature of " + current_temp + "°F and " +\
                current_humidity + "% humidity."
    else:
        reply = "Sorry, I couldn't find the weather for that location."
    return reply

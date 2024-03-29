#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
from core.concepts.Domain import Domain 
# Import meteo France API.
from meteofrance_api import MeteoFranceClient
# Import logging library
import logging
#
#
#
class Weather(Domain):
  
    def __init__(self):

        """ Class constructor. """
            
        # Init parent class Domain.
        super().__init__()

        # Initialisation.

        # Init client
        self.client = MeteoFranceClient()

    @Domain.match_intent("weather.daily")
    def daily(self, city=None, day_diff=None):

        """ Get today weather via meteofrance api. """

        # If city is not defined.
        if city == None or city == "":
            # Set default city.
            city = self.config["weather"]["default_city"]

        # If day_diff is not defined.
        if day_diff == None or day_diff == "" or day_diff == "0":
            # Set default city.
            day_diff = "0"
            day_diff_int = 0
        else:
            # Convert day_diff to integer.
            day_diff_int = int(day_diff)

        # Search a location from name.
        list_places = self.client.search_places(city)
        my_place = list_places[0]

        # Fetch weather forecast for the location
        weather = self.client.get_forecast_for_place(my_place)

        # Get the daily forecast
        day_weather = weather.daily_forecast[day_diff_int]

        # Get slots values.
        day_name = self.get_slot(day_diff)
        
        # Check if day_weather defined.
        if "weather12H" in day_weather :
            # Return weather.daily dialog response.
            return self.say(
                "weather.daily",
                city=city.title(), 
                day_name=day_name, 
                weather_desc=day_weather['weather12H']['desc'].lower(),
                temp_min=day_weather['T']['min'],
                temp_max=day_weather['T']['max'],
            )
        else:
            # Return weather.not_found dialog response.
            return self.say(
                "weather.not_found",
                city=city.title(), 
                day_name=day_name, 
            )

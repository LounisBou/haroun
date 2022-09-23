#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
from core.concepts.Domain import Domain 
# Import meteo France API.
from meteofrance_api import MeteoFranceClient
from meteofrance_api.helpers import readeable_phenomenoms_dict
# [DEBUG] Import pretty formatter.
from prettyformatter import pprint
#
#
# Domain globals : 
#
# Needed slots list.
SLOTS_FILES = [
  "city",
  "day_diff",
]
#
#
# ! DOMAIN 
#
class Weather(Domain):
  
    def __init__(self):

        """ Class constructor. """
            
        # Init parent class Domain.
        super().__init__()

        # Initialisation.

        # Load config file.
        #self.load_config()

        # Load dialogs file.
        self.load_dialogs()

        # Retrieve needed slots.
        self.get_slots_entries(SLOTS_FILES)

        # Init client
        self.client = MeteoFranceClient()

    @Domain.match_intent("weather.daily")
    def daily(self, city=None, day_diff=None):

        """ Get today weather via meteofrance api. """

        # If city is not defined.
        if city == None or city == "":
            # Set default city.
            city = "Lille"

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
        
        # [DEBUG]
        #print(f"slots_entries : ")
        #pprint(self.slots_entries)

        # Get slots values.
        day_name = self.slots_entries[day_diff]

        # [DEBUG]
        #print("day_weather dict : ")
        #pprint(day_weather)
        
        # Get weather.daily dialog response.
        #dialog = self.get_dialog("weather.daily")

        # Create response.
        response = f"""
            Voici la météo pour {city.title()} {day_name} : 
            La journée sera {day_weather['weather12H']['desc'].lower()} 
            avec des températures comprises entre {day_weather['T']['min']} et {day_weather['T']['max']} degrés. 
        """

        # Return daily forecast.
        return response

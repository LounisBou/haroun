#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Random library import.
import random
# Import core concept domain.
from core.concepts.Domain import Domain 
# Import core concept skill.
from core.concepts.Skill import Skill 
#
#
# Domain statics attributs : 
#
# Openhab API connection infos.
OPENHAB_IP = "192.168.0.115"
OPENHAB_PORT = "8080"
OPENHAB_API_URL = "https://"+OPENHAB_IP+":"+OPENHAB_PORT
OPENHAB_API_VERSION = "1"
OPENHAB_VERSION = "3"

# Languages dictionnary.
LANGUAGES = {}

# Openhab language code.
LANG_CODE = 'fr'

# Define french language.
LANGUAGES['fr'] = {
  "WHAT_ROOM_ITEM_INFO" : [
    "Ok mais dans quelle pièce souhaitez-vous connaitre {item_type_lang} ?",
    "Très bien je veux bien vous donner {item_type_lang} mais de quelle pièce ?",
  ],
  "WHAT_ROOM_ITEM_ACTION" : [
    "Ok mais dans quelle pièce souhaitez-vous modifier {item_type_lang} ?",
    "Très bien je veux bien modifier {item_type_lang} mais de quelle pièce ?",
  ],
  "TEMPERATURE" : "la température",
  "BRIGHTNESS" : "la luminosité",
  "LIGHT" : "la lumière",
  "BLIND" : "le volet roulant",
  "DOOR" : "la porte",
  "WINDOW" : "la fenetre",
  "HUMIDITY" : "l'humidité",
  "WATER_LEAK" : "l'inondation",
  "HEATER" : "le chauffage",
  "PRESSURE" : "la pression",
  "THERMOSTAT" : "le thermostat"
}
#
#
# ! DOMAIN 
#
class Openhab:
  
  def __init__(self):
    
    """ 
      __init__ : Domain constructor.      
    """
    
    return None
    
  def __get_lang(self, lang_entry_code):
    
    """ 
      __get_lang : Get language string by code. Provide random string if code entry value is list.
      ---
      Parameters 
        lang_entry_code : String
          Language entry code.
      ---
      Return String
        Language string.
    """
    
    # Get current language entry code value.
    lang_entry_value = LANGUAGES[LANG_CODE][lang_entry_code]
    
    # If language entry value is list.
    if type(lang_entry_value) == list :
      # Return random value.
      return random.choice(lang_entry_value)
    else:
      # Return value.
      return lang_entry_value
    
  
  @Skill.match_intent("openhab.question")
  def question(self, item_type, room = None, value = None, question_trigger = None, orphan = None):
  	
    """ 
      Answer to Openhab item state question.
      ---
      Parameters
        item : String
          Openhab item type
        room : String (optionnal)
          Openhab sitemap room
        Value : String (optionnal)
          Openhab current item value to check.
        question_trigger : String (optionnal)
          Part of the sentence that indicate question interrogation form.
    """
    
    # Get item type lang.
    item_type_lang = self.__get_lang(item_type)
    
    # Check if room not provide.
    if not room :
      # Ask for room information.
      return self.__get_lang("WHAT_ROOM_ITEM_INFO").format(**locals(), **globals())
      
    # Return response. 
    return f"Call 'Openhab' method 'question' with params : item_type='{item_type}', room='{room}', value='{value}', question_trigger='{question_trigger}'"
  
  @Skill.match_intent("openhab.action")
  def action(self, item_type, room = None, value = None, action_trigger = None, orphan = None):
    
    """ 
      Make Openhab item state action.
      ---
      Parameters
        item : String
          Openhab item type
        room : String
          Openhab sitemap room
        value : String (optionnal)
          Item new value
        action_trigger : String (optionnal)
          Part of the sentence that indicate the action to make.
    """
    
    # Get item type lang.
    item_type_lang = self.__get_lang(item_type)
    
    # Check if room not provide.
    if not room :
      # Ask for room information.
      return self.__get_lang("WHAT_ROOM_ITEM_ACTION").format(**locals(), **globals())
    
    # Return response. 
    return f"Call 'Openhab' method 'action' with params : item_type='{item_type}', room='{room}', value='{value}', action_trigger='{action_trigger}'"
  	
  	
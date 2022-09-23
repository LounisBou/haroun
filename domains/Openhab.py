#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Random library import.
import random
# Import core concept domain.
from core.concepts.Domain import Domain 
# Import Openhab library.
from openhab import OpenHAB
# Import logging library
import logging
#
#
# Domain globals : 
#
# Needed slots list.
SLOTS_FILES = [
  "oh_item_type",
  "oh_room",
  "oh_value",
#  "oh_question_trigger",
#  "oh_action_trigger",
]
#
#
# ! DOMAIN 
#
class Openhab(Domain):
  
  def __init__(self):
    
    """ Class constructor. """
    
    # Init parent class Domain.
    super().__init__()
    
    # Openhab API connector.
    self.openhab = None
    
    # Openhab available items.
    self.items = None
        
    # Initialisation.
    
    # Load config file.
    self.load_config()

    # Set variables.
    self.__set_variables()
    
    # Retrieve needed slots.
    self.get_slots_entries(SLOTS_FILES)

    # Initiate openhab connection and try to retrieve items.
    if self.__connect():
      # Log success.
      logging.info("Openhab API connection successful.")
    else:
      # Log error.
      logging.error("Openhab API connection failed.")
    
  def __set_variables(self):

    """ Define Openhab API connection infos from config file. """

    self.openhab_ip = self.config["openhab"]["ip"]
    self.openhab_port = self.config["openhab"]["port"]
    self.openhab_api_url = f"http://{self.openhab_ip}:{self.openhab_port}/rest"
    self.openhab_api_version = self.config["openhab"]["api_version"]
    self.openhab_version = self.config["openhab"]["version"]
    
  def __connect(self):
    
    """
      __connect : Initiate openhab API connection.
      ---
      Return Boolean
        Connection init successful.
    """
    
    try:
      # Initiate openhab API connection.
      self.openhab = OpenHAB(self.openhab_api_url)
      # Retrieve aviable items.
      self.__get_items()
    except:
      # Return connection failed.
      self.openhab = None
      return False
    
    # Return 
    return True
      
    
  def __get_items(self):
    
    """
      __get_items : Retrieve Openhab available items list.
    """
    
    self.items = self.openhab.fetch_all_items()
  
      
  def __improve_answer(self, answer):
    
    """ 
      __improve_answer : Improve answer syntaxe.
      ---
      Parameters 
        answer : String
          Answer sentence.
      ---
      Return String
        Improved answer sentence.
    """
    
    # Check for french syntax error.
    answer = answer.replace("de le", "du")
    answer = answer.replace("de fermé", "fermée")
    answer = answer.replace("de ouvert", "ouverte")
    
    # Capitalize.
    answer = answer.capitalize()
    
    # return answer.
    return answer
    
  @Domain.check_api_connection("openhab")
  @Domain.match_intent("openhab.question")
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
    item_type_lang = self.slots_entries[item_type]
    
    # Check if room not provide.
    if not room :
      # Ask for room information.
      response = self.get_dialog("openhab.question.what_room")
      return response.format(item_type = item_type_lang)
      
    # Get room lang.
    room_lang = self.slots_entries[room]
    
    # Define openhab item name to check.
    openhab_item_name = f"{room}_{item_type}"
    
    # [DEBUG]
    #print(f"check for {openhab_item_name}")
    
    # Retrieve item from Openhab.   
    item = self.items.get(openhab_item_name) 
    # If item exist.
    if item : 
      # Get item state.
      item_state = item.state
      # If item state is string, check for lang translation.
      if item_state in self.slots_entries.keys():
        item_state = self.slots_entries[item_state]
    else: 
      # [DEBUG] Say item not found.
      # Ask for room information.
      response = self.get_dialog("openhab.question.item_not_found")
      return response.format(item_name = openhab_item_name)
    
    # If item state retrieve succefully.
    if item_state :
      response = self.get_dialog("openhab.question.answer")
      response = response.format(
        item_type = item_type_lang,
        room = room_lang,
        item_name = openhab_item_name,
        item_state = item_state
      )
    else:
      # [DEBUG]
      response = f"Call 'Openhab' method 'question' with params : item_type='{item_type}', room='{room}', value='{value}', question_trigger='{question_trigger}'"
    
    # Improve response (answer) syntax.
    response = self.__improve_answer(response)
    
    # Return response. 
    return response
  
  @Domain.check_api_connection("openhab")
  @Domain.match_intent("openhab.action")
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
    item_type_lang = self.slots_entries[item_type]
    
    # Check if room not provide.
    if not room :
      # Ask for room information.
      response = self.get_dialog("openhab.action.what_room")
      return response.format(item_type = item_type_lang)

    # Return response. 
    return f"Call 'Openhab' method 'action' with params : item_type='{item_type}', room='{room}', value='{value}', action_trigger='{action_trigger}'"
    
    
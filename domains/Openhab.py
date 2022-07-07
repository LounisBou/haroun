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
# Import Openhab library.
from openhab import OpenHAB
#
#
# Domain statics attributs : 
#
# Openhab API connection infos.
OPENHAB_IP = "192.168.1.115"
OPENHAB_PORT = "8080"
OPENHAB_API_URL = f"http://{OPENHAB_IP}:{OPENHAB_PORT}/rest"
OPENHAB_API_VERSION = "1"
OPENHAB_VERSION = "3"

# Languages dictionnary.
LANGUAGES = {}

# Openhab language code.
LANG_CODE = 'fr'

# Needed slots list.
SLOTS_FILES = [
  "oh_item_type",
  "oh_room",
  "oh_value",
#  "oh_question_trigger",
#  "oh_action_trigger",
]

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
  "QUESTION_ANSWER" : [
    "{item_type_lang} de {room_lang} est de {item_state}",
  ]
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
    
    # Openhab API connector.
    self.openhab = None
    
    # Openhab available items.
    self.items = None
    
    # Slots entries.
    self.slots_entries = {}
    
    # Initialisation.
    
    # Initiate openhab connexion.
    self.__connect()
    
    # Retrieve aviable items.
    self.__get_items()
    
    # Retrieve needed slots.
    self.__get_slots_entries()
    
    
  def __connect(self):
    
    """
      __connect : Initiate openhab API connexion.
      ---
      Return Boolean
        Connexion init successful.
    """
    
    # Initiate openhab API connexion.
    self.openhab = OpenHAB(OPENHAB_API_URL)
    
    # [TODO]
    # Check for Openhab connexion.
    connected = True
    
    # Return 
    return connected
    
  def __get_slots_entries(self):
    
    # Retrieve slots entries for each specified files.
    for slot_file_name in SLOTS_FILES :
    
      # Use Domain static method getSlot to get slot file entries.
      slot_entries = Domain.getSlot(slot_file_name)
      
      # [DEBUG]
      #print(f"Slot file {slot_file_name} entries : {slot_entries}")
      
      # Add slot_entries to self.slots_entries dict.
      self.slots_entries.update(slot_entries)
    
      
    
  def __get_items(self):
    
    """
      __get_items : Retrieve Openhab available items list.
    """
    
    self.items = self.openhab.fetch_all_items()
    
    
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
    item_type_lang = self.slots_entries[item_type]
    
    # Check if room not provide.
    if not room :
      # Ask for room information.
      return self.__get_lang("WHAT_ROOM_ITEM_INFO").format(**locals(), **globals())
      
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
      return f"Je n'ai pas pu trouver d'item {openhab_item_name}"
    
    # If item state retrieve succefully.
    if item_state :
      response = self.__get_lang("QUESTION_ANSWER").format(**locals(), **globals())
    else:
      # [DEBUG]
      response = f"Call 'Openhab' method 'question' with params : item_type='{item_type}', room='{room}', value='{value}', question_trigger='{question_trigger}'"
    
    # Improve response (answer) syntax.
    response = self.__improve_answer(response)
    
    # Return response. 
    return response
  
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
  	
  	
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# ! SLOTS
# 
"""
  List of slots used in this domain.
  Add listed slots below will be added to the corresponding slots.
  SLOTS constant MUST RESPECT following format :
  
  SLOTS = {
    "slot_name_1" : { 
      "<group_1>" : {
        "entry_1",
        "entry_2",
      },
      "group_2" : {
        "entry_3",
        "entry_4",
      },
      "entry_5",
      "entry_6",
    },
    "slot_name_2" : {
      "group_3" : {
       "entry_7",
       "entry_8",
       "entry_9",
      },     
    },
    "slot_name_3" : {
      "entry_10",
    },
  } 

  This will result by adding entry_1, entry_2, entry_3, entry_4, entry_5 and entry_6 to slot_name_1,
  entry_7, entry_8 and entry_9 to slot_name_2,
  and entry_10 to slot_name_3.
"""
#
# Here defined the slots you will use in this domain :
#
SLOTS = {
  #
  "room" : {
    
    "MAISON" : {
      "maison",
      "home",
    }
  },
  "item_type" : {
    "CTX_TEMP" : {
      "temperature",
      "chaleur",
      "degré",
    }
    
  }
}
#
# ! DOMAIN 
#
class Openhab:
    
  """ 
    Domain statics attributs. 
    They should not be place outside class.
  """
  
  # Openhab API connection infos :
  OPENHAB_IP = "192.168.0.115"
  OPENHAB_PORT = "8080"
  OPENHAB_API_URL = "https://"+OPENHAB_IP+":"+OPENHAB_PORT
  OPENHAB_API_VERSION = "1"
  OPENHAB_VERSION = "3"
  
  def __init__(self):
    
    """ 
      __init__ : Domain constructor.      
    """
    
    pass
  
  
  def question(self, item_type, room = None):
  	
  	""" 
  	  Create domain specifics slots files.
      ---
      Parameters
        item : String
          Openhab item type
        room : String
          Openhab sitemap room
          
    """
  	
  	# Rooms slots
  	
  	# Items slots
  	
  	# 
  	return f"Call 'Openhab' method 'question' with params : item_type='{item_type}', room='{room}'"
  	
  	
  def action(self, item_type, room, value):
  	
  	""" Create domain specifics slots files. """
  	
  	# Rooms slots
  	
  	# Items slots
  	
  	# 
  	return f"Call 'Openhab' method 'action' with params : item_type='{item_type}', room='{room}', value='{value}'"
  	
  	
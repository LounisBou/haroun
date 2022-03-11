#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Random library import.
import random
#
#
# Domain statics attributs : 
#
#
# Languages dictionnary.
LANGUAGES = {}

# Openhab language code.
LANG_CODE = 'fr'

# Define french language.
LANGUAGES['fr'] = {
  
}
#
#
# ! DOMAIN 
#
class Social:
  
  def __init__(self):
    
    """ 
      __init__ : Domain constructor.      
    """
    
    
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
    
  def whatsup(self, whatsup, hi = None, orphan = None):
  	
    """ 
      whatsup : 
      ---
      Parameters
        whatsup : String
          
        hi : String (optionnal)
          
        orphan : String (optionnal)
          
    """
    
    
    # Return response. 
    return f"Call 'Social' method 'whatsup' with params : whatsup='{whatsup}', hi='{hi}', orphan='{orphan}'"
  
  def hi(self, hi, orphan = None):
  	
    """ 
      hi : 
      ---
      Parameters
        hi : String
          
        orphan : String (optionnal)
          
    """
    
    
    # Return response. 
    return f"Call 'Social' method 'hi' with params : hi='{hi}', orphan='{orphan}'"
  
  	
  def bye(self, bye, orphan = None):
  	
  	
  	""" 
  	  bye : 
      ---
      Parameters
        bye : String
          
        orphan : String (optionnal)
                    
    """
  	
  	# Return response. 
  	return f"Call 'Social' method 'bye' with params : bye='{bye}', orphan='{orphan}'"
  	
  	
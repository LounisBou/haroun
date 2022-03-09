#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
#
# 
class Openhab:
  
  """ Domain library for Openhab API Interactions. """
  
  """ Statics attributs. """
  openhab_ip = "192.168.0.115"
  openhab_port = "8080"
  openhab_api_url = "https://"+openhab_ip+":"+openhab_port
  openhab_api_version = "1"
  openhab_version = "3"
  
  
  
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
  	return f"Openhab question method call with params : item_type='{item_type}', room='{room}'"
  	
  	
  def action(self, item_type, room, value):
  	
  	""" Create domain specifics slots files. """
  	
  	# Rooms slots
  	
  	# Items slots
  	
  	# 
  	return f"Openhab action method call with params : item_type='{item_type}', room='{room}', value='{value}'"
  	
  	
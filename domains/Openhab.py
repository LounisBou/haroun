#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import librairie execution de commande
import subprocess
#
# 
class Openhab:
  
  """ Domain library for Openhab API Interactions. """
  
  """ Statics attributs. """
  openhab_ip = "192.168.68.106"
  openhab_port = "8080"
  openhab_api_url = "https://"+openhab_ip+":"+openhab_port
  openhab_api_version = "1"
  openhab_version = "3"
  
  
  
  def __init__(self):
    
    """ Domain class constructor. """	
    
    # Load specifics slots
    self.loadSpecificsSlots()
    
	
	# ! - Methods.
	
	def self.loadSpecificsSlots(self):
  	
  	""" Create domain specifics slots files. """
  	
  	# Rooms slots
  	
  	# Items slots
  	
  	# 
  	
  	
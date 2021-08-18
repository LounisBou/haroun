#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import librairie execution de commande
import subprocess
#
# 
class Kodi:
  
  """ Domain library for KODI API Interactions. """
  
  """ Statics attributs. """
  kodi_ip = "192.168.68.106"
  kodi_port = "8080"
  kodi_api_url = "https://"+kodi_ip+":"+kodi_port
  kodi_api_version = "1"
  kodi_version = "18"
  
  
  def __init__(self):
  
    """ Domain class constructor. """	
    
    return True
    
  # ! - Methods.
  
  def loadSpecificsSlots(self):
  
    """ Create domain specifics slots files. """
    
    return True  	
	
  def run(self, film):
  
    """ TEST """
    
    return film
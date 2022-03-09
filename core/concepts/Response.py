#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import system library.
import sys
# Import OS library.
import os
#
#
# Globals :
#
# Current, parent, and root paths.
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
DOSSIER_RACINE = os.path.dirname(DOSSIER_PARENT)
sys.path.append(DOSSIER_RACINE)
#
#
#
class Response:
    
  """ Concept of Haroun Response. """
  
  def __init__(self):
    
    """ 
      __init__ : Response class constructor.
    """	
    
    # Raw text.
    self.raw_text = None
    # Message text.
    self.msg_text = None
    # HTML text.
    self.html_text = None
    # HTML text.
    self.json_text = None
    
    # Flag error.
    self.error = 0
    
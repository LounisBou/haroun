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
    self.raw_text = ""
    # Message text.
    self.msg_text = ""
    # HTML text.
    self.html_text = ""
    # HTML text.
    self.json_text = ""
    # Error text.
    self.error_text = ""
    
    # Flag error.
    self.error = False
    
  def __parse_raw_text(self):
    
    """
      addResponse : Parse raw_text attribut to create others output format.
      ---
      Return
        None
    """
    
    # Create msg text.
    self.msg_text = self.raw_text
    
  def __parse_error(self):
    
    """
      __parse_error : Parse error_text attribut to output format.
      ---
      Return
        None
    """
    
    # Parse error_text attribut.
    self.error_text = self.error_text
    
  
  def addRawText(self, raw_text):
    
    """
      addRawText : 
      ---
      Parameters
        raw_text : String
          Response raw text.
      ---
      Return
        None
    """
    
    # Add new raw_text to raw_text attribut.
    self.raw_text = self.raw_text + "\n" + raw_text
    
    # Parse raw text.
    self.__parse_raw_text()
    
    
  def addError(self, error_text):
    
    """
      addError : 
      ---
      Parameters
        error_text : String
          Error message.
      ---
      Return
        None
    """
    
    # Add new error_text to error_text attribut.
    self.error_text = self.error_text + "\n" + error_text
    
    # Flag error.
    self.error = True
    
    # Parse raw text.
    self.__parse_error()
        
    
    
    
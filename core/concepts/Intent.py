#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
class Intent: 
  
  """ Concept of Haroun Intent. """
  
  def __init__(self):
    
    """ Intent class constructor. """
    
    # Error flag.
    self.error = 0
    
    # Stimulus
    self.stimulus = None
    # Recognition
    self.recognition = None
    
    # Text
    self.text = None
    # Raw text
    self.raw_text = None
    # Label.
    self.label = None
    # Confidence.
    self.confidence = None
    # Entities
    self.entities = None
    # Orphan entity
    self.orphan_entity = None
    # Tokens
    self.tokens = None
    # Raw tokens
    self.raw_tokens = None
  
  def __str__(self):
    
    """ Intent print method. """
    
    # Text
    print_str = "["+str(self.label)+"]"+"\n"
    print_str += "text  : "+str(self.text)+"\n"
    #print_str += "raw_text  : "+str(self.raw_text)+"\n"
    #print_str += "confidence  : "+str(self.confidence)+"\n"
    print_str += "entities  : \n"
    if self.entities : 
      print_str += "\n".join([" - "+str(entity['entity'])+" : "+str(entity['value']) for entity in self.entities])+"\n"
    if self.orphan_entity :
      print_str += " - orphan entity : "+self.orphan_entity+"\n"
    #print_str += "tokens  : \n"
    #if self.tokens : 
      #print_str += "\n".join([str(token) for token in self.tokens])+"\n"
    #print_str += "raw_tokens  : \n"
    #if self.raw_tokens : 
      #print_str += "\n".join([str(raw_token) for raw_token in self.raw_tokens])+"\n"
    
    return print_str
    
  
  # ! - Initialisation.
  
  def checkRecognition(self, stimulus, recognition):
    
    """ 
      Check recognition to define intent info. 
      
      Try to define the intent attributs (label, entities, tokens...) from recognition Object.
      
      Parameters
      ----------
      stimulus : Stimulus source of the Interaction recognition .
      recognition : Recognition Object generated from Interaction interpretation.
      
      Returns
      _______
      void
    
    """
    
    # Stimulus
    self.stimulus = stimulus
    # Recognition
    self.recognition = recognition
    
    # Text
    self.text = recognition['text']
    # Raw text
    self.raw_text = recognition['raw_text']
    # Label.
    self.label = recognition['intent']['name']
    # Confidence.
    self.confidence = recognition['intent']['confidence']
    # Entities
    self.entities = recognition['entities']
    # Orphans
    self.orphan_entity = self.stimulus.raw_sentence.replace(self.text,"")
    # Tokens
    self.tokens = recognition['tokens']
    # Raw tokens
    self.raw_tokens = recognition['raw_tokens']
    
    return True
    
    
    
    

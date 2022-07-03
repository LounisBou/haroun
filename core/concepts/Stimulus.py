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
class Stimulus:
    
  """ Concept of Haroun Stimulus. """
  
  def __init__(self, source, source_id, sentence, user_id, interaction_id, parent_interaction_id, origin_datetime):
    
    """ Stimulus class constructor. """	
    
    """
      Parameters
      ----------
      source : String
        Label for stimulus source origin.
      source_id : String
        Uniq identifier for stimulus source origin.
      sentence : String (optionnal)
        Sentence of the stimulus. [Default = '']
      user_id : Int (optionnal)
          Uniq identifier for user who initiate interaction. [Default = null]
      interaction_id : Int (optionnal)
          Uniq identifier for interaction. [Default = null]  
      parent_interaction_id : Int (optionnal)
        Uniq identifier for parent interaction if Stimulus is due cause of previous interaction. [Default = null]
      origin_datetime : Datetime (optionnal)
        Datetime origin for stimulus. [Default = null]
    """ 
    
    # Source label
    self.source = source
    
    # Source ID
    self.source_id = source_id
    
    # Sentence
    self.raw_sentence = sentence
    
    # Sentence
    self.sentence = self.raw_sentence
    
    # Interaction user ID.
    self.user_id = user_id
    
    # Interaction ID if one.
    self.interaction_id =interaction_id
    
    # Parent interaction ID if one.
    self.parent_interaction_id = parent_interaction_id
    
    # Datetime origin of the stimulus.
    self.origin_datetime = origin_datetime
    
    # Error flag.
    self.error = False
    
    # Interaction flag.
    self.interaction = False
    
    # Stimulus duration.
    self.duration = None
    
    # Clean sentence.
    self.__clean_sentence()
  
  def __clean_sentence(self):
    
    """ 
      __clean_sentence : Clean stimulus sentence. 
      
      Improve sentence such for NLU parsing.      
    """	
    
    # Spacers : add space before defined character.
    spacers = ('°', '%', '$', '€', '£')
    
    # Add spacers.
    for spacer in spacers :
      # Replace splac
      self.sentence = self.sentence.replace(spacer, f" {spacer}")    
    
     
    
  def isValid(self):
    
    """ 
      Define stimulus validity. 
      
      A Stimulus is valid is Haroun Brain manage to understand it.
            
      Returns
      _______
      self.error : Boolean
        True if stimulus is valid and Haroun Brain manage to understand it.
      
    """	
    
    # Return error flag.
    return not self.error
    
    
  def needInteraction(self):
    
    """ 
      Define interaction validity. 
      
      Is interaction is required by Haroun Brain ?
            
      Returns
      _______
      self.error : Boolean
        True if interaction is required by Haroun Brain.
      
    """
    
    # Check if there is a sentence required for the interaction.
    if self.sentence :
      self.interaction = True
    else:
      self.interaction = False
    
    # Return interaction flag.
    return self.interaction
  
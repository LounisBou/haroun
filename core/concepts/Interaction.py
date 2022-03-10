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
# Import Path function form pathlib library.
from pathlib import Path
# Import json library.
import json
# Test spacy for POS-Tagging
# import spacy
# from spacy_lefff import LefffLemmatizer
# from spacy.language import Language
# Import rhasspy-nlu library. 
import rhasspynlu
#
# Import utils
from utils.debug import *
#
#
# Haroun dependancies :
#
# Import core concept Intent.
from core.concepts.Intent import Intent
# Import core concept Intent.
from core.concepts.Response import Response
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
class Interaction:
  
  """ Concept of Interaction for Haroun. """
    
  def __init__(self, stimulus):
    
    """ 
      Interaction class constructor.
      
      Interaction concept class, manage interaction infos.
      
      Parameters
      ----------
      stimulus : Stimulus
        Stimulus at the origin of the interaction.
      
      
      Returns
      _______
      void
      
    """
    
    # ! Attributs
    
    # Error flag.
    self.error = False
    # Done flag.
    self.done = False
    
    # Interaction duration
    self.duration = None
    # Interaction stimulus.
    self.stimulus = stimulus   
    # Sentence words list.
    self.words = self.stimulus.sentence.split(' ')
    
    # Recognition : JSON Recognition Object from NLU recognize.
    self.recognition = None
    # Recognition duration
    self.recognition_duration = None
    
    # Intent : Intent that match the Interaction (defined by Recognition)
    self.intent = Intent()
    # Response : Interaction Response.
    self.response = Response()
    
    # Domain matching intent.
    self.domain = None
    # Skill for interaction execution.
    self.skill = None
    
    # Interaction state of mind.
    self.mind = None
    

  # Fonctions de manipulations : 
  
  def addResponse(self, raw_text):
    
    """
      addResponse : 
      ---
      Parameters
        raw_text : String
          Response raw text.
      ---
      Return
        None
    """
    # Add raw_text to response object.
    self.response.addRawText(raw_text)
    
    # Done flag.
    self.done = True
    
  
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
    
    # Add error_text to response object.
    self.response.addError(error_text)
    
    # Flag error.
    self.error = True

  
  def containsWord(self, word):

    # On parcours la liste de mots.
    for i in range(0,len(self.words)):
      # Récupération du mot courant.
      current = self.mots[i]
      # Test de correspondance du mot (minuscule)
      if(current.lower() == mot.lower()):
        return i
    return -1
  
  # Detect : retourne la position du mot trouvé, -1 sinon.
  def detect(self, mots):
    # On parcours la liste de mots à controller.
    for i in range(0,len(mots)):
      # Récupération du mot courant.
      current = mots[i]
      # On analyse la présence d'un mot dans la question.
      contentPosition = self.contient(current)
      # Si question possède le mot
      if(contentPosition != -1):
        return contentPosition
    return -1


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
from core.concepts.Intent import *
# Import core concept Response.
from core.concepts.Response import *
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
    
    

  # ! NLU (Natural Language Understanding)
  
  def interpreter(self, training_graph):
    
    """ 
      Interpreter method, apply NLU analysis on Interaction sentence.
      
      Interpretation of Interaction sentence via rhasspy-nlu.
      Try to retrieve a recognition dict, if success then create define an the interaction intent attribut from it.
      
      Parameters
      ----------
      training_graph : DiGraph—Directed (See https://networkx.org/documentation/networkx-2.3/reference/classes/digraph.html)
        rhasspy-nlu DiGraph—Directed training result is a directed graph whose states are words and edges are input/output labels.
      
      Returns
      _______
      Boolean : Interpretation of interaction success, recognition and intent attributs are now defined.
      
    """
    
    # [DEBUG]
    #print('Interaction sentence : '+self.stimulus.sentence)
    #print('----------------------------------------')
    
    # Stimulus sentence pre-treatment.
    self.stimulus.sentence = self.stimulus.sentence.lower()
    self.stimulus.sentence = self.stimulus.sentence.replace(',',"")
    
    # Perform intent recognition in Interaction sentence thanks to training graph.
    recognitions = rhasspynlu.recognize(self.stimulus.sentence, training_graph, fuzzy=True)
    
    # [DEBUG]
    #print("Recognitions  : ")
    #print(recognitions)
    #print('----------------------------------------')
    
    # If rhasspynlu perform recognition without problem.
    if(recognitions):
      
      # Format recognitions as dict.
      recognitions_dict = recognitions[0].asdict()
      # Format recognition dict as json string.
      recognition_string = json.dumps(recognitions_dict)
      
      # Format recognition as Object.
      self.recognition = json.loads(recognition_string)
      
      # Retrieve recognition duration
      self.recognition_duration = self.recognition['recognize_seconds'] 
      
      # Retrieve stimulus duration
      self.stimulus.duration = self.recognition['wav_seconds']
      
      # Define intent.
      self.defineIntent()
      
      # Return
      return True
      
    else:
      # Return
      return False
      
  
  def defineIntent(self):
    
    """ 
      Define Intent attribut from recognition.
      
      Try to retrieve intent label, entities, tokens, ect... from recognition dict.
      
      Returns
      _______
      Boolean : Ìntent defined with success.
      
    """
    
    return self.intent.checkRecognition(self.stimulus, self.recognition)
  
  
  # Fonctions de manipulations : 
  
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


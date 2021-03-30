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
# Import rhasspy-nlu library. 
import rhasspynlu
#
#
# Haroun dependancies :
#
# Import core concept intent.
from core.concepts.Intent import *
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
    
  def __init__(self, sentence):
    
    """ 
      Interaction class constructor.
      
      Interaction concept class, manage interaction infos.
      
      Parameters
      ----------
      sentence : String
        Interaction sentence in string format
      
      
      Returns
      _______
      void
      
    """
    
    # ! Attributs
    
    # Error flag.
    self.error = 0
    
    # Interaction sentence.
    self.sentence = sentence   
    # Sentence words list.
    self.words = self.sentence.split(' ')
    # Recognition : JSON Recognition Object from NLU recognize.
    self.recognition
    # Intent : Intent that match the Interaction (defined by Recognition)
    self.intent
    

  # ! NLU (Natural Language Understanding)
  
  def interpreter(self, training_graph):
    
    """ 
      Interpreter method, apply NLU analysis on Interaction sentence.
      
      Interpretation of Interaction sentence via rhasspy-nlu.
      
      Parameters
      ----------
      training_graph : DiGraph—Directed (See https://networkx.org/documentation/networkx-2.3/reference/classes/digraph.html)
        rhasspy-nlu DiGraph—Directed training result is a directed graph whose states are words and edges are input/output labels.
      
      Returns
      _______
      void
      
    """
    
    # Perform intent recognition in Interaction sentence thanks to training graph.
    recognitions = rhasspynlu.recognize(self.sentence, training_graph)
    
    # If rhasspynlu perform recognition without problem.
    if(recognitions):
      # Format recognitions as dict.
      recognitions_dict = recognitions[0].asdict()
      # Format recognitions dict as json.
      self.recognition = json.dumps(reconnaissance_dict)
      # [DEBUG]
      print(self.recognition)
    else:
      # [DEBUG]
      print("Je n'ai pas compris votre intention.")
           

  # Fonction : Setter
  def set(self, text):
    self.__init__(text)
  
  # Fonctions : Getter
  def getText(self):
      return self.texte
      
  def getList(self):
    return self.mots
  
  def getMot(self, position):
    return self.mots[position]
  
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


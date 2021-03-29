#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Dependances : sys, os
#
# Import de la librairie system
import sys
# Import de la librairie OS
import os
# Import de Path depuis la librairie pathlib.
from pathlib import Path
# Import JSON.
import json
# Rhasspynlu
import rhasspynlu
#
#
# Import core concept intent.
from core.concepts.Intent import *
#
#
#
# Ajout des du dossier des domaines au path systeme
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PARENT = os.path.dirname(DOSSIER_COURRANT)
DOSSIER_RACINE = os.path.dirname(DOSSIER_PARENT)
sys.path.append(DOSSIER_RACINE)
#
#
# Class : Question (Question au format texte du STT)
class Question:
    
  # ! - Fonctions
  
  # Fonction : Constructeur
  def __init__(self, text):
    
    # ! Attributs
    
    # Flag d'état.
    self.error = 0
    # Chaine à manipuler.
    self.texte = text   
    # Liste de mot.
    self.mots = self.texte.split(' ')
    

  # Fonction : NLU (Natural Language Understanding)
  def interprete(self):
    
    # Chargement des intentions de compétences
    intentions = rhasspynlu.parse_ini(Path(DOSSIER_RACINE+"/competences/openhab.ini"))
    
    # Analyse des intentions en graph d'intentions.
    intentions_graph = rhasspynlu.intents_to_graph(intentions)
    
    # Reconnaissance de l'intention dans le texte en fonction du graph d'intentions.
    reconnaissance = rhasspynlu.recognize(self.texte, intentions_graph)
    
    # Si la reconnaissance de l'intention est réussi.
    if reconnaissance :
      # Transformation de la reconnaissance reconnue au format JSON.
      reconnaissance_dict = reconnaissance[0].asdict()
      # [DEBUG]
      print(json.dumps(reconnaissance_dict))
    else:
      # DEBUG
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
  
  # Fonctions de m anipulations : 
  
  # Contient : retourne la position du mot, -1 sinon.
  def contient(self, mot):
    # On parcours la liste de mots.
    for i in range(0,len(self.mots)):
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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Dependances : 
#
#
# Consciousness
from core.consciousness.Conscious import *
from core.consciousness.Ego import *
#
# Concepts
from core.concepts.Domain import *
from core.concepts.Skill import *
from core.concepts.Stimulus import *
from core.concepts.Interaction import *
from core.concepts.Intent import *
from core.concepts.Memory import *
#
#
#
# Variables : 
#
# Ajout des du dossier des domaines au path systeme
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))
DOSSIER_RACINE = os.path.dirname(DOSSIER_COURRANT)
sys.path.append(DOSSIER_RACINE)
#
#
#
# Class : Cerveau d'Haroun
class Cerveau:  
  
  # ! Fonctions
  
  # Fonction : Constructeur
  def __init__(self):
    
    # - Attributs Reflexion :
    
    # Conscience (paramètres de la réfléxion).
    self.me = Me()
    
    # Interaction.
    self.interaction = Interaction('')

    # Memories 
    self.memories = Memory()
  
  # ! - Domaines et compétences.
  
  # Fonction : Parcours les domaines et étudie chaque domaine.
  def apprentissage(self):
    # Ajout à la liste des Competences d'Haroun
    self.competences.append(competence)

  # Fonction : Ajout des Competences d'un domaine
  def etudie(self, domaine):
    # Pour chaque compétence du domaine
      # Ajout à la liste des competences d'Haroun
    return
    
  # Fonction : Apprendre une competence. 
  def apprendre(self, competence):
    # Ajout à la liste des Competences d'Haroun
    self.competences.append(competence)
  
  # ! - Analyse de la question.
  
  # Fonction : Analyse la question pour trouver la Competence correspondante et récupèrer les paramètres.
  def analyse(self, texte, encode):
    
    # On définie le texte de la question.
    self.question.set(texte)
    
    # Interprétation de la question : NLU.
    self.question.interprete()    
        
    # ! Trouver Competence.
    
    # Pour chaque Competence 
    for i in range(0,len(self.competences)):
    
      # On vérifie si les mots clefs de la Competence son présent dans la question.
      position = self.question.detect(self.competences[i].keywords);
      
      # DEBUG
      #print('Competence '+str(i)+' => '+str(position))
      
      # Test si la Competence correspond
      if(position != -1):
      
        # On charge le cerveau avec la Competence.
        self.competence = self.competences[i]
        
        # DEBUG
        #print('Paramètres : ')
        
        # ! Params => Variables.
        
        # Pour chaque parametre de la Competence.
        for param_name, value_positions in self.competence.params.items():
          
          # Instancie/Reset la variable value
          value = ""
          
          # ! Définition des bornes
          
          # Si debut est un chiffre.
          if( isinstance( value_positions[0], int ) ):
            debut = value_positions[0]
          else: # C'est un mot.
            # Si il est contenu dans la chaine.
            pos = self.question.contient(value_positions[0])
            if(pos != -1):
              fin = value_positions[0]
            else:
              pos = 0
            
          # Si fin est un chiffre.
          if( isinstance( value_positions[1], int ) ):
            fin = value_positions[1]
          else: # C'est un mot.
            # Si il est contenu dans la chaine.
            pos = self.question.contient(value_positions[1])
            # Affect la position (-1 si non trouvé)
            fin = pos
                    
          # Si debut < 0, alors on met le debut à 0
          if(debut < 0):
            debut = 0                 
          # Si fin à -1, on prend la fin de la question.
          if(fin == -1):
            fin = len(self.question.mots)
          # Si fin > fin_question, on prend la fin de la question.
          if(fin > (len(self.question.mots))):
            fin = len(self.question.mots)
          
          # DEBUG
          #print('Param '+param_name+' from '+str(debut)+' to '+str(fin)) 
          
          # Je récupère dans la phrase les parties correspondante :
          for i in range(debut,fin):
            # Construction de la value par concatenation mot à mot.           
            value =  value + " " + self.question.getMot(i)
          # J'affecte leurs valeurs aux variables.
          self.competence.variables[param_name] = value
          
        # DEBUG
        #print('Variables : ')
        #for var_name, var_value in self.competence.variables.items():
          # DEBUG
          #print( 'Var ' + var_name + ' = ' + str(var_value) )
          
        # Trouvé
        return 1
      # Fin if position != 1
    # Fin for.
    
    # Aucune compétence correspondante trouvé.
    return 0
  
  # Fonction : Execute la demande
  def execute(self):
    # DEBUG
    #print("Execute...")
  
    # ! Compétence
  
    # On execute la compétence.
    self.domaine.execute(self.competence)
    
    # ! Reponse
    
    # On choisie une réponse pour la compétence.
    reponse = self.competence.reponses[0]
    # On remplace les variables dans la reponse.    
    self.reponse.texte = reponse.format(**self.competence.variables)
    
    # DEBUG
    #print("Reponse : "+self.reponse.texte)   
    # Retour
    return 1
  
  # Fonction : Reflexion personnel d'Haroun. (temps de refléxion)
  def reflexion(self):
    # Retour
    return 1


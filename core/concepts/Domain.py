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
class Domain:
	
	""" Concept of Haroun Domain. """
	
	# Fonction : Constructeur
	def __init__(self):
  	
  	""" Domain class constructor. """		
  
    # Action to manage via domain.
		action = ""
	
  # Fonction d'import
	def my_import(name):
		components = name.split('.')
		mod = __import__(components[0])
		for comp in components[1:]:
			mod = getattr(mod, comp)
		return mod
	
	# Fonction : execution
	def execute(self, competence):
		
		# Récupération des paramètres de la compétence.
		
		# Récupération du nom du domaine.
		domaine_name = competence.domaine
		# Récupération du nom de la class.		
		class_name = competence.domaine
		# Chemin import class
		class_import_path = 'domaines.'+domaine_name 
		
		# DEBUG
		#print('Chemin : '+class_import_path)
		
		# ! Domaine
		
		# Import du domaine
		domaine_module = __import__(class_import_path, fromlist = [class_name])
		# On récupère la class
		domaine_class = getattr(domaine_module, class_name)
		# Instance du domaine
		domaine_instance = domaine_class()
		
		# ! Action 
		
		# Récupération de l'action.
		action_name =  competence.action
		
		# Si la fonction "action_name" existe bien.
		if(hasattr(domaine_instance, action_name)):
			
			# Récupération fonction à actionner.
			action_func = getattr(domaine_instance, action_name)
		
			# Execution de la fonction "action_name".
			competence.reaction = action_func(**competence.variables)
			
			# On crée la variable "reponse"
			competence.variables['reponse']	= competence.reaction

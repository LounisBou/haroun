#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Dependances : subprocess
#
# Import librairie execution de commande
import subprocess
#
# Class : Competence exécuté par Haroune.
class Skill:
	
	# ! - Fonctions
	
	# Fonction : Constructeur
	def __init__(self):
		
		# Keywords
		self.keywords = []
		# Params
		self.params = {}
		# Domaine de Competence
		self.domaine = ''
		# Action de la Competence
		self.action = ''
		# Reponses Competence
		self.reponses = []		
		# Variables
		self.variables = {}		
		# Reaction Competence
		self.reaction = ''		
		# Code de retour Competence
		self.erreur = -1
	
	# Fonctions : Setter
	def addKeyword(self, keyword):
		self.keywords.append(keyword)
	def setKeywords(self, keywords):
		self.keywords = keywords
	
	def addParam(self, paramName, positions):
		self.params[paramName] = positions
	def setParams(self, params):
		self.params = params
		
	def addVariable(self, varName, value):
		self.variables[varName] = value
	def setVariables(self, variables):
		self.variables = variables
	
	def setDomaine(self, domaine):
		self.domaine = domaine
		
	def setAction(self, action):
		self.action = action
		
	def addReponse(self, reponse):
		self.reponses.append(reponse)		
	def setReponses(self, reponses):
		self.reponses = reponses
	
	# Fonctions : Getter	    
	def getParam(self, paramName):
		return self.params[paramName]	
		
	def getKeyword(self, position):
		return self.keywords[position]	
	

	# Fonction : Excute
	def execute(self):
		# Ecécution de la Competence 
		# et récuperaction de la sortie standard
		# Version DEBUG : Sortie erreur redirigé vers sortie standard
		# result = subprocess.check_output([batcmd], stderr=subprocess.STDOUT)
		self.reaction = subprocess.check_output(self.action, shell=True)
		# Et on renvoi.
		return 1
		

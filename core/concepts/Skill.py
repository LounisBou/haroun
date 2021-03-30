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
# Import subprocess library.
import subprocess
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
class Skill:
	
	""" Concept of Haroun Skill. """
	
	def __init__(self):
		
		""" Skill class constructor. """		
		
		# Keywords.
		self.keywords = []
		# Params.
		self.params = {}
    # Variables.
		self.vars = {}	
		# Domain of skill.
		self.domain = ''
		# Action of skill.
		self.action = ''
		
		# Skill exectution answer.
		self.answer_infos = []		
		# Reaction Competence.
		self.reaction = ''		
		# Error flag.
		self.error = -1
	
  
  """ Getters/Setters """

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
	
	def getParam(self, paramName):
		return self.params[paramName]	
		
	def getKeyword(self, position):
		return self.keywords[position]	
	
  
  """ Skill management methods : """
  
  def prepare(self):
    
    """
  	  Prepare skill for execution.
  	  
  	  Prepare skill data to perform action domain skill execution.
  	  
  	  Returns
  	  -------
  	  void.
    """
    
    # End.
    return
    
  
	def execute(self):
  	
  	"""
  	  Execute the skill.
  	  
  	  Execute the method of domain link to the skill action, and retrieve stdOut output.
  	  
  	  Execution via : subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    	  command : Shell command to execute.
    	  shell : Flag to use shell.
    	  stderr : Flag to redirect stdErr.
  	  
  	  Returns
  	  -------
  	  execution_code : Int
  	    Return value of skill execution.
    """
  	
		# Excécution de la Competence 
		# et récuperaction de la sortie standard
		# Version DEBUG : Sortie erreur redirigé vers sortie standard
		# result = subprocess.check_output([batcmd], stderr=subprocess.STDOUT)
		self.reaction = subprocess.check_output(self.action, shell=True)
		
		# End.
		return 1
		

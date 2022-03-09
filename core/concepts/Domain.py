#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import system library.
import sys
# Import Python Object Inspector library.
import inspect
# Import OS library.
from os import path
#
#
# Globals :
#
# Current, parent, and root paths.
DOSSIER_COURRANT = path.dirname(path.abspath(__file__))
DOSSIER_PARENT = path.dirname(DOSSIER_COURRANT)
DOSSIER_RACINE = path.dirname(DOSSIER_PARENT)
sys.path.append(DOSSIER_RACINE)
import domains
#
#
DOMAINS_PATH = f"{DOSSIER_RACINE}/domains"
#
class Domain:
  
  """ Concept of Haroun Domain. """
  
  # Fonction : Constructeur
  def __init__(self, name):
    
    """ 
      __init__ : Domain class constructor. 
      ---
      Parameters : String
        domaine_name : Name of the domain class.
    """   
  
    # Domain name.
    self.name = name
    
    # Instanciate domain class.
    self.instance = None
    # Domains modules.
    self.modules = None
    # Domain module.
    self.module = None
    # Domain class.
    self.class_name = None
    
    # Domain methods list.
    self.methods = {}
    
    # Instanciate domain.
    self.__instanciate()
    
    # Get domain instance methods.
    self.__get_methods()
    
    
  
  def __instanciate(self):
    
    """
      __instanciate : Create an instance of domain class.
    """
    
    # Import domains module.
    self.modules = __import__(f"domains", fromlist=[self.name])
    
    # Get domain class
    self.module = getattr(self.modules, self.name)
    self.class_name = getattr(self.module, self.name)
        
    # Instanciate domain class.
    self.instance = self.class_name()
    
    
    
  def __get_methods(self):
    
    """
      __get_methods : Retrieve domain methods instance list. 
    """
    
    # Get methods names and args.
    domains_instance_methods_and_locations = inspect.getmembers(self.instance, predicate=inspect.ismethod)    
    for method_and_location in domains_instance_methods_and_locations :
    
      # Get method name.
      method_name = method_and_location[0]
      
      # Get domain instance method.
      method = getattr(self.instance, method_name)
      
      # Save methods name and args.
      self.methods[method_name] = method
    
  
  def methodExist(self, method_name):
    
    """
      methodExist : Check if method_name is a valid method for domain.
      ---
      Parameters : 
        method_name : String
          Method name to check in domain instance.
      ---
      Return Boolean
        Method is valid for domain.
    """ 
    
    # Return
    return method_name in self.methods
    
    
  def methodGetArgs(self, method_name):
    
    """
      methodExist : Get methods arguments list as tuple.
      ---
      Parameters : 
        method_name : String
          Method name in domain instance.
      ---
      Return Tuple
        Method arguments.
    """ 
    
    # Get Skill method.
    method = self.methods[method_name]
    
    # Return methods args.
    return inspect.getargspec(method).args
  
  def executeSkill(self, skill):
    
    """
      executeSkill : Execute the skill on a domain class method.
      ---
      Parameters : 
        skill : Skill
          Skill to execute.
      ---
      Return skill : modified skill.
    """ 
    
    # Get methods.
    method = self.methods[skill.method_name]
    
    # Execute methods with skill parameters
    skill.return_values = self.methods[skill.method_name](**skill.parameters)
    
    # Return modified skill
    return skill

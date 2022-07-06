#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import system library.
import sys
# Import OS library.
from os import path
# Import Python Object Inspector library.
import inspect
# Import functools wraps for decorators.
from functools import wraps
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
  
  # Static variables :
  
  # Store next loading domain name.
  loading_domain_name = None
  
  # Store intents handlers for each instanciate domains
  intents_handlers = {}
  
  # Fonction : Constructeur
  def __init__(self, name):
    
    """ 
      __init__ : Domain class constructor. 
      ---
      Parameters : String
        domaine_name : Name of the domain class.
    """   
    
    # Prepare for loading domain.
    Domain.loading_domain_name = name
    
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

    # Set name of the last instanciate domain.
    Domain.last_instanciate_domain_name = self.name
        
    # [DEBUG]
    #print(f"Domain {Domain.loading_domain_name} loaded.")
    
    
    
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
    
    # Retrieve method arguments.
    args = inspect.getargspec(method).args
    
    # [DEBUG]
    print(f"{method_name} args : {args}")
    
    # Return methods args.
    return args
    
  
  
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
  
  @staticmethod
  def register_handled_intent(function_name, intent_name):
    
    """
      Register the function that handle intent.
    """
    
    # [DEBUG]
    #print(f"Preparing intent handler for {Domain.loading_domain_name}")
        
    # If intent_name entry don't exist. 
    if intent_name not in Domain.intents_handlers.keys() :
      # Create intent handler entry in intents_handlers.
      Domain.intents_handlers[intent_name] = {
        "domain" : Domain.loading_domain_name,
        "method" : function_name
      }
      # [DEBUG]
      print(f"Register {Domain.loading_domain_name}.{function_name} as handling {intent_name}")
    else:    
      # [DEBUG]
      print(f"Intent handler for {intent_name} already exist !")  
    
    
    
    
    
  



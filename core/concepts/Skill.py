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
# Import Python Object Inspector library.
import inspect
# Import functools wraps for decorators.
from functools import wraps
# Import core domain concept class.
from core.concepts.Domain import Domain

#
#
# Globals :
#
#
#
#
class Skill:
  
  """ Concept of Haroun Skill. """
  
  def __init__(self, domain_name, method_name):
    
    """ Skill class constructor. """   
    
    # Domain the skill is link.
    self.domain_name = domain_name
    # Method of domain the skill is link.
    self.method_name = method_name
    
    # Skill exectution return values.
    self.return_values = None
    
    # Skill exectution return values.
    self.return_values = None  
    
    # Skill execution parameters.
    self.parameters = None
    
    # Skill prepared flag.
    self.prepared = False
    
    # Skill exectution error flag.
    self.error = -1
  
  
 
  
  
  """ Skill management methods : """
  
  def prepare(self, intent, method_args):
    
    """
      Prepare skill for execution.
      Match intent with methods args to create skills execution parameters.
      ---
      Parameters
        intent : Intent
          Interaction intent Object.
        method_args : Tupple
          Domain method arguments list.
      ---
      Returns
        Boolean : Intent match method_args, skill is prepared.
    """
    
    # Skill execution parameters.
    self.parameters = {}
    
    # Parse intent entities to create parameters.
    for entity in intent.entities :
      # Get entity name and value.
      entity_name = entity['entity']
      entity_value = entity['value']
      # Check if entity exist in method args.
      if entity_name in method_args :
        # Create parameter.
        self.parameters[entity_name] = entity_value
      
    # Skill prepared flag.
    self.prepared = False
    
    # Return prepared status.
    return self.prepared
    
  
  # ! Decorators :
  
  @staticmethod
  def match_intent(intent_name):
    
    """
      Decorator that allow a domain method to match a specific intent.
      ---
      Parameters
        intent_name : String
          Name of intent to match.
      ---
      Return Function
        Decorator inner function.
    """
    
    def inner_function(function):
      
      """
        inner_function that received the original function in parameters.
        --- 
        Parameters
          function : Function
            Domain method on which the decorator was applied.
        ---
        Return Function
          Decorator function wrapper
      """
    
      @wraps(function)
      def wrapper(self_instance, *args, **kwargs):
        
        """
          match_intent wrapper function. Execute decorator code.
          ---
          Parameters
            self_instance : Class instance
              Domain instance on which method have been called.
            *args : List
              List of arguments pass on function call.
            *kargs : Dict
              Dict of arguments_names : arguments pass on function call.
          ---
          Return : result of function call.
        """
        
        # [DEBUG]
        #print(f"Intent name : {intent_name}")
        #print(f"Instance : {self_instance}")
        #print(f"args :  {args}")
        #print(f"kwargs : {kwargs}")
        #print(f"Before Calling {function.__name__}")
        
        # Call the original function.
        result = function(self_instance, *args, **kwargs)
        
        # [DEBUG]
        #print(f"After Calling {function.__name__}")
        
        # Return result.
        return result
      
      # Try to maintain method signature.
      wrapper.__signature__ = inspect.signature(function)  # the magic is here!
            
      # Registering function as intent handler.
      Domain.register_handled_intent(function.__name__, intent_name)
            
      # [DEBUG]
      #print(f"Decorator for domain {function.getattr()}, method {function.__name__} : {intent_name}")
      
      # Return the wrapper function.
      return wrapper
          
    # Return inner_function
    return inner_function

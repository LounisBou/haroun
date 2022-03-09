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
    
  
    

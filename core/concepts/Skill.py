#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
#
#
# Globals :
#
#
#
#
class Skill(object):
    
    """ Concept of Haroun Skill. """
    
    def __init__(self, domain_module_name, domain_class_name, domain_method_name):
        
        """ Skill class constructor. """   
        
        # Domain module the skill is link to.
        self.module_name = domain_module_name
        # Domain class the skill is link to.
        self.class_name = domain_class_name
        # Domain method the skill is link to.
        self.method_name = domain_method_name
        
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
        self.prepared = True
        
        # Return prepared status.
        return self.prepared
        
    
 

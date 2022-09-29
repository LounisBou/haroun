#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
from core.concepts.Domain import Domain 
#
#
# Domain globals : 
#
# Needed slots list.
SLOTS_FILES = []
#
# ! DOMAIN 
#
class DomainExemple(Domain):
    
    def __init__(self):
        
        """ Class constructor. """
                
        # Init parent class Domain.
        super().__init__()
        

    
    @Domain.match_intent("domain_exemple.intent_name")
    def whatsup(self, whatsup, hi = None, orphan = None):
        
        """ 
            A method that handle intent.    
        """
        
        # Return a response dialog.
        return self.say("domain_exemple.dialog_key")
    

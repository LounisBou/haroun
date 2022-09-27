#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
#
# Haroun dependancies :
#
# Import core concept Intent.
from core.concepts.Intent import Intent
# Import core concept Intent.
from core.concepts.Response import Response
#
#
# Globals :
#
#
#
#
class Interaction(object):
    
    """ Concept of Interaction for Haroun. """
        
    def __init__(self, stimulus):
        
        """ 
            Interaction class constructor.
            
            Interaction concept class, manage interaction infos.
            
            Parameters
            ----------
            stimulus : Stimulus
                Stimulus at the origin of the interaction.
            
            
            Returns
            _______
            void
            
        """
        
        # ! Attributs
        
        # Error flag.
        self.error = False
        
        # Interaction duration
        self.duration = None
        
        # Intent : Intent that match the Interaction (defined by Recognition)
        self.intent = Intent(stimulus)
        # Response : Interaction Response.
        self.response = Response()

        # Skills list for interaction execution.
        self.skills = []
        
        # Interaction state of mind.
        self.mind = None
        

    # Fonctions de manipulations : 
    
    def add_response(self, raw_text):
        
        """
            Add response to response object.
            ---
            Parameters
                raw_text : String
                    Response raw text.
            ---
            Return
                None
        """
        # Add raw_text to response object.
        self.response.add_raw_text(raw_text)
        
        # Done flag.
        self.done = True
        
    
    def add_error(self, error_text):
        
        """
            Add error text to response object.
            ---
            Parameters
                error_text : String
                    Error message.
            ---
            Return
                None
        """
        
        # Add error_text to response object.
        self.response.add_error(error_text)
        
        # Flag error.
        self.error = True



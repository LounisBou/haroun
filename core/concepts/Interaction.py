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
        # Done flag.
        self.done = False
        
        # Interaction duration
        self.duration = None
        # Interaction stimulus.
        self.stimulus = stimulus   
        # Sentence words list.
        self.words = self.stimulus.sentence.split(' ')
        
        # Recognition : Recognition Dict from NLU recognize.
        self.recognition = None
        
        # Intent : Intent that match the Interaction (defined by Recognition)
        self.intent = Intent()
        # Response : Interaction Response.
        self.response = Response()
        
        # Domain matching intent.
        self.domain = None
        # Skill for interaction execution.
        self.skill = None
        
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

    
    def contains_word(self, word):

        # On parcours la liste de mots.
        for i in range(0,len(self.words)):
            # Récupération du mot courant.
            current = self.mots[i]
            # Test de correspondance du mot (minuscule)
            if(current.lower() == mot.lower()):
                return i
        return -1
    
    # Detect : retourne la position du mot trouvé, -1 sinon.
    def detect(self, mots):
        # On parcours la liste de mots à controller.
        for i in range(0,len(mots)):
            # Récupération du mot courant.
            current = mots[i]
            # On analyse la présence d'un mot dans la question.
            contentPosition = self.contient(current)
            # Si question possède le mot
            if(contentPosition != -1):
                return contentPosition
        return -1


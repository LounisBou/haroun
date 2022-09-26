#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
from core.Mouth import CURRENT_PATH
from core.concepts.Domain import Domain 
# Random library import.
import random
#
#
# Domain globals : 
#
# Needed slots list.
SLOTS_FILES = []
#
# ! DOMAIN 
#
class Social(Domain):
    
    def __init__(self):
        
        """ Class constructor. """
                
        # Init parent class Domain.
        super().__init__()
        

    
    @Domain.match_intent("social.whatsup")
    def whatsup(self, whatsup, hi = None, orphan = None):
        
        """ 
            whatsup : 
            ---
            Parameters
                whatsup : String
                    
                hi : String (optionnal)
                    
                orphan : String (optionnal)
                    
        """
        
        # Return a response dialog.
        return self.dialog.get_dialog("social.whatsup.good")
    
    @Domain.match_intent("social.hi")
    def hi(self, hi, orphan = None):
        
        """ 
            hi : 
            ---
            Parameters
                hi : String
                    
                orphan : String (optionnal)
                    
        """

        # Add context.
        
        # Return a response dialog.
        return self.dialog.get_dialog("social.hi")
    
    @Domain.match_intent("social.bye")
    def bye(self, bye, orphan = None):

        """ 
            bye : 
            ---
            Parameters
                bye : String
                    
                orphan : String (optionnal)
                                        
        """

        # Return a response dialog.
        return self.dialog.get_dialog("social.bye")

    @Domain.match_intent("social.good")
    def good(self, good, orphan = None):

        """ 
            good : 
            ---
            Parameters
                good : String
                    
                orphan : String (optionnal)
                                        
        """

        # Return a response dialog.
        return self.dialog.get_dialog("social.good")

    @Domain.match_intent("social.bad")
    def bad(self, good, orphan = None):

        """ 
            bad : 
            ---
            Parameters
                bad : String
                    
                orphan : String (optionnal)
                                        
        """

        # Return a response dialog.
        return self.dialog.get_dialog("social.bad")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
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

        # Initialisation.
        
        # Load config file.
        #self.load_config()

        # Load dialogs file.
        self.load_dialogs()

        
    def __get_lang(self, lang_entry_code):
        
        """ 
            __get_lang : Get language string by code. Provide random string if code entry value is list.
            ---
            Parameters 
                lang_entry_code : String
                    Language entry code.
            ---
            Return String
                Language string.
        """
        
        # Get current language entry code value.
        lang_entry_value = LANGUAGES[LANG_CODE][lang_entry_code]
        
        # If language entry value is list.
        if type(lang_entry_value) == list :
            # Return random value.
            return random.choice(lang_entry_value)
        else:
            # Return value.
            return lang_entry_value
    
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
        return self.get_dialog("social.whatsup.good")
    
    @Domain.match_intent("social.hi")
    def hi(self, hi, orphan = None):
        
        """ 
            hi : 
            ---
            Parameters
                hi : String
                    
                orphan : String (optionnal)
                    
        """
        
        # Return a response dialog.
        return self.get_dialog("social.hi")
    
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
        return self.get_dialog("social.bye")

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
        return self.get_dialog("social.good")

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
        return self.get_dialog("social.bad")
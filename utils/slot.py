#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import os.path
from os import path
# Import system library.
from sys import path as syspath
# Import logging library
import logging
#
# Gloabls : 
#
# Current, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
ROOT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
#
class Slot():

    """ Slot utils for slot loading and saving. """

    def __init__(self, lang, slot_name = None):

        """ 
            Class constructor. 
            ---
            Parameters
                lang : String
                    Language to use for slot.
                slot_name : String (optionnal)
                    Slot name to load. [Default : None]
        """

        # Define slot data.
        self.data = {}

        # Define language.
        self.lang = lang

        # Load slot if slot_name provided.
        if slot_name:
            self.load_slot_file(slot_name)
        

    def load_slot_files(self, slot_names):

        """ 
            Load slot files.
            ---
            Parameters
                slot_names : List
                    List of slot names to load.
        """

        # For each slot name.
        for slot_name in slot_names:
            self.load_slot_file(slot_name)


    def load_slot_file(self, slot_name):
        
        """ 
            Acquire a slot file and append slot data in dict. 
            ---
            Parameters 
                slot_name : String 
                    Slot name use to find slot file name to load.
        """
        
        # Slots directory path.
        slot_file_path=f"{ROOT_PATH}slots/{self.lang}/{slot_name.lower()}"
        
        """ Create slot entries dict from slot file. """
        
        # Check if slot file exist.
        if path.exists(slot_file_path):
            
        # Retrieve slot file content.
            with open(slot_file_path) as fileBuffer:
                
                # Read file lines. 
                fileLines = fileBuffer.readlines()
                
                # For each lines.
                for line in fileLines :
                    
                    # Split line on ':'
                    entry_parts = line.split(':')
                    
                    # If split is ok.
                    if len(entry_parts) == 2 :
                        slot_entry_key = entry_parts[1]
                    else:
                        slot_entry_key = entry_parts[0]

                    try:

                        # Create slot_entry_key from second part.
                        slot_entry_key = slot_entry_key.strip().replace("(", "").replace(")", "")
                        slot_entry_key = slot_entry_key.strip()
                        
                        # Create slot_entry_value from second part.
                        slot_entry_value = entry_parts[0].strip().replace("(", "").replace(")", "")
                        slot_entry_value = slot_entry_value.split('|')
                        slot_entry_value = slot_entry_value[0]
                        slot_entry_value = slot_entry_value.replace("[", "").replace("]", "")
                        slot_entry_value = slot_entry_value.strip()
                        
                        # Set second part as key, first part as value.
                        self.data[slot_entry_key] = slot_entry_value
                        
                    except:
                        # [LOG]
                        logging.error(f"Slot line can't be interpreted. File slot {slot_file_path} error on : {line}")
        else:
            # [LOG]
            logging.error(f"Slot file {slot_file_path} not found.")

    
    def get(self, key):
        
        """ 
            Get slot value from key.
            ---
            Parameters
                key : String
                    Key to get value from.
        """
        
        # Return slot value.
        return self.data[key]

    def get_reverse(self, value):
        
        """ 
            Get slot key from value.
            ---
            Parameters
                value : String
                    Value to get key from.
        """
        
        # For each slot data.
        for key, slot_value in self.data.items():
            
            # If slot value match.
            if slot_value == value:
                
                # Return key.
                return key
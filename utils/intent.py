#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import os.path, os.walk
from os import path, walk
# Import system library.
from sys import path as syspath
# Import pathlib.Path for rhasspynlu.parse_ini
from pathlib import Path
# Import rhasspynlu
import rhasspynlu
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
class Intent():

    """ Intent utils for intent loading. """

    @staticmethod
    def get_rhasspy_intent_list(lang):

        """ 
            Acquire intents file list and create a all.ini intents file. 
            Parse haroun/intents folder to list of intents file.
            Normally one file per available domains.
            Generate one intents file and parse it with rhasspy-nlu.
            ---
            Return : intents 
                Rhasspy NLU intents list.
        """
        
        # Intents directory path.
        intents_path=f"{ROOT_PATH}intents/{lang}/"
        
        # Browse through intents files 
        intents_files = []    
        for(dir_path, dir_names, file_names) in walk(intents_path):
            # [LOG]
            logging.debug(f"Looking in intent directory : {intents_path}, listing files : \n{file_names}")
            intents_files.extend(file_names)
            break
            
        """ Write all intents in intents/.all.ini file. """
        
        # Open intents/.all.ini, a file that will contains all intents.
        all_intents_file_path  = intents_path+".all.ini"
                    
        # Open intents/.all.ini in write mode
        with open(all_intents_file_path, 'w+') as all_intents_file_buffer:
            
            # Iterate through intents_files list
            for file_name in intents_files:
                
                # Ignore .all.ini file.
                if file_name != ".all.ini":

                    # Construct file path.
                    file_path = intents_path+file_name
                    
                    # Open each file in read mode
                    with open(file_path) as file_buffer:
        
                        # Read the data from file. 
                        file_intents = file_buffer.read()
                        
                        # Write it in all_intents_file_buffer and add '\n\n' to enter data from next line
                        all_intents_file_buffer.write("# "+file_name+" file content : \n")
                        # Lowercase all intents.
                        all_intents_file_buffer.write(file_intents.lower()+"\n\n")
                    
                            
        # Load file for rhasspy-nlu.
        intents = rhasspynlu.parse_ini(Path(all_intents_file_path))
        
        # Return
        return intents
    
    


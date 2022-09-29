#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies :
#
# Import sys.path as syspath
from sys import path as syspath
# Import os.path, os.walk
from os import path, walk
# Import pathlib.Path for rhasspynlu.parse_ini
from pathlib import Path
# Import rhasspynlu
import rhasspynlu
# Import logging
import logging
# Import utils debug functions.
from utils.debug import *
#
#
# Gloabls : 
#
# Current, parent, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
PARENT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
ROOT_PATH = path.dirname(path.abspath(PARENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
#
class Intent(object): 
    
    """ Concept of Haroun Intent. """

    # Intents files path dict.
    intents_files_path = []

    # Intents list.
    intents = []

    # Intents graph.
    graph = None

    # Intent recognize fuzzy mode.
    fuzzy_mode = True


    def __init__(self):
        
        """ Intent class constructor. """
        
        # Error flag.
        self.error = 0
        
        # Recognition
        self.recognition = None
        
        # Raw text
        self.raw_text = None
        # Interpreted text
        self.text = None      
        # Label.
        self.label = None
        # Confidence.
        self.confidence = None
        # Entities
        self.entities = None
        # Orphan entity value
        self.orphan_text = None
        # Tokens
        self.tokens = None
        # Raw tokens
        self.raw_tokens = None

        # Arguments dict.
        self.kwargs = {}
        
        # Ponctuation counter :
        self.ponctuation_marks = {
            # Period.
            '.' : 0,
            # Question mark.
            '?' : 0,
            # Exclamation mark.
            '!' : 0,
            # Comma.
            ',' : 0,
            # Colon.
            ':' : 0,
            # Semicolon
            ';' : 0,
        }
    
    def __str__(self):
        
        """ Intent print method. """
        
        # Text
        print_str = f"\n"
        print_str += f"  label : {str(self.label)} \n"
        print_str += f"  raw_text  : {str(self.raw_text)} \n"
        print_str += f"  interpreted text : {str(self.text)} \n"
        #print_str += f" confidence  : {str(self.confidence)} \n"
        print_str += f"  entities  : \n"
        if self.entities : 
            print_str += "\n".join(["    - "+str(entity['entity'])+" : "+str(entity['value']) for entity in self.entities])+"\n"
        #print_str += f"tokens  : \n"
        #if self.tokens : 
            #print_str += "\n".join([str(token) for token in self.tokens])+"\n"
        #print_str += "raw_tokens  : \n"
        #if self.raw_tokens : 
            #print_str += "\n".join([str(raw_token) for raw_token in self.raw_tokens])+"\n"
            
        # Ponctuation counter :
        for key, value in self.ponctuation_marks.items():
            if value > 0 :
                print_str += f"    - {key} = {value} \n"
        
        print_str += f"\n"
        
        
        return print_str
        
    
    """ NLU methods. """

    @staticmethod
    def __get_intent_files_from(intent_dir_path):

        """
            Return list of intents files in path.
            ---
            Parameters :
                path : str
                    Path to look for intents files.
            ---
            Returns : list
                List of intents files path.
        """

        # Check if path exists.
        if path.exists(intent_dir_path):

            # Create list of files path for domains intents.
            intent_files = []  

            # Browse through domains intents files   
            for dir_path, dir_names, file_names in walk(intent_dir_path):
                # Remove hidden files.
                file_paths = [path.join(dir_path, file_name) for file_name in file_names if not file_name.startswith('.')]
                # [LOG]
                logging.debug(f"Looking in intent directory : {intent_dir_path}")
                logging.debug(f"Listing intents files : \n{file_names}")
                # Add domains intents dir files to list.
                intent_files.extend(file_paths)
                # End of loop.
                break

            # Return list of intents files.
            return intent_files
            
        else:
            # [LOG]
            logging.error(f"Path {path} does not exists.")
            # Return empty list.
            return []

    @classmethod
    def scan_domain_intents(cls, domain_name, lang):

        """ 
            Look for domain intents files in domain directory.
            Add domain intents files path to self.domains_intents_files_path dict.
            ---
            Parameters :
                domain_name : str
                    Domain name.
                lang : str
                    Language.
        """

        # Intents directory path.
        domain_intents_path=f"{ROOT_PATH}domains/{domain_name.lower()}/{lang}/intents/"

        # Add list of files to intents files path list.
        cls.intents_files_path.extend(Intent.__get_intent_files_from(domain_intents_path))

    @classmethod
    def load_intents(cls, domains, lang):

        """ 
            Acquire intents file list and create a all.ini intents file. 
            Parse haroun/intents folder to list of intents file.
            Normally one file per available domains.
            Generate one intents file and parse it with rhasspy-nlu to create Rhasspy NLU intents list.
            ---
            Parameters :
                domains : list
                    List of domains.
                lang : str
                    Language.
        """
        
        """ Scan intent to fill intents_files_path list. """

        # Intents directory path.
        haroun_intents_path = f"{ROOT_PATH}intents/{lang}/"

        # Get haroun intents files list.
        cls.intents_files_path.extend(Intent.__get_intent_files_from(haroun_intents_path))  
        # Get domains intents files list.
        for domain_name in domains :
            # Scan domain intents files and add them to intents files path list.
            cls.scan_domain_intents(domain_name, lang)
            
        """ Write all intents in intents/.all.ini file. """

        # Open intents/.all.ini, a file that will contains all intents.
        all_intents_file_path  = haroun_intents_path+".all.ini"
                    
        # Open intents/.all.ini in write mode
        with open(all_intents_file_path, 'w+') as all_intents_file_buffer:

            # Iterate through intents_files list
            for file_path in cls.intents_files_path:
                
                # Ignore .all.ini file.
                if file_path != all_intents_file_path:
                    
                    # Open each file in read mode
                    with open(file_path) as file_buffer:
        
                        # Read the data from file. 
                        file_intents = file_buffer.read()
                        
                        # Write it in all_intents_file_buffer and add '\n\n' to enter data from next line
                        all_intents_file_buffer.write("# "+file_path+" file content : \n")
                        # Lowercase all intents.
                        all_intents_file_buffer.write(file_intents.lower()+"\n\n")
                    
                            
        # Load file for rhasspy-nlu.
        cls.intents = rhasspynlu.parse_ini(Path(all_intents_file_path))

    @classmethod   
    @debug("verbose", True)
    #@lru_cache(maxsize=128, typed=True)  
    def create_graph(cls, slot_replacements):
        
        """ 
            Acquire domains knowledge. 
            Transform intents into graph training, replace slots if necessary.
            ---
            Parameters :
                slot_replacements : list
                    List of slot replacements.
        """
        
        # Generate intents training graph from list of known intents.
        cls.graph = rhasspynlu.intents_to_graph(cls.intents, replacements = slot_replacements)
    
    
    @debug("verbose", True) 
    def recognize(self, sentence):
        
        """ 
            Apply NLU analysis on sentence, try to retrieve a recognition dict.
            ---
            Parameters
                sentence : String
                    Sentence to analyse.
            ---
            Return : boolean 
                Sentence recognition success, if True recognition and intent attributs are now defined.
        """
        
        # [LOG]
        logging.debug(f"Interaction sentence : {sentence}\n\n")
                
        # Perform intent recognition in Interaction intent sentence thanks to training graph.
        try:
            recognition = rhasspynlu.recognize(
                sentence, 
                Intent.graph, 
                fuzzy=Intent.fuzzy_mode
            )
        except ZeroDivisionError :
            # Return
            return False

        # [LOG]
        logging.debug(f"Raw recognition : {recognition}\n\n")
            
        # Sentence recognition failed.
        if not recognition :
            # [LOG]
            logging.info("Sentence recognition failed. No intent found for this sentence.")
            # Return
            return False

        # If intent found, parse recognition infos.
        else:
            
            # Format recognition as Object.
            recognition = recognition[0].asdict()

            # [LOG]
            logging.debug(f"Intent recognition : {recognition}\n\n")
            logging.debug(f"Intent recognition entities : {recognition['entities']}")

        # If recognition successful (intent found).
        if recognition :

            # Parse recognition infos.
            self.checkRecognition(recognition)

        # Return
        return recognition  
    
    def checkRecognition(self, recognition):
        
        """ 
            Check recognition to define intent info. 
            
            Try to define the intent attributs (label, entities, tokens...) from recognition Object.
            ---
            Parameters :
                recognition : Recognition
                    Recognition Object generated from Interaction interpretation.
        """
        
        # Recognition
        self.recognition = recognition
        
        # Text
        self.text = recognition['text']
        # Raw text
        self.raw_text = recognition['raw_text']
        # Label.
        self.label = recognition['intent']['name']
        # Confidence.
        self.confidence = recognition['intent']['confidence']
        # Entities
        self.entities = recognition['entities']
        # Tokens
        self.tokens = recognition['tokens']
        # Raw tokens
        self.raw_tokens = recognition['raw_tokens']


    """ Arguments methods. """

    def get_args(self, skill_params):

        """ 
            Get arguments from entities and orphan.
            ---
            Parameters :
                skill_params : list
                    List of skill parameters.
            ---
            Return : dict
                Dict of arguments.    
        """

        # If there is entities.
        if self.entities :
            # Check entities to create kwargs.
            for entity in self.entities :
                # If entity is not already in kwargs.
                if entity['entity'] not in self.kwargs.keys() :
                    # Add entity to kwargs.
                    self.kwargs[entity['entity']] = entity['value']
        
        # Add orphan to kwargs.
        self.__get_orphan(skill_params)

        # Return kwargs.
        return self.kwargs

    def __get_orphan(self, skill_params):
        
        """ 
            Get orphan entity value. 
            Entity is orphan if it is not in skill parameters.
            If no orphan entity, orphan_text is declare as orphan.
            ---
            Parameters :
                skill_params : list
                    List of skill parameters.
        """

        # Create orphan argument.
        self.kwargs['orphan'] = None

        # For each intent argument.
        for arg_key, arg_value in self.kwargs.items() :
            # If argument is not in skill parameters.
            if arg_key not in skill_params :
                # Define orphan entity value.
                self.kwargs['orphan'] = arg_value
                # Remove argument value.
                self.kwargs[arg_key] = None

        # Orphan entity value
        self.orphan_text = self.raw_text.lower()

        # Trim orphan entity.
        self.orphan_text = self.__clean_entity_value(self.orphan_text)

        # If orphan_text is not empty and orphan argument not already defined..
        if self.orphan_text and not self.kwargs['orphan'] :
            # Add orphan to kwargs.
            self.kwargs['orphan'] = self.orphan_text

        # If orphan is empty or None.
        if not self.kwargs['orphan'] :
            # Remove orphan from kwargs.
            del self.kwargs['orphan']

    def __clean_entity_value(self, entity_value):
        
        """ Clean entity value. """
        
        # Remove ponctuation marks.
        for ponctuation_mark in self.ponctuation_marks.keys():
            # If present.
            if ponctuation_mark in entity_value :
                # Remove ponctuation mark.
                entity_value = entity_value.replace(ponctuation_mark, "")
                # Increase counter
                self.ponctuation_marks[ponctuation_mark] += 1
        
        # Trim orphan entity.
        entity_value = entity_value.strip()
        
        # Return cleaned entity value.
        return entity_value
                
        
        
        
        

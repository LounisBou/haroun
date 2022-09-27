#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies :
#
# Import logging
import logging
#
#
# Globals :
#
#
#
#
class Intent(object): 
    
    """ Concept of Haroun Intent. """
    
    def __init__(self, stimulus):
        
        """ Intent class constructor. """
        
        # Error flag.
        self.error = 0
        
        # Stimulus
        self.stimulus = stimulus
        # Recognition
        self.recognition = None
        
        # Text
        self.text = None
        # Raw text
        self.raw_text = None
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
        if self.stimulus :
            print_str += f"  stimulus text : {self.stimulus.sentence} \n"
        print_str += f"  interpreted text : {str(self.text)} \n"
        print_str += f"  raw_text  : {str(self.raw_text)} \n"
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
        
    
    # ! - Initialisation.
    
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
        self.orphan_text = self.stimulus.sentence.lower()

        # If raw text is not empty.
        if self.raw_text :
            # Remove raw text from orphan.
            self.orphan_text = self.orphan_text.replace(self.raw_text, "")

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
                
        
        
        
        

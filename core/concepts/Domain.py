#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import system library.
from locale import currency
from sys import path as syspath
# Import os.path
from os import path
# Import Python Object Inspector library.
import inspect
# Import logging library
import logging
# Import functools wraps for decorators.
from functools import wraps
# Import configparser.
from configparser import ConfigParser
from tkinter.messagebox import NO
# Import DialogParser.
from utils.dialogParser import DialogParser
# Import Context class.
from core.concepts.Context import Context
# Import Memory class.
from core.concepts.Memory import Memory
# Import random.
from random import choice
# Import json.
import json
# [DEBUG] Import pretty formatter.
from prettyformatter import pprint
#
#
# Globals :
#
# Current, parent, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
PARENT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
ROOT_PATH = path.dirname(path.abspath(PARENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
#
#
class Domain(object):
    
    """ Concept of Haroun Domain. """
    
    # Static variables :
    
    # Store intents handlers for each instanciate domains
    intents_handlers = {}
    
    # Fonction : Constructeur
    def __init__(self):
        
        """ Domain class constructor. """ 
        
        # Get domain class name.
        self.domain_class_name = type(self).__name__

        # Configuration file
        self.config_file_name = f"{self.domain_class_name.lower()}.ini"
        
        # Dialogs file name.
        self.dialogs_file_name = f"{self.domain_class_name.lower()}.dialogs"
        
        # Config dict.
        self.config = {}

        # Dialogs dict.
        self.dialogs = {}
        
        # Load Haroun config file.
        self.load_config("haroun.ini")
        
        # Set logging level.
        logging.getLogger().setLevel(self.config['haroun']['LOG_LEVEL'])
                
        # Slots entries.
        self.slots_entries = {}

        # Initialisation.
        
        # Load config file.
        self.load_config()

        # Load dialogs file.
        self.load_dialogs()

        # Use context intent lifespan if exist.
        self.check_intent_lifespan()

    
    def load_config(self, config_file_name = None):
        
        """ 
            Get config from config/{config_file_name} 
            ---
            Parameters
                config_file_name : String (optionnal)
                    Domain config file name if not same name as domain class name.
        """
        
        # Check if config_file_name, else use class default.
        if not config_file_name :
            config_file_name = self.config_file_name
        
        # Domain config file path.
        domain_config_file_path = f"{ROOT_PATH}config/{config_file_name}"
        
        # Check if config exist.
        if path.exists(domain_config_file_path):
        
            # See configparser 
            configParser = ConfigParser()
        
            # Parse domain config file.
            configParser.read(f"{domain_config_file_path}")
                        
            # Get config parser sections.
            sections = configParser.sections()
            
            # Get all sections.
            for section_name in sections:
                self.config[section_name] = configParser[section_name]
                
        else:
            # [LOG]
            logging.error(f"Error config file {domain_config_file_path} doesn't exist.")
    
    def __get_slot(self, slot_file_name):
        
        """ 
            Acquire a slot file and return all slot entries in dict. 
            ---
            Parameters 
                slot_file_name : String 
                    Slot file name
            ---
            Return : Dict
                Dict of Slots in file.
        """
        
        # Slots directory path.
        slots_path=f"{ROOT_PATH}slots/{self.config['haroun']['lang']}/"
        
        """ Create slot entries dict from slot file. """
        
        # Slot entries dict.
        slot_entries = {}

        # Construct file path.
        slot_file_path = slots_path+slot_file_name
            
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
                    slot_entries[slot_entry_key] = slot_entry_value
                    
                except:
                    # [LOG]
                    logging.error(f"Slot line can't be interpreted. File slot {slot_file_name} error on : {line}")
        
        # Return slot_entries
        return slot_entries
        
    def get_slots_entries(self, slots_files_names):
        
        """
            Retrieve slots entries from specified slots files names.
            Add entries to self.slots_entries.
            ---
            Parameters
                slots_files_names : List
                    List of slots files names to import.
        """
        
        # Retrieve slots entries for each specified files.
        for slot_file_name in slots_files_names :
        
            # Use Domain static method getSlot to get slot file entries.
            slot_entries = self.__get_slot(slot_file_name)
            
            # [LOG]
            logging.debug(f"Slot file {slot_file_name} entries : {slot_entries}\n")
            
            # Add slot_entries to self.slots_entries dict.
            self.slots_entries.update(slot_entries)

    def load_dialogs(self, domain_class_name = None):
        
        """
            Retrieve dialog from domain dialogs file, add dialogs to dialogs dict.
            ---
            Parameters
                domain_class_name : String
                    Domain dialogs file name, if you want to override it. [Default : None]
        """

         # Check if domain_class_name, else use class default.
        if domain_class_name :
            dialogs_file_name = self.domain_class_name.lower()+".dialogs"
        else:
            dialogs_file_name = self.dialogs_file_name
        
        # Dialogs directory path.
        dialogs_path=f"{ROOT_PATH}dialogs/{self.config['haroun']['lang']}/"

        # Domain dialogs file path.
        domain_dialog_file_path = f"{ROOT_PATH}dialogs/{self.config['haroun']['lang']}/{dialogs_file_name}"
        
        # Check if dialogs exist.
        if path.exists(domain_dialog_file_path):
        
            # Use configparser to read dialogs file.
            dialogsParser = DialogParser()
        
            # Parse domain dialogs file.
            dialogsParser.read(f"{domain_dialog_file_path}")

            # Get all sections.
            for section_name in dialogsParser.sections():
                dialog_section = dialogsParser[section_name]
                self.dialogs[section_name] = []
                # Get all dialogs.
                for dialog in dialog_section.items():
                    # If dialog contains ':' it may be cut in tupple.
                    if not dialog[1] :
                        self.dialogs[section_name].append(dialog[0])
                    else:
                        # Add dialog to self.dialogs[section_name] list.
                        self.dialogs[section_name].append(' : '.join(dialog))

            # [LOG]
            logging.debug(f"Dialogs : {self.dialogs[section_name]}")
                
        else:
            # [LOG]
            logging.error(f"Error config file {domain_dialog_file_path} doesn't exist.")
             

    def get_dialog(self, dialog_key, random = True):
        
        """
            Retrieve dialog self.dialogs.
            ---
            Parameters
                dialog_key : String
                    Dialog section key name.
                random : Boolean
                    If True, return a random dialog from section. [Default : True]
            ---
            Return : String
                Dialog sentence.
        """
                
        # Random dialogs
        if random :
            dialog = choice(self.dialogs[dialog_key])
        else:
            dialog = self.dialogs[dialog_key][0]

        # Replace "" by space, manage empty dialog.
        dialog = dialog.replace('""', ' ')

        # Capitalize first letter.
        dialog = dialog[0].upper() + dialog[1:]

        # Return dialog.
        return dialog
        
    def get_method_args(self, method_name):
        
        """
            Get methods arguments list as tuple.
            ---
            Parameters : 
                method_name : String
                    Method name in domain instance.
            ---
            Return Tuple
                Method arguments.
        """ 
        
        # Get Skill method.
        method = getattr(self, method_name)
        
        # Retrieve method arguments.
        args = inspect.getargspec(method).args
        
        # Return methods args.
        return args
        
    
    def execute_skill(self, skill):
        
        """
            Execute the skill on a domain class method.
            ---
            Parameters : 
                skill : Skill
                    Skill to execute.
            ---
            Return skill : modified skill.
        """ 
        
        # Get methods.
        method = getattr(self, skill.method_name)
        
        # [LOG]
        logging.info(f"Skills parameters = {skill.parameters}")
        
        # Execute methods with skill parameters
        skill.return_values = method(**skill.parameters)
        
        # Return modified skill
        return skill
    
    @staticmethod
    def register_handled_intent(module_name, class_name, method_name, intent_name):
        
        """
            Register domain method that handle an intent with Domain.match_intent decorator.
            ---
            Parameters
                module_name : String
                     Domain module name that match the intent.
                class_name : String
                     Domain class name that match the intent.
                method_name : String
                    Domain method name that match the intent.
                intent_name : String
                    Name of the intent to match.
        """
                
        # If intent_name entry don't exist. 
        if intent_name not in Domain.intents_handlers.keys() :
            # Declare new list of skill method for intent_name.
            Domain.intents_handlers[intent_name] = []
        else:    
            # [LOG]
            logging.warning(f"Intent handler for {intent_name} already exist. Handler is added to the list.")  

        # Add intent handler entry in intents_handlers.
        Domain.intents_handlers[intent_name].append({
            "module" : module_name,
            "class" : class_name,
            "method" : method_name,
        })
        
    # ! Context methods.

    @classmethod
    def check_intent_lifespan(cls):

        """ Decrease intent lifespan if exist. """
        
        # Check if intent exist in context.
        if context_intent := cls.get_context_intent() :

            # [LOG]
            logging.info(f"Context intent : {context_intent}")

            # Remove 1 to intent lifespan.
            if context_intent['lifespan'] > 0 :
                # [LOG]
                logging.info(f"Context intent lifespan will decrease by 1.")
                context_intent['lifespan'] = cls.__reduce_context_intent_lifespan()

            # If intent lifespan is 0, remove content intent.
            if context_intent['lifespan'] == 0 :
                # [LOG]
                logging.info(f"Intent lifespan is 0, remove context intent.")
                cls.remove_context_intent()

        else:

            # [LOG]
            logging.info(f"No context intent.")


    @classmethod
    def set_context_intent(cls, intent_name, args={}, lifespan = 1):

        """
            Set intent in context.
            ---
            Parameters
                intent_name : String
                    Intent name to set.
                lifespan : Integer
                    Intent lifespan. [Default : 1]
        """

        # Set intent in context.
        Context.add("intent", intent_name)

        # Add intent args to context.
        Context.add("intent_args", json.dumps(args))

        # Add intent lifespan to context.
        Context.add("intent_lifespan", lifespan)

    @classmethod
    def get_context_intent(cls):

        """
            Get intent from context.
            ---
            Return : dict
                Intent description, none if no context intent.
        """
        
        # Check if intent exist in Context.
        if context_intent := Context.get("intent") :
            return {
                "name": context_intent.value,
                "args": cls.__get_context_intent_args(),
                "lifespan": cls.__get_context_intent_lifespan()
            }
        else:
            return None

    @classmethod
    def __get_context_intent_args(cls):

        """
            Get intent args in Context.
            ---
            Return : Dict
                Intent args.
        """

        # Check if intent exist in Context.
        if intent_args := Context.get("intent_args") :
            return json.loads(intent_args.value)
        else:
            return 0

    @classmethod
    def __get_context_intent_lifespan(cls):

        """
            Get intent lifespan in Context.
            ---
            Return : Integer
                Intent lifespan.
        """

        # Check if intent exist in Context.
        if intent_lifespan := Context.get("intent_lifespan") :
            return int(intent_lifespan.value)
        else:
            return 0

    @classmethod
    def __reduce_context_intent_lifespan(cls):

        """
            Reduce intent lifespan by 1.
            ---
            Return : Integer
                Nex intent lifespan.
        """

        # Get context intent lifespan.
        context_intent_lifespan = cls.__get_context_intent_lifespan()

        # New intent lifespan.
        new_intent_lifespan = context_intent_lifespan - 1

        # Reduce context intent lifespan by 1.
        Context.add("intent_lifespan", new_intent_lifespan)

        # Return new intent lifespan.
        return new_intent_lifespan

    @classmethod
    def remove_context_intent(cls):

        """
            Remove intent from context.
        """

        # Remove intent from context.
        Context.remove("intent")
        # Remove intent args from context.
        Context.remove("intent_args")
        # Remove intent lifespan from context.
        Context.remove("intent_lifespan")

    
    def set_context(self, key, value, duration = None):
        
        """
            Set context value.
            ---
            Parameters
                key : String
                    Context key.
                value : String
                    Context value.
                duration : Integer
                    Context duration in seconds. [Default : None]
        """
        
        # Set context value.
        Context.add(key, value, self.domain_class_name.lower(), duration)

    def get_context(self, key):

        """
            Get context value.
            ---
            Parameters
                key : String
                    Context key.
            ---
            Return : String
                Context value or None if not found.
        """

        # Get context value.
        context = Context.get(key, self.domain_class_name.lower())
        if context:
            return context.value
        else:
            return None

    # ! Decorators :
    
    @staticmethod
    def match_intent(intent_name, auto_affect_orphans = True):
        
        """
            Decorator that allow a domain method to match a specific intent.
            ---
            Parameters
                intent_name : String
                    Name of intent to match.
            ---
            Return Function
                Decorator inner function.
        """
        
        def inner_function(function):
            
            """
                inner_function that received the original function in parameters.
                --- 
                Parameters
                    function : Function
                        Domain method on which the decorator was applied.
                ---
                Return Function
                    Decorator function wrapper
            """
        
            @wraps(function)
            def wrapper(self_instance, *args, **kwargs):
                
                """
                    match_intent wrapper function. Execute decorator code.
                    ---
                    Parameters
                        self_instance : Class instance
                            Domain instance on which method have been called.
                        *args : List
                            List of arguments pass on function call.
                        *kargs : Dict
                            Dict of arguments_names : arguments pass on function call.
                    ---
                    Return : result of function call.
                """
                
                # Get function arguments list.
                args_list = inspect.getargspec(function).args
                
                # Define orphan use.
                if auto_affect_orphans and "orphan" in args_list and "orphan" in kwargs.keys() :
                    for arg_name in args_list:
                        if arg_name is not "self" and arg_name not in kwargs.keys() :
                            orphan = kwargs["orphan"]
                            logging.info(f"Argument {arg_name} not defined, set to orphan value : {orphan}")
                            kwargs[arg_name] = orphan
                            break
                
                # Call the original function.
                result = function(self_instance, *args, **kwargs)
                
                # Return result.
                return result
            
            # Try to maintain method signature.
            wrapper.__signature__ = inspect.signature(function)  # the magic is here!
            
            # Get all function infos for registering intent handler.
            module_name = function.__module__.split('.')[1]
            class_name = function.__qualname__.split('.')[0]
            method_name = function.__qualname__.split('.')[1]
            
            # [LOG]
            logging.debug(f"Intent {intent_name} : handling by {module_name}.{class_name}.{method_name}")
                 
            # Registering function as intent handler.
            Domain.register_handled_intent(module_name, class_name, method_name, intent_name)
                        
            # Return the wrapper function.
            return wrapper
                    
        # Return inner_function
        return inner_function

    
    @staticmethod
    def check_api_connection(api_var_name):
        
        """
            Decorator that check if API connection is done.
            ---
            Parameters
                api_var_name : String
                    Name of domain variable that manage API connection.
            ---
            Return Function
                Decorator inner function.
        """
        
        def inner_function(function):
            
            """
                inner_function that received the original function in parameters.
                --- 
                Parameters
                    function : Function
                        Domain method on which the decorator was applied.
                ---
                Return Function
                    Decorator function wrapper
            """
        
            @wraps(function)
            def wrapper(self_instance, *args, **kwargs):
                
                """
                    match_intent wrapper function. Execute decorator code.
                    ---
                    Parameters
                        self_instance : Class instance
                            Domain instance on which method have been called.
                        *args : List
                            List of arguments pass on function call.
                        *kargs : Dict
                            Dict of arguments_names : arguments pass on function call.
                    ---
                    Return : result of function call.
                """
                
                # Check API connection.
                if getattr(self_instance, api_var_name) is None:
                    # [LOG]
                    logging.error(f"API connection not done !")
                    return "La connexion API à échoué !"

                # Call the original function.
                result = function(self_instance, *args, **kwargs)
                
                # Return result.
                return result
            
            # Return the wrapper function.
            return wrapper
                    
        # Return inner_function
        return inner_function
    



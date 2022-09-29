#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import system library.
from sys import path as syspath
# Import os.path, os.scandir
from os import path, scandir
# Import Python Object Inspector library.
import inspect
# Import logging library
import logging
# Import functools wraps for decorators.
from functools import wraps
# Import Config utils.
from utils.config import Config
# Import concept Dialog.
from core.concepts.Dialog import Dialog
# Import Slot utils.
from core.concepts.Slot import Slot
# Import concept Context .
from core.concepts.Context import Context
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
        
        # Load config haroun and domain config.
        self.config = Config("haroun")
        self.config.load_config_file(self.domain_class_name)

        # Load domain slots.
        Slot.load_domain_slots(self.domain_class_name, self.config['haroun']['lang'])

        # Load domain dialogs.
        Dialog.load_domain_dialog_files(self.domain_class_name, self.config['haroun']['lang'])
        
        # Set logging level.
        logging.getLogger().setLevel(self.config['haroun']['LOG_LEVEL'])

        # Initialisation.

        # Use context intent lifespan if exist.
        self.check_context_intent()

    
    """ Domain methods. """

    @staticmethod
    def get_available_domain_list():
        
        """ Scan domains directory to find available domain list. """
        
        # Domain directory path.
        domain_dir_path = f"{ROOT_PATH}domains/"

        # List of available domains.
        domain_list = []

        # Browse through domains intents files   
        for entry in scandir(domain_dir_path):
            if entry.is_dir() and not entry.name.startswith('__'):
                # Check if directory is a valid domain.
                domain_dir_path = path.join(domain_dir_path, entry)
                domain_file_path = path.join(domain_dir_path, f"{entry.name.title()}.py")
                if path.isfile(domain_file_path):
                    domain_list.append(entry.name)
                else:
                    logging.warning(f"Domain '{domain_file_path}' not found.")
    
        # Get domain list.
        return domain_list
    
    """ Slots methods. """

    def getSlot(self, slot_name):

        """
            Get slot value.
            ---
            Parameters
                slot_name : String
                    Slot name.
            ---
            Return : String
                Slot value or None if not found.
        """

        # Get slot value.
        return Slot.get(slot_name)

    """ Dialogs methods. """

    def say(self, dialog_name, **kwargs):

        """
            Say dialog.
            ---
            Parameters
                dialog_name : String
                    Dialog name.
                **kwargs : Dictionary
                    Dialog arguments.
            ---
            Return : String
                Dialog text.
        """

        # Say dialog.
        return Dialog.say(dialog_name, **kwargs)

    """ Context methods. """

    @classmethod
    def check_context_intent(cls):

        """ Decrease intent lifespan if exist. """
        
        # Check if intent exist in context.
        if context_intent := cls.get_context_intent() :

            # [LOG]
            logging.debug(f"Context intent : {context_intent}")

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

    # ! Intents methods.

    @staticmethod
    def add_handled_intent(module_name, class_name, method_name, intent_name):
        
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

    @staticmethod
    def remove_handled_intent(intent_name):

        """
            Remove intent handler.
            ---
            Parameters
                intent_name : String
                    Name of the intent to remove.
        """

        # Remove intent handler.
        Domain.intents_handlers.pop(intent_name, None)

        

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
            Domain.add_handled_intent(module_name, class_name, method_name, intent_name)
                        
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
    



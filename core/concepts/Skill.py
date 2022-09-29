#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Imports :
#
# Import logging library
import logging
# Import importlib
import importlib
# Import Python Object Inspector library.
import inspect
# Import domains.
import domains 
for domain in domains.__all__:
    globals()[domain] = importlib.import_module(f"domains.{domain}.{domain.title()}")
#
#
class Skill(object):
    
    """ Concept of Haroun Skill. """
    
    def __init__(self, domain_module_name, domain_class_name, domain_method_name):
        
        """ Skill class constructor. """   
        
        # Domain module name the skill is link to.
        self.module_name = domain_module_name
        # Domain class name the skill is link to.
        self.class_name = domain_class_name
        # Domain method name the skill is link to.
        self.method_name = domain_method_name

        # Domain module the skill is link to.
        self.module = None
        # Domain class the skill is link to.
        self.cls = None
        # Domain method the skill is link to.
        self.method = None

        # Domain class instance.
        self.cls_instance = None
        
        # Skill exectution return values.
        self.return_values = None  

        # Skill execution parameters dict.
        self.kwargs = {}
        
        # Prepared skill flag.
        self.prepared = False
        
        # Skill exectution error flag.
        self.error = -1
    
    def __get_domain_class(self):
        
        """ Get domain class. """
        
        # Get domain module.
        self.module = globals()[self.module_name]

        # [LOG]
        logging.info(f"Domain module : {self.module}")

        # Get domain class.
        self.cls = getattr(self.module, self.class_name)
        

    def __get_domain_class_instance(self):

        """ Get domain class instance. """

        # Get domain class instance.
        self.cls_instance = self.cls()


    def __get_method(self):

        """ Get domain class method to execute."""

        # Get domain class method.
        self.method = getattr(self.cls_instance, self.method_name)

    def __get_method_params(self):

        """
            Get domain method parameters.
            ---
            Returns
                Tupple : Domain method parameters.
        """
        
        # Retrieve method arguments.
        method_params = inspect.getargspec(self.method).args

        # Remove self from method arguments.
        method_params.remove('self')

        # Add method arguments to skill kwargs.
        for param in method_params :
            self.kwargs[param] = None
    
    def __set_args_from_intent(self, intent, use_orphan=True):
        
        """
            Prepare skill for execution.
            Match intent with methods args to create skills execution parameters.
            ---
            Parameters
                intent : Intent
                    Interaction intent Object.
            ---
            Returns
                Boolean : Intent match method_args, skill is prepared.
        """

        # Get intent args.
        intent_args = intent.get_args(list(self.kwargs))

        # [LOG]
        logging.info(f"Intent args : {intent_args}")
        
        # Parse intent entities to create argument.
        for param, arg in intent_args.items() :
            # Check if param exist in method parameters.
            if param in self.kwargs.keys() :
                # Create argument.
                self.kwargs[param] = arg
        
        # [LOG]
        logging.info(f"Skill args before : {self.kwargs}")

        # Place orphan argument.
        if use_orphan :
            self.__place_orphan()
        
        # [LOG]
        logging.debug(f"Skill kwargs after : {self.kwargs}")

    def __place_orphan(self):

        """ Set orphan as first missing argument value. """

        # If orphan argument exist and has value.
        if 'orphan' in self.kwargs and self.kwargs['orphan'] :
            # Check first None value in arguments.
            for param, arg in self.kwargs.items() :
                # Check if argument is None.
                if arg is None :
                    # Set param to orphan value.
                    self.kwargs[param] = self.kwargs['orphan']
                    # [LOG]
                    logging.info(f"Argument {param} is None. Set to orphan value : {self.kwargs['orphan']}")
                    # Reset orphan value.
                    self.kwargs['orphan'] = None
                    # Break loop.
                    break

    def prepare(self):

        """
            Prepare skill for execution.
            Retrieve module, domain class, method, class instance, args, etc...
            ---
            Returns
                Boolean : Skill is prepared.
        """

        # Get domain class.
        self.__get_domain_class()
        # Get domain class instance.
        self.__get_domain_class_instance()
        # Get domain method.
        self.__get_method()
        # Get domain method parameters.
        self.__get_method_params()

        # Set skill prepared flag.
        self.prepared = True

        # Return prepared status.
        return self.prepared

    def execute(self, intent):

        """
            Execute skill with intent infos.
            ---
            Parameters
                intent : Intent
                    Interaction intent Object.
            ---
            Returns
                String : Skill execution response.
        """

        # Check if skill is prepared.
        if not self.prepared :
            # [LOG]
            logging.error("Skill is not prepared.")
            # Raise error.
            raise Exception('Skill is not prepared.')

        # Retrieve intent entities to create arguments.
        self.__set_args_from_intent(intent, use_orphan=True)

        # Execute domain method.
        response = self.method(**self.kwargs)

        # Return execution response.
        return response
        
    
 

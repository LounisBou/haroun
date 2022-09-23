#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
from functools import wraps
from time import perf_counter
from termcolor import colored
#
# 
#
class debug:
    
    """ Debug class decorator """
    
    def __init__(self, level="info", show_args = False):
        
        """ 
            Debug decorator constructor.
            
            Parameters
                ----------
                level : String
                    Debug level string (optionnal, defaut = "info") [Possible values : info, verbose]
                show_args : Boolean  
                    If true show argument for each called function.
                
            Returns
            _______
            decorator : decorator
        """
        
        # Debug level.
        self.level = level
        self.show_args = show_args
        
    
    def __call__(self, function):
        
        """
            Debug decorator call method.
            
            Returns
            _______
            warper : warper method.
        """
        
        
        # Retrieve the function docstring thanks to the functools wraps decorator.
        @wraps(function)
        def warper(*args, **kwargs):
            
            """ 
                Debug decorator warper 
            
                Returns
                _______
                void
            """
            
            # [DEBUG]
            print(colored("---------------------- {} ----------------------".format(function.__name__), "blue"))
            
            """ Retrieve function arguments if show_args is True. """
            if self.show_args : 
                
                # [DEBUG] 
                print(colored("Args : ", "green"))
                
                # Loop over kwargs arguments dict.
                for item in args:
                    # [DEBUG] 
                    if type(item) in (int, str, list) : 
                        print(colored(" - {}".format(item), "green"))
                    else:
                        print(colored(" - {}".format(type(item)), "green"))
                
                # Loop over kwargs arguments dict.
                for key, value in kwargs.items():
                    # [DEBUG] 
                    if type(value) in (int, str, list) :
                        print(colored(" - {} : {}".format(key, value), "green"))
                    else:
                        print(colored(" - {} : {}".format(key, type(value)), "green"))
            
                
            """ Decorator override before. """
            
            
            """ Call the function. """
            # Start execution timer
            if self.level == "verbose" : 
                timer_start = perf_counter()
            
            # Execute function. 
            result = function(*args, **kwargs)      
            
            # Stop execution timer
            if self.level == "verbose" : 
                timer_stop = perf_counter()
                # Timing definition.
                timer = timer_stop - timer_start
                # Print timer diff.
                print(colored("Execution time : {} ms".format(timer * 1000), "red"))
            
            """ Decorator override after. """
            result = result
            
            """ Return function call result. """
            return result
                    
        # Return warper method.
        return warper
    

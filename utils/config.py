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
# Import configparser library.
from configparser import ConfigParser
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
class Config():
    
    """ Config utils class. """

    @staticmethod
    def load_haroun_config(config_name, mandatory = True, parser = None):
        
        """ 
            Load haroun config.
            ---
            Parameters
                config_name : String
                    Config name to load.
                mandatory : Boolean (optional)
                    If True, raise error if config file not found. (default is True)
                parser : ConfigParser (optional)
                    ConfigParser object to use, if None new ConfigParser object will be returned. (default is None)
            ---
            Return : ConfigParser
                ConfigParser object.
        """
        
        # Load domain config and return configParser object.
        return Config.__load_config_file(f"{ROOT_PATH}config/{config_name.lower()}.ini", mandatory, parser)


    @staticmethod
    def load_domain_config(domain_name, mandatory = True, parser = None):
        
        """ 
            Load domain config.
            ---
            Parameters
                domain_name : String
                    Domain config to load.
                mandatory : Boolean (optional)
                    If True, raise error if config file not found. (default is True)
                parser : ConfigParser (optional)
                    ConfigParser object to use, if None new ConfigParser object will be returned. (default is None)
            ---
            Return : ConfigParser
                ConfigParser object.
        """
        
        # Load domain config and return configParser object.
        return Config.__load_config_file(f"{ROOT_PATH}domains/{domain_name.lower()}/config.ini", mandatory, parser)


    @staticmethod
    def __load_config_file(config_file_path, mandatory = True, parser = None):
        
        """ 
            Load config from file.
            ---
            Parameters
                config_file_path : String 
                    Path to config file.
                mandatory : Boolean (optional)
                    If True, raise error if config file not found. (default is True)
                parser : ConfigParser (optional)
                    ConfigParser object to use, if None new ConfigParser object will be returned. (default is None)
            ---
            Return : ConfigParser
                ConfigParser object.
        """

        # Create config parser.
        if parser is None:
            parser = ConfigParser()
        
        # Check if config exist.
        if path.exists(config_file_path):
            # Parse domain config file.
            parser.read(f"{config_file_path}")
        # If config file not found and mandatory.
        elif mandatory:
            # Raise error.
            raise FileNotFoundError(f"Config file not found : {config_file_path}")
        else:
            # [LOG]
            logging.warning(f"Config file {config_file_path} doesn't exist. Continue without it.")

        # Return config parser.
        return parser
    
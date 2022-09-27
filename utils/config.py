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
class Config(ConfigParser):

    """ Config extend ConfigParser. """

    def __init__(self, config_name = None):

        """ Class constructor. """
            
        # Init parent class ConfigParser.
        super().__init__()

        # If config_name provided, load config file.
        if config_name:
            self.load_config_file(config_name)


    def load_config_file(self, config_name):
        
        """ 
            Get config from config/{config_name}.ini file.
            ---
            Parameters
                config_name : String 
                    Config name use to find config file name to load.
        """
        
        # Domain config file path.
        domain_config_file_path = f"{ROOT_PATH}config/{config_name.lower()}.ini"
        
        # Check if config exist.
        if path.exists(domain_config_file_path):
        
            # Parse domain config file.
            self.read(f"{domain_config_file_path}")
                
        else:
            # [LOG]
            logging.warning(f"Config file {domain_config_file_path} doesn't exist. Continue without it.")
    
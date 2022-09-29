#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import regular expression library.
import re
# Import os.path
from os import path
# Import system library.
from sys import path as syspath
# Import configparser library.
from configparser import ConfigParser
# Import logging library
import logging
# Import random.
from random import choice
#
# Gloabls : 
#
# Current, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
ROOT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
#
class Dialog(ConfigParser):

    """
        Modified ConfigParser that allow ':' in keys and only '=' as separator.
    """

    OPTCRE = re.compile(
        r'(?P<option>[^=\s][^=]*)'          # allow only = 
        r'\s*(?P<vi>[=])\s*'                # for option separator           
        r'(?P<value>.*)$'                   
    )

    def __init__(self, lang, dialogs_name = None):

        """ Class constructor. """
            
        # Init parent class ConfigParser allowing no value.
        super().__init__(allow_no_value=True)

        # Create dialogs sections dict.
        self.dialogs_sections = {}

        # Define dialogs language.
        self.lang = lang

        # Load dialogs if dialogs_name provided.
        if dialogs_name:
            self.load_dialogs_file(dialogs_name)


    def load_dialogs_file(self, dialogs_name = None):
        
        """
            Retrieve dialog from domain dialogs file, add dialogs to dialogs dict.
            ---
            Parameters
                domain_class_name : String
                    Domain dialogs file name, if you want to override it. [Default : None]
        """

        # Define dialogs file name.
        dialogs_file_name = dialogs_name.lower()+".dialogs"
        
        # Dialogs directory path.
        dialogs_file_path=f"{ROOT_PATH}dialogs/{self.lang}/{dialogs_file_name}"
        
        # Check if dialogs exist.
        if path.exists(dialogs_file_path):

            # Parse domain dialogs file.
            self.read(f"{dialogs_file_path}")

            # Get all sections.
            for section_name in self.sections():
                dialog_section = self[section_name]
                self.dialogs_sections[section_name] = []
                # Get all dialogs.
                for dialog in dialog_section.items():
                    # If dialog contains ':' it may be cut in tupple.
                    if not dialog[1] :
                        self.dialogs_sections[section_name].append(dialog[0])
                    else:
                        # Add dialog to self.dialogs[section_name] list.
                        self.dialogs_sections[section_name].append(' : '.join(dialog))

            # [LOG]
            logging.debug(f"Dialogs : {self.dialogs_sections[section_name]}")
                
        else:
            # [LOG]
            logging.error(f"Error config file {dialogs_file_path} doesn't exist.")
             

    def get_dialog(self, dialog_key, random = True, dialog_position = 1):
        
        """
            Retrieve dialog self.dialogs.
            ---
            Parameters
                dialog_key : String
                    Dialog section key name.
                random : Boolean
                    If True, return a random dialog from section. [Default : True]
                dialog_position : Integer
                    If random is False, return dialog at dialog_position. [Default : 1]
            ---
            Return : String
                Dialog sentence.
        """
                
        # Random dialogs
        if random :
            dialog = choice(self.dialogs_sections[dialog_key])
        else:
            dialog = self.dialogs_sections[dialog_key][dialog_position - 1]

        # Replace "" by space, manage empty dialog.
        dialog = dialog.replace('""', ' ')

        # Capitalize first letter.
        dialog = dialog[0].upper() + dialog[1:]

        # Return dialog.
        return dialog

    def say(self, dialog_key, **kwargs):

        """
            Return dialog formated with kwargs.
            ---
            Parameters
                dialog_key : String
                    Dialog section key name.
                kwargs : Dict
                    Dialogs parameters.
            ---
            Return : String
                Dialog sentence.
        """

        # Get dialog.
        dialog = self.get_dialog(dialog_key)

        # Return dialog with replaced parameters.
        return dialog.format(**kwargs)
        
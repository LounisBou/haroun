#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import regular expression library.
import re
# Import os.path, os.walk
from os import path, walk
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
# Current, parent, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
PARENT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
ROOT_PATH = path.dirname(path.abspath(PARENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
#
class Dialog(object):

    """ Concept of Haroun Dialog. """

    # Dialogs sections dict.
    sections = {}

    """ Loading methods. """

    @classmethod
    def load_haroun_dialog_files(cls, lang):

        """ 
            Load domain dialog files.
            ---
            Parameters
                domain_name : String
                    Domain name to load.
                lang : String
                    Language to use for dialog.
        """

        # Load domain dialogs.
        cls.load_dialog_files(f"{ROOT_PATH}lang/{lang}/dialogs/")

    @classmethod
    def load_domain_dialog_files(cls, domain_name, lang):

        """ 
            Load domain dialog files.
            ---
            Parameters
                domain_name : String
                    Domain name to load.
                lang : String
                    Language to use for dialog.
        """

        # Load domain dialogs.
        cls.load_dialog_files(f"{ROOT_PATH}domains/{domain_name.lower()}/lang/{lang}/dialogs/")

    @classmethod
    def load_dialog_files(cls, dialog_dir_path):

        """ 
            Load dialog files.
            ---
            Parameters
                dialog_dir_path : String
                    Dialog directory path.
        """

        # Get dialog files path list.
        dialog_files_path = Dialog.__get_dialog_files(dialog_dir_path)

        # For each dialog file.
        for dialog_file_path in dialog_files_path:
            # Load dialog file.
            cls.load_dialog_file(dialog_file_path)
    

    @classmethod
    def load_dialog_file(cls, dialog_file_path):
        
        """
            Retrieve dialog from domain dialogs file, add dialogs to dialogs dict.
            ---
            Parameters
                dialog_file_path : String
                    Dialog file path.
        """
        
        # Check if dialogs exist.
        if path.exists(dialog_file_path):

            # Create parser.
            parser = ConfigParser(allow_no_value=True)

            # Parse domain dialogs file.
            parser.read(f"{dialog_file_path}")

            # Get all sections.
            for section_name in parser.sections():
                # Add section to dialogs dict.
                cls.sections[section_name] = []
                # Get all dialogs.
                for dialog in parser[section_name].items():
                    # If dialog contains ':' it may be cut in tupple.
                    if not dialog[1] :
                        cls.sections[section_name].append(dialog[0])
                    else:
                        # Add dialog to self.dialogs[section_name] list.
                        cls.sections[section_name].append(' : '.join(dialog))

            # [LOG]
            logging.debug(f"Dialogs : {cls.sections[section_name]}")
                
        else:
            # [LOG]
            logging.error(f"Error dialog file {dialog_file_path} doesn't exist.")

    """ Get files methods. """

    @staticmethod
    def __get_dialog_files(dialog_dir_path):

        """ 
            Get dialog files path list.
            ---
            Parameters
                dialog_dir_path : String
                    Dialog directory path.
            ---
            Return : List
                Dialog files path list.
        """

        # List of dialog files.
        dialog_files_path = []

        # For each dialog file in dialog directory.
        for dir_path, dir_names, file_names in walk(dialog_dir_path):
            # Create file paths and remove hidden files.
            file_paths = [path.join(dir_path, file_name) for file_name in file_names if not file_name.startswith('.') and file_name.endswith('.ini')]
            # Add file paths to dialog files list.
            dialog_files_path.extend(file_paths)

        # Return dialog files path list.
        return dialog_files_path



    """ Getters """

    @classmethod
    def get(cls, dialog_key, dialog_position = None):
        
        """
            Retrieve dialog self.dialogs, return random dialog if multiple dialogs.
            You can choose dialog position by passing dialog_position parameter.
            ---
            Parameters
                dialog_key : String
                    Dialog section key name.
                dialog_position : Integer
                    Choose dialog at dialog_position. [Default : None]
            ---
            Return : String
                Dialog sentence.
        """
                
        # Random dialogs
        if dialog_position is not None and dialog_position <= len(cls.sections[dialog_key]) and dialog_position >= 1:
            dialog = cls.sections[dialog_key][dialog_position - 1] 
        else:
            dialog = choice(cls.sections[dialog_key])

        # Replace "" by space, manage empty dialog.
        dialog = dialog.replace('""', ' ')

        # Capitalize first letter.
        dialog = dialog[0].upper() + dialog[1:]

        # Return dialog.
        return dialog

    @classmethod
    def say(cls, dialog_key, **kwargs):

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
        dialog = cls.get(dialog_key)

        # Return dialog with replaced parameters.
        return dialog.format(**kwargs)
        
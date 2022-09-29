#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import os.path, os.walk, os.remove
from os import path, walk, remove
# Import system library.
from sys import path as syspath
# Import subprocess
import subprocess
# Import rhasspynlu
import rhasspynlu
# Import logging library
import logging
#
# Gloabls : 
#
# Current, parent, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
PARENT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
ROOT_PATH = path.dirname(path.abspath(PARENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
class Slot(object):

    """ Concept of Haroun Slot. """

    # NLU slots replacement dict.
    replacements = {}

    # Loaded slots.
    data = {}

    """ Loadings methods. """

    @classmethod
    def load_haroun_slots(cls, lang):

        """ 
            Load haroun slots.
            ---
            Parameters
                lang : String
                    Language to use for slots.
        """

        # Load haroun slots.
        cls.load_slot_files(f"{ROOT_PATH}slots/{lang}/")

    @classmethod
    def load_domain_slots(cls, domain_name, lang):

        """ 
            Load domain slots.
            ---
            Parameters
                domain_name : String
                    Domain name to load.
                lang : String
                    Language to use for slot.
        """

        # Load domain slots.
        cls.load_slot_files(f"{ROOT_PATH}domains/{domain_name.lower()}/{lang}/slots/")

    @classmethod
    def load_slot_files(cls, slots_dir_path):

        """ 
            Load slot files.
            ---
            Parameters
                slots_dir_path : String
                    Slots directory path.
        """

        # Get slots files path list.
        slots_files_path = Slot.get_slots_files(slots_dir_path)

        # For each slot file.
        for slot_file_path in slots_files_path:
            # Load slot file.
            cls.load_slot_file(slot_file_path)


    @classmethod
    def load_slot_file(cls, slot_file_path):
        
        """ 
            Acquire a slot file and append slot data in dict. 
            ---
            Parameters 
                slot_file_path : String 
                    Slot file path.
        """
        
        """ Create slot entries dict from slot file. """
        
        # Check if slot file exist.
        if path.exists(slot_file_path):
            
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
                        cls.data[slot_entry_key] = slot_entry_value
                        
                    except:
                        # [LOG]
                        logging.error(f"Slot line can't be interpreted. File slot {slot_file_path} error on : {line}")
        else:
            # [LOG]
            logging.error(f"Slot file {slot_file_path} not found.")

    """ Getters """
    
    @classmethod
    def get(cls, key):
        
        """ 
            Get slot value from key.
            ---
            Parameters
                key : String
                    Key to get value from.
            ---
            Return : String
                Slot value, or None if not found.
        """
        
        # Return slot value.
        if key in cls.data:
            return cls.data[key]
        else :
            return None

    @classmethod
    def get_reverse(cls, value):
        
        """ 
            Get slot key from value.
            ---
            Parameters
                value : String
                    Value to get key from.
            ---
            Return : String
                Slot key, or None if not found.
        """
        
        # For each slot data.
        for key, slot_value in cls.data.items():
            
            # If slot value match.
            if slot_value == value:
                
                # Return key.
                return key

        return None


    """ Get slots files. """

    @staticmethod
    def get_domain_slots_files(domain_name, lang):

        """ 
            Load domain slots.
            ---
            Parameters
                domain_name : String
                    Domain name to load.
                lang : String
                    Language to use for slot.
            ---
            Return
                slots_files : List
                    Domain slots files path list.
        """

        # Define domain slots dir path.
        domain_slots_dir_path = f"{ROOT_PATH}domains/{domain_name.lower()}/{lang}/slots/"
        
        # Get slots files path list.
        return Slot.get_slots_files(domain_slots_dir_path)


    @staticmethod
    def get_slots_files(slots_dir_path):

        """ 
            Get slot files path.
            ---
            Parameters
                slots_dir_path : String
                    Slots directory path.
            ---
            Return
                slots_files : List
                    Slots files path list.
        """

        # List of slot files.
        slots_files_path = []

        # For each slot file in slot directory.
        for dir_path, dir_names, file_names in walk(slots_dir_path):
            # Create file paths and remove hidden files.
            file_paths = [path.join(dir_path, file_name) for file_name in file_names if not file_name.startswith('.')]
            # Append file paths to slots files list.
            slots_files_path.extend(file_paths)

        # Return slots files path list.
        return slots_files_path


    """ NLU method. """

    @classmethod
    def create_slots_replacement_dict(cls, domains, lang):
        
        """ 
            Acquire all slots files and create a Rhasspy NLU slots dict. 
            Create Rhasspy NLU slots replacements dict.
            ---
            Parameters
                domains : List
                    List of domains slots to load.
                lang : String
                    Language to use for slot.
        """

        # List of slots files path to load.
        slots_files = []
        
        # Haroun slots directory path.
        haroun_slots_dir_path=f"{ROOT_PATH}slots/{lang}/"
        
        # Get Haroun slots files.
        slots_files.extend(Slot.get_slots_files(haroun_slots_dir_path))

        # For each domain.
        for domain in domains:
            # Get domain slots files.
            slots_files.extend(Slot.get_domain_slots_files(domain, lang))
        
        """ Create slots dict from slots files. """
            
        # Iterate through slots_files list
        for slot_file_path in slots_files:

            # Get slot file name from path.
            slot_file_name = path.basename(slot_file_path)
            
            # Retrieve slot file content.
            with open(slot_file_path) as file_buffer:
                
                # Read the data from file. 
                FileContent = file_buffer.read()
                
                # Retrieve all slots entries in file and separate them with pipe.
                slots_entries = FileContent.replace("\n", " | ")
            
                # Construct slots.
                key = "$"+slot_file_name
                value = [rhasspynlu.Sentence.parse(slots_entries)]
                
                # Add it to replacement slots dict.
                cls.replacements[key] = value
        


    """ SlotProgram utils methods for slot program execution and slot file creation. """

    @staticmethod
    def get_domain_slot_program_files(domain, lang):

        """ 
            Load domain slot programs.
            ---
            Parameters
                domain : String
                    Domain name to load.
                lang : String
                    Language to use for slot.
            ---
            Return
                slot_program_files : List
                    Domain slot programs files path list.
        """

        # Define domain slot programs dir path.
        domain_slot_program_dir_path = f"{ROOT_PATH}domains/{domain.lower()}/{lang}/slots_programs/"

        # Return slot programs files path list.
        return Slot.get_slot_program_files(domain_slot_program_dir_path)

    @staticmethod
    def get_slot_program_files(slot_program_dir_path):

        """ 
            Get slot programs files path.
            ---
            Parameters
                slot_program_dir_path : String
                    Slot programs directory path.
            ---
            Return
                slot_program_files : List
                    Slot programs files path list.
        """

        # List of slot programs files path.
        slot_program_files = []

        # Get files from dir path.
        for dir_path, dir_names, file_names in walk(slot_program_dir_path):
            # Create file paths and remove hidden files.
            file_paths = [path.join(dir_path, file_name) for file_name in file_names if not file_name.startswith('.')]
            # Append file paths to slot programs files list.
            slot_program_files.extend(file_paths)

        # Return slot programs files path list.
        return slot_program_files

    
    @staticmethod
    def execute_all_slot_program(domains, lang, force_regenerate_slot = False):
          
        """ 
            Execute all slot_program in slot program directory. 
            Slots programs are independents scripts that generate slots.
            ---
            Parameters
                domains : List
                    List of domains slots to load.
                lang : String
                    Language to use for slots and slots programs.
                force_regenerate_slot : Boolean (optional)
                    Force slot regeneration. [Default: False]
        """
        
        # Haroun slot program directory path.
        haroun_slot_program_path=f"{ROOT_PATH}slotsPrograms/{lang}/"

        # Haroun slot directory path.
        haroun_slot_path=f"{ROOT_PATH}slots/{lang}/"

        # Get Haroun slot programs files.
        haroun_slot_program_files = Slot.get_slot_program_files(haroun_slot_program_path)

        # For each slot program file.
        for haroun_slot_program_file in haroun_slot_program_files:
            # Execute Haroun slot program.
            Slot.execute_slot_program(haroun_slot_program_file, haroun_slot_path, force_regenerate_slot)

        # For each domain.
        for domain in domains:
            
            # Get domain slot program files.
            Slot.execute_domain_slot_program(domain, lang, force_regenerate_slot)


    @staticmethod
    def execute_domain_slot_program(domain_name, lang, force_regenerate_slot = False):

        """ 
            Execute domain slots programs.
            ---
            Parameters
                domains : List
                    List of domains slots programs to execute.
                lang : String
                    Language to use for slot.
        """

        # Get domain slot programs files.
        slot_program_files = Slot.get_domain_slot_program_files(domain_name, lang)

        # Slot files directory path.
        slot_files_dir_path = f"{ROOT_PATH}domains/{domain_name.lower()}/{lang}/slots/"

        # For each domain.
        for slot_program_file_path in slot_program_files:
            # Execute domain slots programs.
            Slot.execute_slot_program(slot_program_file_path, slot_files_dir_path, force_regenerate_slot)

    @staticmethod
    def execute_slot_program(slot_program_file_path, slot_files_dir_path, force_regenerate_slot = False):

        """ 
            Execute slot program.
            ---
            Parameters
                slot_program_file_path : String
                    Slot program file to execute.
                slot_files_dir_path : String
                    Slot files directory path.
                force_regenerate_slot : Boolean (optional)
                    Force slot regeneration. [Default: False]
        """

        print(f"Execute slot program: {slot_program_file_path}")

        # Get slot program file name.
        slot_program_file_name = path.basename(slot_program_file_path)

        # Get slot program directory path.
        slot_program_dir_path = path.dirname(slot_program_file_path)

        # Get slot program file name without extension.
        slot_program_file_name_without_extension = path.splitext(slot_program_file_name)[0]

        # Define slot name as slot program file name without extension.
        slot_name = slot_program_file_name_without_extension.lower()

        # Create slot file with program slot name.
        slot_file_path = f"{slot_files_dir_path}{slot_name}"

        # If slot file already exist and config slot_force_regenerate is true.
        if path.exists(slot_file_path) and force_regenerate_slot :
            # [LOG]
            logging.info(f"Slot file {slot_file_path} already exist and config slot_force_regenerate is true, so we delete it.")
            # Remove slot file.
            remove(slot_file_path)
        elif path.exists(slot_file_path) :
            # [LOG]
            logging.warning(f"Slot {slot_name} already exist.")
            logging.warning(f"Slot program  file '{slot_program_file_path}' won't be executed. Delete slot {slot_name} to re-generate it.\n")
            # End function.
            return
        
        # Execute program slot file.
        process = subprocess.Popen(
            [slot_program_file_path],
            shell=True,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True
        )
        
        # Get program slot file execution outputs.
        output, error = process.communicate()

        # If program slot file execution failed.
        if process.returncode != 0:
            # [LOG]
            logging.error(f"Slot program {slot_program_file_path} execution failed.")
            logging.error(f"Error : {error.decode('utf-8')} \n")
            logging.error(f"----------------------------------------\n")
            # End function.
            return
        
        # Retrieve output string.
        slot_file_content = output.decode()
                        
        # Open file : create if not exist, truncate if exist.
        with open(slot_file_path, 'w') as slot_file:
            # Write program slot file execution output.
            slot_file.write(f"{slot_file_content}")

        # [LOG]
        logging.info(f"Slot file {slot_file_path} created.")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Libraries dependancies :
#
# Import os.path, os.walk, os.remove
from os import path, walk, remove
# Import subprocess
import subprocess
# Import system library.
from sys import path as syspath
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
class SlotProgram():

    """ SlotProgram utils for slot program execution and slot file creation. """

    @staticmethod
    def execute(lang, slot_program_file_name, force_regenerate_slot = False):

        """ 
            Execute slot program.
            ---
            Parameters
                lang : String
                    Language to use for slot and slot progrma.
                slot_program_file_name : String
                    Slot program name to execute.
                force_regenerate_slot : Boolean (optional)
                    Force slot regeneration. [Default: False]
        """

        # Get file name without extension as program_slot_name.
        slot_program_name = path.splitext(slot_program_file_name)[0]

        # Get file name extension as slot_program_ext.
        slot_program_ext = path.splitext(slot_program_file_name)[1]

        # Slots directory path.
        slots_path=f"{ROOT_PATH}slots/{lang}/"
        
        # Slots programs directory path.
        slots_program_path=f"{ROOT_PATH}slotsPrograms/{lang}/"
    
        # Get program path.
        slot_program_path = f"{slots_program_path}{slot_program_name}.{slot_program_ext}"
        
        # Create slot file with program slot name.
        slot_file_path = f"{slots_path}{slot_program_name}"

        # If slot file already exist and config slot_force_regenerate is true.
        if path.exists(slot_file_path) and force_regenerate_slot :
            # [LOG]
            logging.info(f"Slot file {slot_file_path} already exist and config slot_force_regenerate is true, so we delete it.")
            # Remove slot file.
            remove(slot_file_path)
        else:
            # [LOG]
            logging.warning(f"Slot {slot_program_name} already exist.")
            logging.warning(f"Slot program  file '{slot_program_path}' won't be executed. Delete slot {slot_program_name} to re-generate it.\n")
            # End function.
            return
        
        # Execute program slot file.
        process = subprocess.Popen(
            [slot_program_path],
            shell=True,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True
        )
        
        # Get program slot file execution outputs.
        output, error = process.communicate()

        # If program slot file execution failed.
        if error:
            # [LOG]
            logging.error(f"Slot program {slot_program_name} execution failed.")
            logging.error(f"Error : {error.decode('utf-8')}")
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


    @staticmethod
    def execute_all(lang, force_regenerate_slot = False):
        
        """ 
            Execute all slots programs in slotsPrograms directory. 
            Slots programs are independents scripts that generate slots.
            ---
            Parameters
                lang : String
                    Language to use for slots and slots programs.
                force_regenerate_slot : Boolean (optional)
                    Force slot regeneration. [Default: False]
        """
        
        # Slots programs directory path.
        slots_program_path=f"{ROOT_PATH}slotsPrograms/{lang}/"
        
        # Browse through slots files to get files names. 
        slots_programs_files_names = []    
        for(dir_path, dir_names, file_names) in walk(slots_program_path):
            # [LOG]
            logging.info(f"Looking in slotsPrograms directory : {slots_program_path}, listing files :\n{file_names}")
            # Add file_names to slots_programs_files list.
            slots_programs_files_names.extend(file_names)
            break
            
        # Iterate through slots_programs_files list
        for slot_program_file_name in slots_programs_files_names:
            
            # Execute slot program.
            SlotProgram.execute(lang, slot_program_file_name)

            
    
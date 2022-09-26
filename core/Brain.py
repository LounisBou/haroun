#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : 
#
#
# Haroun dependancies : 
#
# Import sys.path as syspath
from sys import path as syspath
# Import os.path, os.walk, os.remove
from os import path, walk, remove
# Import subprocess
import subprocess
# Import rhasspynlu
import rhasspynlu
# Import logging library
import logging
# Import pathlib.Path for rhasspynlu.parse_ini
from pathlib import Path
from core.Mouth import Mouth
# Import consciousness class.
from core.consciousness.Conscious import Conscious
from core.consciousness.Ego import Ego
# Import Base utils.base (Peewee ORM connector)
from utils.bdd import MyModel
# Import audio transcription class (STT)
from core.Ear import Ear
# Import audio generation class (TTS)
from core.Mouth import Mouth
# Import concepts class.
from core.concepts.Domain import Domain
from core.concepts.Skill import Skill
from core.concepts.Stimulus import Stimulus
from core.concepts.Interaction import Interaction
from core.concepts.Intent import Intent
from core.concepts.Response import Response
from core.concepts.Memory import Memory
from core.concepts.Context import Context
# Import domains.
from domains import *
# Import utils
from utils.debug import *
# Import json library.
import json
# Import dialog utils.
from utils.dialog import Dialog
#
#
#
# Gloabls : 
#
# Current, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
ROOT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
#
#
class Brain(object):  
    
    """ Concepts and consciousness class management for Haroun. """
        
    def __init__(self, config):
        
        """ 
            __init__ : Brain class constructor.
        """
        
        # Audio transcription class (STT).
        self.ear = Ear()

        # Audio generation class (TTS).
        self.mouth = Mouth()

        # Consciousness (Reflexivity).
        self.conscious = Conscious()
        self.ego = Ego()
        
        # Config vars.
        self.config = config
        
        # Set logging level.
        logging.getLogger().setLevel(self.config['haroun']['log_level'])
        
        # Available domains list. 
        self.domains = {}
        
        # Available intents list. 
        self.intents = None
        
        # Available slots for replacements in intents.
        self.slots = None
        
        # Training rhasspy-nlu graph from known intents. 
        self.intents_graph = None
    
        # Memories 
        self.memories = None
        
        # Wake up : initialisation of Brain class.
        self.wakeUp()

        # Load error dialogs.
        self.dialogs = Dialog(self.config['haroun']['lang'], "error")
        
    
    # ! - Initialisation.
    
    def wakeUp(self):
        
        """
            wakeUp : Initialise Brain Class.
        """
        
        # Available intents list. 
        self.intents =  self.get_intents()
        
        # Execute slots programs.
        self.execute_slots_programs()
        
        # Available slots for replacements in intents.
        self.slots = self.get_slots()
    
        # Memories 
        self.memories = Memory()
        
        # Create database schema if not exist.
        self.create_database()
        
        # Training brain by creating intents graph.
        self.nlu_training()
        
        # ! - Utility methods.
    
    @staticmethod
    def __get_domain_class(domain_module_name, domain_class_name): 
        
        """ 
            Return domain class from domain name. 
            ---
            Parameters 
                domain_name : String
                    Domain module and class name.
            ---
            Return Class
                Domain class from domain module.
        """
        
        # Retrieve domain module.
        domain_module = globals()[domain_module_name]
        
        # Retrieve domain class.
        domain_class = getattr(domain_module, domain_class_name)
        
        # Return domain class. 
        return domain_class

    def create_database(self):
        
        """ Create database schema if not exist. """
        
        # List of models to create.
        haroun_models = [Memory, Context]
        
        # Create tables, indexes and associated metadata for the given list of models.
        MyModel.db.create_tables(haroun_models)
        
    
    def get_intents(self):
        
        """ 
            Acquire intents file list and create a all.ini intents file. 
            Parse haroun/intents folder to list of intents file.
            Normally one file per available domains.
            Generate one intents file and parse it with rhasspy-nlu.
            ---
            Return : intents 
                Rhasspy NLU intents list.
        """
        
        # Intents directory path.
        intents_path=f"{ROOT_PATH}intents/{self.config['haroun']['lang']}/"
        
        # Browse through intents files 
        intents_files = []    
        for(dir_path, dir_names, file_names) in walk(intents_path):
            # [LOG]
            logging.debug(f"Looking in intent directory : {intents_path}, listing files : \n{file_names}")
            intents_files.extend(file_names)
            break
            
        """ Write all intents in intents/.all.ini file. """
        
        # Open intents/.all.ini, a file that will contains all intents.
        all_intents_file_path  = intents_path+".all.ini"
                    
        # Open intents/.all.ini in write mode
        with open(all_intents_file_path, 'w+') as all_intents_file_buffer:
            
            # Iterate through intents_files list
            for file_name in intents_files:
                
                # Ignore .all.ini file.
                if file_name != ".all.ini":

                    # Construct file path.
                    file_path = intents_path+file_name
                    
                    # Open each file in read mode
                    with open(file_path) as file_buffer:
        
                        # Read the data from file. 
                        file_intents = file_buffer.read()
                        
                        # Write it in all_intents_file_buffer and add '\n\n' to enter data from next line
                        all_intents_file_buffer.write("# "+file_name+" file content : \n")
                        # Lowercase all intents.
                        all_intents_file_buffer.write(file_intents.lower()+"\n\n")
                    
                            
        # Load file for rhasspy-nlu.
        intents = rhasspynlu.parse_ini(Path(all_intents_file_path))
        
        # Return
        return intents
    
    
    def execute_slots_programs(self):
        
        """ 
            Execute slots programs. Slots programs are independents scripts that generate slots.
        """
        
        # Slots directory path.
        slots_path=f"{ROOT_PATH}slots/{self.config['haroun']['lang']}/"
        
        # Slots programs directory path.
        slots_program_path=f"{ROOT_PATH}slotsPrograms/{self.config['haroun']['lang']}/"
        
        # Browse through slots files 
        slots_programs_files = []    
        for(dir_path, dir_names, file_names) in walk(slots_program_path):
            # [LOG]
            logging.info(f"Looking in slotsPrograms directory : {slots_program_path}, listing files :\n{file_names}")
            # Add file_names to slots_programs_files list.
            slots_programs_files.extend(file_names)
            break
            
        # Iterate through slots_programs_files list
        for program_slot_file_name in slots_programs_files:
            
            # Get file name without extension as program_slot_name.
            program_slot_name = path.splitext(program_slot_file_name)[0]
        
            # Get program path.
            program_path = slots_program_path+program_slot_file_name
            
            # Create slot file with program slot name.
            slot_file_path = slots_path+program_slot_name

            # If slot file already exist and config slot_force_regenerate is true.
            if path.exists(slot_file_path) and self.config['haroun']['slot_force_regenerate'] == 'True' :
                # [LOG]
                logging.info(f"Slot file {slot_file_path} already exist and config slot_force_regenerate is true, so we delete it.")
                # Remove slot file.
                remove(slot_file_path)
            else:
                # [LOG]
                logging.warning(f"Slot {program_slot_name} already exist.")
                logging.warning(f"Program slot file '{program_slot_file_name}' won't be executed. Delete slot {program_slot_name} to re-generate it.\n")
                # Skip to next program slot file.
                continue
            
            # Execute program slot file.
            process = subprocess.Popen(
                [program_path],
                shell=True,
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True
            )
            
            # Get program slot file execution outputs.
            output, error = process.communicate()
            
            # Retrieve output string.
            slot_file_content = output.decode()
                            
            # Open file : create if not exist, truncate if exist.
            with open(slot_file_path, 'w') as slot_file:
                # Write program slot file execution output.
                slot_file.write(f"{slot_file_content}")

            # [LOG]
            logging.info(f"Slot file {slot_file_path} created.")
                    
            
    def get_slots(self):
        
        """ 
            Acquire all slots files and create a Rhasspy NLU slots dict. 
            ---
            Return : Rhasspy NLU slots
                Rhasspy NLU slots dict.
        """
        
        # Slots directory path.
        slots_path=f"{ROOT_PATH}slots/{self.config['haroun']['lang']}/"
        
        # Browse through slots files 
        slots_files = []    
        for(dir_path, dir_names, file_names) in walk(slots_path):
            # [LOG]
            logging.debug(f"Looking in slots directory : '{slots_path}', listing files :\n{file_names}")
            # Add file_names to slots_files list.
            slots_files.extend(file_names)
            break
        
        """ Get slots from domains files and add them to slots files. """
        
        # [TO DO]
        #self.domains
        
        """ Create slots dict from slots files. """
        
        # Replacement slots dict.
        slots = {}
            
        # Iterate through slots_files list
        for file_name in slots_files:
            
            # Construct file path.
            file_path = slots_path+file_name
            
            # Retrieve slot file content.
            with open(file_path) as file_buffer:
                
                # Read the data from file. 
                FileContent = file_buffer.read()
                
                # Retrieve all slots entries in file and separate them with pipe.
                slots_entries = FileContent.replace("\n", " | ")
            
                # Construct slots.
                key = "$"+file_name
                value = [rhasspynlu.Sentence.parse(slots_entries)]
                
                # Add it to replacement slots dict.
                slots[key] = value
        
        # Return
        return slots
            
    
    # ! - A.I. Training.
    
    @debug("verbose", True)
    #@lru_cache(maxsize=128, typed=True)
    def nlu_training(self):
        
        """ 
            nlu_training : Acquire domains knowledge. 
            Transform intents into graph training, replace slots if necessary.
        """
        
        # Generate intents training graph from list of known intents.
        self.intents_graph = rhasspynlu.intents_to_graph(self.intents, replacements = self.slots)
    
    # ! - Stimulus management.
        
    def generate_stimulus(self, source, source_id, sentence, user_id, interaction_id, parent_interaction_id, origin_datetime):
    
        """ 
            Generate Stimulus concept object. 
            Transform script call infos, to create a Haroun Stimulus containing infos to generate an Interaction.
            ---
            Parameters
                source : String
                    Label for stimulus source origin.
                source_id : String
                    Uniq identifier for stimulus source origin.
                sentence : String (optionnal)
                    Sentence of the stimulus. [Default = '']
                user_id : Int (optionnal)
                    Uniq identifier for user who initiate interaction. [Default = null]
                interaction_id : Int (optionnal)
                    Uniq identifier for interaction. [Default = null]
                parent_interaction_id : Int (optionnal)
                    Uniq identifier for parent interaction if Stimulus is due cause of previous interaction. [Default = null]
                origin_datetime : Datetime (optionnal)
                    Datetime origin for stimulus. [Default = null]
            ---
            Return : Stimulus
                Stimulus concept object created with scripts call infos.
        """

        # [DEBUG] 

        # Set user id as izno.
        memory = Memory.add(f"user_id_{user_id}", "Laura", "Telegram")
        #memory.remove()
        
        # Set context to make a test.
        context = Context.add(f"user_id_{user_id}", "Laura", "Telegram")
        #context.remove()
        

        # Create stimulus from script call infos.
        stimulus = Stimulus(source, source_id, sentence, user_id, interaction_id, parent_interaction_id, origin_datetime)
        
        # Check if stimulus is valid.
        if(stimulus.is_valid()):
            # End.
            return stimulus
        else:
            # Error.
            return False
        
        
    # ! - Interaction creation.
    
    def create_interaction(self, stimulus):
    
        """ 
            Generate Interaction concept object. 
            Transform script call infos, to create a Haroun Stimulus containing infos to generate an Interaction.
            ---
            Parameters
                stimulus : Stimulus
                    Stimulus source origin of the interaction.
            ---
            Return : Interaction
                Modified interaction with domain and skill infos, None if error.
        """
        
        # Create interaction from stimulus.
        interaction = Interaction(stimulus)
        
        # Return interaction ready to interact.
        return interaction
        
    # ! - Interaction management.
    
    def manage_interaction(self, interaction):
        
        """ 
            manage_interaction : Manage interaction. 
            Interaction analysis, check NLU of the interaction sentence to defined instance.
            Correct slots if neccessary.
            ---
            Parameters
                interaction : Interaction
                    Interaction concept object generate from trigger Stimulus.
            ---
            Return : Interaction
                Modified interaction with domain and skills infos, None if error.
        """
        
        # Interaction interpretation. 
        modified_interaction = self.interpreter(interaction)
        # if interpretation failed.
        if not modified_interaction :
            # Return interaction message error.
            interaction.add_response(self.dialogs.get_dialog("intent_not_found"))
            # [LOG]
            logging.error(f"Interaction interpretation failed. [Error #4].")
            logging.info(f"Message : {interaction.stimulus.sentence}")
            logging.info(f"Intent : {str(interaction.intent)}")
        else:
            # [LOG]
            logging.info(f"{str(interaction.intent)}")
            # Defined Domain & Skills for this interaction.
            modified_interaction = self.analysis(modified_interaction)
            # If Interaction analysis failed. 
            if not modified_interaction :
                # Return interaction message error.
                interaction.add_response(self.dialogs.get_dialog("intent_not_handled"))
                # [LOG]
                logging.error(f"Interaction analysis failed. [Error #6].")
                logging.info(f"Message : {interaction.stimulus.sentence}")
                logging.info(f"Intent : {str(interaction.intent)}")
            else:
            
                # [TODO]
                # Get Consciousness state of mind to add in the interaction.
                # Consciousness current interaction states may be used 
                # by interaction to generate alternative response during skill execution.
                modified_interaction.mind = self.get_states_of_mind()
                
                # Execute Skills via correponding Domains.
                modified_interaction = self.execute_skills(modified_interaction)
                # If Interaction execution failed. 
                if not modified_interaction :
                    # Return interaction message error.
                    interaction.add_response(self.dialogs.get_dialog("skill_execution_failed"))
                    # [LOG]
                    logging.error(f"Interaction skills execution failed. [Error #20].")
                else:   
                    # Generate interaction response.
                    modified_interaction = self.response(modified_interaction)
                    # If response creation failed. 
                    if not modified_interaction :
                        # Return interaction message error.
                        interaction.add_response(self.dialogs.get_dialog("response_creation_failed"))
                        # [LOG]
                        logging.error(f"Interaction skills execution failed. [Error #30].")
                    else:
                        # If all step successfully pass, override interaction with modified interaction.
                        interaction = modified_interaction
        
        # Return modified interaction.
        return interaction 
        
    # ! - Interaction steps.
        
    @debug("verbose", True) 
    def interpreter(self, interaction):
        
        """ 
            interpreter : Interpreter method, apply NLU analysis on Interaction sentence.
            Interpretation of Interaction sentence via rhasspy-nlu.
            Try to retrieve a recognition dict, if success then create define an the interaction intent attribut from it.
            ---
            Parameters
                interaction : Interaction
                    Interaction concept object generate from trigger Stimulus.
            ---
            Return : interaction 
                Interpretation of interaction success, recognition and intent attributs are now defined.
        """
                
        # Stimulus sentence pre-treatment.
        interaction.stimulus.sentence = interaction.stimulus.sentence.lower()
        interaction.stimulus.sentence = interaction.stimulus.sentence.replace(',',"")
        
        # [LOG]
        logging.debug(f"Interaction sentence : {interaction.stimulus.sentence}\n\n")
                
        # Perform intent recognition in Interaction sentence thanks to training graph.
        try:
            recognition = rhasspynlu.recognize(interaction.stimulus.sentence, self.intents_graph, fuzzy=True)
        except ZeroDivisionError :
            # Return
            return None

        # [LOG]
        logging.debug(f"Raw recognition : {recognition}\n\n")
            
        # If didn't find any intent for the stimulus sentence.
        if not recognition :
            # [LOG]
            logging.info("No intent found for this sentence.")
            # Check if there is a context intent.
            if context_intent := Domain.get_context_intent() :
                # [LOG]
                logging.info(f"Context intent found : {context_intent}")
                # Create recognition dict with current intent.
                interaction.recognition = {
                    "text" : interaction.stimulus.sentence,
                    "raw_text" : "", # Keep empty to retrieve orphan from text.
                    "intent": {"name": context_intent['name'], "confidence": 0.99},
                    "entities": [{"entity": arg_name, "value": arg_value} for arg_name, arg_value in context_intent['args'].items()],
                    "tokens": interaction.stimulus.sentence.split(" "),
                    "raw_tokens": interaction.stimulus.sentence.split(" "),
                }
            else:
                # [LOG]
                logging.info(f"No current intent found. End of interaction.\n\n")
                # Return
                return None

        # If intent found, parse recognition infos.
        else:
            
            # Format recognition as Object.
            interaction.recognition = recognition[0].asdict()

            # [LOG]
            logging.debug(f"Interaction recognition : {interaction.recognition}\n\n")
            logging.debug(f"Interaction recognition entities : {interaction.recognition['entities']}")

        # If recognition success.
        if interaction.recognition :  
            
            # Define intent.
            interaction.intent.checkRecognition(interaction.stimulus, interaction.recognition)

        # Return
        return interaction   

    def analysis(self, interaction):
        
        """ 
            Analyse interaction to define skills from intent. 
            
            Interaction analysis, check NLU recognition dict of the interaction to define skills to apply.
            Correct intent entities if necessary and define slots from them.
            ---
            Parameters
                interaction : Interaction
                    Interaction concept object generate from trigger Stimulus.
            ---
            Return : Interaction, None if error.
                Modified interaction with domain and skills infos.      
        """
        
        # [LOG]
        logging.debug(f"Interaction intent found : {interaction.intent.label}\n")
        logging.debug(f"Intent handlers : {Domain.intents_handlers}\n")
        
        # Check if there is a domain method that handle this intent.
        if interaction.intent.label in Domain.intents_handlers.keys():

            # Create a skill for all handlers of this intent.
            for intent_handler in Domain.intents_handlers[interaction.intent.label]:
                
                # [LOG]
                logging.debug(f"Intent handler found : {intent_handler}\n")

                # Create the interaction skill.
                interaction.skills.append(
                    Skill(
                        intent_handler['module'], 
                        intent_handler['class'], 
                        intent_handler['method']
                    )
                )
                
         # Check if there is a context intent.
        elif context_intent := Domain.get_context_intent() :

            # [LOG]
            logging.info(f"No handler for intent : {interaction.intent.label}")
            logging.info(f"Context intent found : {context_intent}")
            logging.info(f"Switching to context intent.")

            # Change interaction intent with intent context info.
            interaction.intent.label = context_intent['name']
            interaction.intent.confidence = 0.99

            # Get a copy entities from interaction.
            entities = interaction.intent.entities.copy()

            # For original entities in interaction.
            for entity in entities:
                # Generate orphan infos.
                interaction.intent.entities.extend([
                    {
                        "entity": "orphan_type", 
                        "value": entity['entity']
                    },
                    {
                        "entity": "orphan_raw", 
                        "value": entity['raw_value']
                    },
                    {
                        "entity": "orphan", 
                        "value": entity['value']
                    }
                ])

            # Retrieve context intent args, set them as entities.
            interaction.intent.entities.extend(
                [{"entity": arg_name, "value": arg_value} for arg_name, arg_value in context_intent['args'].items()]
            )

            # Relaunch analysis with modified interaction.
            return self.analysis(interaction)

        else:
            # Error message. 
            logging.info(f"No handler for intent '{interaction.intent.label}' found.")
            # Return None (error)
            return None
              
        # Return modified interaction.
        return interaction
                
    def execute_skills(self, interaction):
        
        """ 
            Execute Skills via Domains methods.  
            Instanciate the correct domain class for each skill. 
            Prepare domain method call with correct info from intent. 
            Then execute the method and retrieve execute return infos.
            ---
            Parameters
                interaction : Interaction
                    Interaction concept object generate from trigger Stimulus.
            ---
            Return : Interaction
                Modified interaction with domain and skill infos, None if error/      
        """
        
        for skill in interaction.skills:

            # Retrieve domain class.
            domain_class = Brain.__get_domain_class(skill.module_name, skill.class_name)
                            
            # Instanciate domain.
            domain_instance = domain_class()

            # Get domain methods args list to prepare skill.
            method_args = domain_instance.get_method_args(skill.method_name)
            
            # Prepare skill for execution.
            preparation_flag = skill.prepare(interaction.intent, method_args)
            
            # Excute skill on domain.
            execution_flag = domain_instance.execute_skill(skill)

        # Return modified interaction.
        return interaction

    def response(self, interaction):
        
        """ 
            response : Create interaction response.  
            Parse interaction data, to generate an response with datas and sentence.
            ---
            Parameters
                interaction : Interaction
                    Interaction for which to generate response.
            ---
            Return : Interaction
                Modified interaction with domain and skill infos, None if error.
        """
        
        # Retrieve response sentence of each skill.
        for skill in interaction.skills:

            # Retrieve skill execution return values.
            interaction.add_response(skill.return_values)
        
        # Return modified interaction
        return interaction

    # ! Consciousness (Reflexivity)

    def get_states_of_mind(self):
        
        """ 
            get_states_of_mind : method, allow reflexivity management.
            --- 
            Return : 
                Curent states of mind.
        """
        
        # Re-calculate awareness values.
        
        
        # Return
        return {}


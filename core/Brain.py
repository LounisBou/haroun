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
# Import os.path
from os import path
# Import importlib
import importlib
# Import rhasspynlu
#import rhasspynlu
# Import logging library
import logging
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
from core.concepts.Memory import Memory
from core.concepts.Context import Context
from core.concepts.Dialog import Dialog
from core.concepts.Intent import Intent
from core.concepts.Slot import Slot
# Import utils debug function.
from utils.debug import *
#
#
# Gloabls : 
#
# Current, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
ROOT_PATH = path.join(CURRENT_PATH, "..")
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

        # Define language from config.
        self.lang = config['haroun']['lang']
        
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
        self.domains = []
        
        # Wake up : initialisation of Brain class.
        self.wakeUp()
        
    
    # ! - Initialisation.
    
    def wakeUp(self):
        
        """
            wakeUp : Initialise Brain Class.
        """
        
        # Get available domains list.
        self.domains = Domain.get_available_domain_list()

        # Load intents.
        Intent.load_intents(self.domains, self.lang)

        # Check if slot file must be generated.
        slot_force_regenerate = self.config['haroun']['slot_force_regenerate'] == 'True' 

        # Execute slots programs.
        Slot.execute_all_slot_program(self.domains, self.lang, slot_force_regenerate)
        
        # Create slot dict for replacements in intents.
        Slot.create_slots_replacement_dict(self.domains, self.lang)

        # Create intents graph.
        Intent.create_graph(Slot.replacements)
        
        # Load haroun slots.
        Slot.load_haroun_slots(self.lang)

        # Load haroun dialogs.
        Dialog.load_haroun_dialog_files(self.lang)

        # Create database schema if not exist.
        self.create_database()
        
    
    # ! - Utility methods.

    def create_database(self):
        
        """ Create database schema if not exist. """
        
        # List of models to create.
        haroun_models = [Memory, Context]
        
        # Create tables, indexes and associated metadata for the given list of models.
        MyModel.db.create_tables(haroun_models)
    
    
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
            interaction.add_response(Dialog.say("intent_not_found"))
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
                interaction.add_response(Dialog.say("intent_not_handled"))
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
                    interaction.add_response(Dialog.say("skill_execution_failed"))
                    # [LOG]
                    logging.error(f"Interaction skills execution failed. [Error #20].")
                else:   
                    # If all step successfully pass, override interaction with modified interaction.
                    interaction = modified_interaction
        
        # Return modified interaction.
        return interaction 
        
    # ! - Interaction steps.
        
    @debug("verbose", True) 
    def interpreter(self, interaction):
        
        """ 
            Try intent recognition : define intent from interaction sentence.
            ---
            Parameters
                interaction : Interaction
                    Interaction concept object generate from trigger Stimulus.
            ---
            Return : interaction 
                Interpretation of interaction success, recognition and intent attributs are now defined.
        """
        
        # [LOG]
        logging.debug(f"Interaction sentence : {interaction.stimulus.sentence}\n\n")

        # Perform intent recognition from sentence.
        recognition_success = interaction.intent.recognize(interaction.stimulus.sentence)
        
        if recognition_success :
            # Return
            return interaction   
        else:
            # Return
            return None

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

                # Prepare skill, get domain, method, args, etc...
                interaction.skills[-1].prepare()
                
         # Check if there is a context intent.
        elif context_intent := Domain.get_context_intent() :

            # [LOG]
            logging.info(f"No handler for intent : {interaction.intent.label}")
            logging.info(f"Context intent found : {context_intent}")
            

            # Change interaction intent with intent context info.
            interaction.intent.label = context_intent['name']
            interaction.intent.confidence = 0.99

            # Add context intent args as interaction intent args.
            interaction.intent.kwargs.update(context_intent['args'])

            # [LOG]
            logging.info(f"Switching to context intent with arguments : {interaction.intent.kwargs}")
            logging.info(f"Stimulus sentence : {interaction.stimulus.sentence}")
            
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
            Then execute the method and retrieve skill response.
            Add res
            ---
            Parameters
                interaction : Interaction
                    Interaction concept object generate from trigger Stimulus.
            ---
            Return : Interaction
                Modified interaction with domain and skill infos, None if error/      
        """
        
        for skill in interaction.skills:

            # Execute skill.
            response = skill.execute(interaction.intent)

            # If response is not None.
            if response:
                # Add response to interaction.
                interaction.add_response(response)
            else:
                # [LOG]
                logging.error(f"No response from skill : {skill}")
                # Return None (error)
                return None

        # Return modified interaction.
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


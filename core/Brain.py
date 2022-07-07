#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : 
#
#
# Haroun dependancies : 
#
# Import sys
import sys
# Import os
import os
# Import subprocess
import subprocess
# Import python nlu spacy
#import spacy
# Import rhasspynlu
import rhasspynlu
# Import Path from pathlib
from pathlib import Path
# Import configparser.
from configparser import ConfigParser
# Import consciousness class.
from core.consciousness.Conscious import Conscious
from core.consciousness.Ego import Ego
#
# Import concepts class.
from core.concepts.Domain import Domain
from core.concepts.Skill import Skill
from core.concepts.Stimulus import Stimulus
from core.concepts.Interaction import Interaction
from core.concepts.Intent import Intent
from core.concepts.Response import Response
from core.concepts.Memory import Memory
# Import functools
from functools import *
# Import utils
from utils.debug import *
# Import json library.
import json
#
#
#
# Gloabls : 
#
# Current, and root paths.
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))+'/'
ROOT_PATH = os.path.dirname(os.path.abspath(CURRENT_PATH))+'/'
sys.path.append(ROOT_PATH)
#
#
#
class Brain:  
  
  """ Concepts and consciousness class management for Haroun. """
    
  def __init__(self):
    
    """ 
      __init__ : Brain class constructor.
    """
    
    # Consciousness (Reflexivity).
    self.conscious = Conscious()
    self.ego = Ego()
    
    # Config vars.
    self.config = {}
    
    # Available domains list. 
    self.domains = {}
    
    # Available skills list. 
    #self.skills = None
    
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

  # ! - Initialisation.
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def wakeUp(self):
    
    """
      wakeUp : Initialise Brain Class.
    """
    
    # Load config from config files.
    self.loadConfig()
    
    # Available domains list. 
    self.domains = self.getDomains()
    
    # Available skills list. 
    #self.skills = self.getSkills()
    
    # Available intents list. 
    self.intents =  self.getIntents()
    
    # Execute slots programs.
    self.executeSlotsPrograms()
    
    # Available slots for replacements in intents.
    self.slots = self.getSlots()
  
    # Memories 
    self.memories = Memory()
    
    # Training brain by creating intents graph.
    self.nlu_training()
    
    
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def loadConfig(self):
    
    """ 
      getConfig : Get config files and load config vars.
      ---
      Return : None
    """
    
    # Config path.
    configPath = ROOT_PATH+"config"
    
    # Browse through config files 
    configFiles = []
    for(dirpath, dirnames, filenames) in os.walk(configPath):
      # Add directory filenames without extension to domains list.
      configFiles.extend(filenames)
      break
    
    # [TODO]
    # See configparser 
    configParser = ConfigParser()
    
    # Iterate through slotsProgramsFiles list
    for fileName in configFiles: 
      # Get filename extension.
      extension = os.path.splitext(fileName)[1]
            
      # If .ini file.
      if extension == ".ini" :
        # Parse INI config file.
        configParser.read(configPath+'/'+fileName)
      
      # [TODO]
      # If .json file.
      elif extension == ".json" :
        # Parse JSON config file.
        pass
     
    # Get config parser sections.
    sections = configParser.sections()
    
    # Get all sections.
    for section_name in sections:
      self.config[section_name] = configParser[section_name]
    
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def loadLanguage(self, language):
    
    """ 
      loadLanguage : Get language file and load values in languages var.
      ---
      Parameters
        language : String
          Language to load.
      ---
      Return : None
    """
    
    # Languages path.
    languagesPath = ROOT_PATH+"languages"
    
    # Language file path.
    languageFile = languagesPath+'/'+language+".json"
      
    # [TODO]
    # Parse JSON language file.
    pass
    
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getDomains(self):
    
    """ 
      getDomains : Acquire domains available list. 
      Parse haroun/domains folder to define list of available domains.
      ---
      Return : List[String]
        Domains available list.
    """
    
    # Dict of domains instances.
    domains = {}
    
    # List of domains names.
    domains_names = []
    
    # Browse through domains files 
    for(dirpath, dirnames, filenames) in os.walk(ROOT_PATH+"domains"):
      # Remove filenames extensions
      filenames = [os.path.splitext(filename)[0] for filename in filenames]
      # Add domains filenames without extension to domains list.
      domains_names.extend(filenames)
      break
    
    # Instanciate domains to retrieve intent handlers.
    for domain_name in domains_names :
     
      # Check if domain exist and is not __init__ file.
      if domain_name and domain_name != '__init__' :
      
        # [DEBUG]
        #print(f"BEFORE domain {domain_name} instantiation.")        
        
        # Instanciate domain.
        domains[domain_name] = Domain(domain_name)
        
        # [DEBUG]
        #print(f"AFTER domain {domain_name} instantiation.")
    
    # Return
    return domains
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getSkills(self):
    
    """ 
      getSkills : Acquire skills available list. 
      Parse haroun/skills folder to define list of available skills.
      ---
      Return : List[String]
        List des nom de skills
    """
    
    # Browse through skills files 
    skills = []
    for(dirpath, dirnames, filenames) in os.walk(ROOT_PATH+"skills"):
      # Remove filenames extensions
      filenames = [os.path.splitext(filename)[0] for filename in filenames]
      # Add directory filenames without extension to skills list.
      skills.extend(filenames)
      break
    
    # Return
    return skills
    
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getIntents(self):
    
    """ 
      getIntents : Acquire intents file list and create a all.ini intents file. 
      Parse haroun/intents folder to list of intents file.
      Normally one file per available domains.
      Generate one intents file and parse it with rhasspy-nlu.
      ---
      Return : intents 
        Rhasspy NLU intents list.
    """
    
    # Intents directory path.
    intentsPath=ROOT_PATH+"intents/"
    
    # Browse through intents files 
    intentsFiles = []    
    for(dirPath, dirNames, fileNames) in os.walk(intentsPath):
      # [DEBUG]
      #print('Looking in intent directory : '+intentsPath+", listing files :")
      #print(fileNames)
      intentsFiles.extend(fileNames)
      break
      
    """ Write all intents in intents/.all.ini file. """
    
    # Open intents/.all.ini, a file that will contains all intents.
    allIntentsFilePath  = intentsPath+".all.ini"
          
    # Open intents/.all.ini in write mode
    with open(allIntentsFilePath, 'w+') as allIntentsFileBuffer:
      
      # Iterate through intentsFiles list
      for fileName in intentsFiles:
        
        # Construct file path.
        filePath = intentsPath+fileName
        
        # Open each file in read mode
        with open(filePath) as fileBuffer:
  
          # Read the data from file. 
          fileIntents = fileBuffer.read()
          
          # Write it in allIntentsFileBuffer and add '\n\n' to enter data from next line
          allIntentsFileBuffer.write("# "+fileName+" file content : \n")
          allIntentsFileBuffer.write(fileIntents+"\n\n")
          
              
    # Load file for rhasspy-nlu.
    intents = rhasspynlu.parse_ini(Path(allIntentsFilePath))
    
    # [DEBUG]
    #print('Intents : ')
    #print(intents)
    #print('----------------------------------------')
    
    # Return
    return intents
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def executeSlotsPrograms(self):
    
    """ 
      executeSlotsPrograms : Execute slots programs. Slots programs are independents scripts that generate slots.
      ---
      Return : None
    """
    
    # Slots directory path.
    slotsPath=ROOT_PATH+"slots/"
    
    # Slots programs directory path.
    slotsProgramPath=ROOT_PATH+"slotsPrograms/"
    
    # Browse through slots files 
    slotsProgramsFiles = []    
    for(dirPath, dirNames, fileNames) in os.walk(slotsProgramPath):
      # [DEBUG]
      #print('Looking in slotsPrograms directory : '+slotsProgramPath+", listing files :")
      #print(fileNames)
       # Add fileNames to slotsProgramsFiles list.
      slotsProgramsFiles.extend(fileNames)
      break
      
    # Iterate through slotsProgramsFiles list
    for programSlotFileName in slotsProgramsFiles:
      
      # Get file name without extension as programSlotName.
      programSlotName = os.path.splitext(programSlotFileName)[0]
    
      # Get program path.
      program_path = slotsProgramPath+programSlotFileName
      
      # Create slot file with program slot name.
      slotFilePath = slotsPath+programSlotName
      # If slot file doesn't already exist.
      if not os.path.exists(slotFilePath) :
      
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
        slotFileContent = output.decode()
                
        # Open file : create if not exist, truncate if exist.
        with open(slotFilePath, 'w') as slotFile:
          # Write program slot file execution output.
          slotFile.write(f"{slotFileContent}")
          
      else:
        # Error message.
        print(f"Slot {programSlotName} already exist. Program slot file '{programSlotFileName}' can't be executed. Delete slot {programSlotName} to re-generate it.")
        
    # Return
    return None
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getSlots(self):
    
    """ 
      getSlots : Acquire all slots files and create a Rhasspy NLU slots dict. 
      ---
      Return : Rhasspy NLU slots
        Rhasspy NLU slots dict.
    """
    
    # Slots directory path.
    slotsPath=ROOT_PATH+"slots/"
    
    # Browse through slots files 
    slotsFiles = []    
    for(dirPath, dirNames, fileNames) in os.walk(slotsPath):
      # [DEBUG]
      #print('Looking in slots directory : '+slotsPath+", listing files :")
      #print(fileNames)
      # Add fileNames to slotsFiles list.
      slotsFiles.extend(fileNames)
      break
    
    """ Get slots from domains files and add them to slots files. """
    
    # [TO DO]
    #self.domains
    
    """ Create slots dict from slots files. """
    
    # Replacement slots dict.
    slots = {}
      
    # Iterate through slotsFiles list
    for fileName in slotsFiles:
      
      # Construct file path.
      filePath = slotsPath+fileName
      
      # Retrieve slot file content.
      with open(filePath) as fileBuffer:
        
        # Read the data from file. 
        FileContent = fileBuffer.read()
        
        # Retrieve all slots entries in file and separate them with pipe.
        slots_entries = FileContent.replace("\n", " | ")
      
        # Construct slots.
        key = "$"+fileName
        value = [rhasspynlu.Sentence.parse(slots_entries)]
        
        # Add it to replacement slots dict.
        slots[key] = value
    
    # Return
    return slots
      
  
  # ! - A.I. Training.
  
  @debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def nlu_training(self):
    
    """ 
      nlu_training : Acquire domains knowledge. 
      Transform intents into graph training, replace slots if necessary.
      ---
      Return : None
    """
    
    # [DEBUG]
    #print('Replacement slots : ')
    #print(self.slots)
    #print('----------------------------------------')
    
    # Generate intents training graph from list of known intents.
    self.intents_graph = rhasspynlu.intents_to_graph(self.intents, replacements = self.slots)
            
    # End.
    return
  
  # ! - Stimulus management.
    
  def generateStimulus(self, source, source_id, sentence, user_id, interaction_id, parent_interaction_id, origin_datetime):
  
    """ 
      generateStimulus : Generate Stimulus concept object. 
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
    
    # Create stimulus from script call infos.
    stimulus = Stimulus(source, source_id, sentence, user_id, interaction_id, parent_interaction_id, origin_datetime)
    
    # Check if stimulus is valid.
    if(stimulus.isValid()):
      # End.
      return stimulus
    else:
      # Error.
      return False
    
    
  # ! - Interaction creation.
  
  def createInteraction(self, stimulus):
  
    """ 
      createInteraction : Generate Interaction concept object. 
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
  
  def manageInteraction(self, interaction):
    
    """ 
      manageInteraction : Manage interaction. 
      Interaction analysis, check NLU of the interaction sentence to defined instance.
      Correct slots if neccessary.
      ---
      Parameters
        interaction : Interaction
          Interaction concept object generate from trigger Stimulus.
      ---
      Return : Interaction
        Modified interaction with domain and skill infos, None if error.
    """
    
    # Interaction interpretation. 
    modified_interaction = self.interpreter(interaction)
    # if interpretation failed.
    if not modified_interaction :
      # Return interaction message error.
      interaction.addError(f"Interaction interpretation failed. [Error #4].")
    else:
      # [DEBUG]
      #interaction.addResponse(str(interaction.intent))
      print(str(interaction.intent))
      # Defined Domain & Skill for this interaction.
      modified_interaction = self.analysis(modified_interaction)
      # If Interaction analysis failed. 
      if not modified_interaction :
        # Return interaction message error.
        interaction.addError(f"Interaction analysis failed. [Error #10].")
      else:
      
        # [TODO]
        # Get Consciousness state of mind to add in the interaction.
        # Consciousness current interaction states may be used 
        # by interaction to generate alternative response during skill execution.
        modified_interaction.mind = self.getStatesOfMind()
        
        # Execute the Skill via the Domain.
        modified_interaction = self.executeSkill(modified_interaction)
        # If Interaction execution failed. 
        if not modified_interaction :
          # Return interaction message error.
          interaction.addError(f"Interaction skill execution failed. [Error #20].")
        else:   
          # Generate interaction response.
          modified_interaction = self.response(modified_interaction)
          # If response creation failed. 
          if not modified_interaction :
            # Return interaction message error.
            interaction.addError(f"Interaction skill execution failed. [Error #20].")
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
    
    #

    
    # Stimulus sentence pre-treatment.
    interaction.stimulus.sentence = interaction.stimulus.sentence.lower()
    interaction.stimulus.sentence = interaction.stimulus.sentence.replace(',',"")
    
    # [DEBUG]
    #print('Interaction sentence : '+interaction.stimulus.sentence)
    #print('----------------------------------------')
    
    # Perform intent recognition in Interaction sentence thanks to training graph.
    try:
      recognitions = rhasspynlu.recognize(interaction.stimulus.sentence, self.intents_graph, fuzzy=True)
    except ZeroDivisionError :
      # Return
      return None
      
    # [DEBUG]
    #print("Recognitions  : ")
    #print(recognitions)
    #print('----------------------------------------')
    
    # If rhasspynlu perform recognition without problem.
    if not recognitions :
      # Return
      return None
      
    # Format recognitions as dict.
    recognitions_dict = recognitions[0].asdict()
    # Format recognition dict as json string.
    recognition_string = json.dumps(recognitions_dict)
    
    # Format recognition as Object.
    interaction.recognition = json.loads(recognition_string)
    
    # Retrieve recognition duration
    interaction.recognition_duration = interaction.recognition['recognize_seconds'] 
    
    # Retrieve stimulus duration
    interaction.stimulus.duration = interaction.recognition['wav_seconds']
    
    # Define intent.
    interaction.intent.checkRecognition(interaction.stimulus, interaction.recognition)
    
    # Return
    return interaction   

  #@debug("verbose", True)
  def analysis(self, interaction):
    
    """ 
      Analyse interaction to define skill from intent. 
      
      Interaction analysis, check NLU recognition dict of the interaction to define skill to apply.
      Correct intent entities if necessary and define slots from them.
      ---
      Parameters
        interaction : Interaction
          Interaction concept object generate from trigger Stimulus.
      ---
      Return : Interaction, None if error.
        Modified interaction with domain and skill infos.      
    """
    
    # Define interaction domain and method name.
    interaction_domain_name = None
    interaction_method_name = None
    
    # [DEBUG]
    #print(f"Interaction intent found : {interaction.intent.label}")
    #print(f"Intent handlers : {Domain.intents_handlers}")
    
    # Check if there is a domain method that handle this intent.
    if interaction.intent.label in Domain.intents_handlers.keys():
      # Check if interaction domain found.
      if Domain.intents_handlers[interaction.intent.label] :
        # Define interaction domain name.
        interaction_domain_name = Domain.intents_handlers[interaction.intent.label]['domain']
        # Retieve interaction method name.
        interaction_method_name = Domain.intents_handlers[interaction.intent.label]['method']
      else:
        # Error message.
        interaction.addError(f"No domain '{interaction.intent.label}' found for this intent. [Error #5]")
        # Return None (error)
        return None
    else:
      # Error message.
      interaction.addError(f"No handler for intent '{interaction.intent.label}' found. [Error #6]")
      # Return None (error)
      return None
    
    # Retrieve domain instance for interaction.
    interaction.domain = self.domains[interaction_domain_name]
    
    # DEPRECATED CODE : Since Intent Handler decorator.
    # Check if method exist. 
    #if interaction_method_name is not None :
    #  if not interaction.domain.methodExist(interaction_method_name) :
    #    # Error message.
    #    interaction.addError(f"No method '{interaction.intent.label}' found for this intent on domain '{interaction_domain_name}'. [Error #5]")
    #    # Return None (error)
    #    return None
      
    # instantiation interaction skill.
    interaction.skill = Skill(interaction_domain_name, interaction_method_name)
      
    # Return modified interaction.
    return interaction
        
  def executeSkill(self, interaction):
    
    """ 
      executeSkill : Execute Skill via Domain function.  
      Instanciate the correct domain class for the skill. Prepare domain method call with correct info from intent. Then execute the method and retrieve execute return infos.
      ---
      Parameters
        interaction : Interaction
          Interaction concept object generate from trigger Stimulus.
      ---
      Return : Interaction
        Modified interaction with domain and skill infos, None if error/      
    """
    
    # Get domain methods args list to prepare skill.
    method_args = interaction.domain.methodGetArgs(interaction.skill.method_name)
    
    # Prepare skill for execution.
    preparation_flag = interaction.skill.prepare(interaction.intent, method_args)
    
    # Excute skill on domain.
    execution_flag = interaction.domain.executeSkill(interaction.skill)
    
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
    
    # Retrieve skill execution return values.
    interaction.addResponse(interaction.skill.return_values)
    
    # Return modified interaction
    return interaction

  # ! Consciousness (Reflexivity)

  def getStatesOfMind(self):
    
    """ 
      getStatesOfMind : method, allow reflexivity management.
      --- 
      Return : 
        Curent states of mind.
    """
    
    # Re-calculate awareness values.
    
    
    # Return
    return {}


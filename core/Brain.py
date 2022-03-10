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
# Import rhasspynlu
import rhasspynlu
# Import Path from pathlib
from pathlib import Path
#
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
DOSSIER_COURRANT = os.path.dirname(os.path.abspath(__file__))+'/'
DOSSIER_RACINE = os.path.dirname(os.path.abspath(DOSSIER_COURRANT))+'/'
sys.path.append(DOSSIER_RACINE)
#
#
#
class Brain:  
  
  """ Concepts and consciousness class management for Haroun. """
    
  def __init__(self):
    
    """ Brain class constructor. """
    
    # Consciousness (Reflexivity).
    self.conscious = Conscious()
    self.ego = Ego()
    
    # Available domains list. 
    self.domains = self.getDomains()
    
    # Available skills list. 
    #self.skills = self.getSkills()
    
    # Available intents list. 
    self.intents =  self.getIntents()
    
    # Available slots for replacements in intents.
    self.slots = self.getSlots()
    
    # IntentToSkill dictionnary, create a dict for "Intent to Skill" conversion. 
    self.intentToSkill = {
      "OH_QUESTION" : {
        "class" : "openhab",
        "method" : "question"
      },
      "OH_ACTION" : {
        "class" : "openhab",
        "method" : "action"
      }
    }
    
    # Training rhasspy-nlu graph from known intents. 
    self.intents_graph = None
  
    # Memories 
    self.memories = Memory()
    
    # Training brain by creating intents graph.
    self.nlu_training()

  # ! - Initialisation.
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getDomains(self):
    
    """ 
      Acquire domains available list. 
      
      Parse haroun/domains folder to define list of available domains.
      ---
      Returns
        domains : List[String]
          Domains avialable list.
    
    """
    
    # Browse through domains files 
    domains = []
    for(dirpath, dirnames, filenames) in os.walk(DOSSIER_RACINE+"domains"):
      # Remove filenames extensions
      filenames = [os.path.splitext(filename)[0] for filename in filenames]
      # Add directory filenames without extension to domains list.
      domains.extend(filenames)
      break
    
    # Return
    return domains
  
  #@debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getSkills(self):
    
    """ 
      Acquire skills available list. 
      
      Parse haroun/skills folder to define list of available skills.
      
       
      ____
      Returns
        skills : List[String] : List des nom de skills
      void
    
    """
    
    # Browse through skills files 
    skills = []
    for(dirpath, dirnames, filenames) in os.walk(DOSSIER_RACINE+"skills"):
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
      Acquire intents file list and create a all.ini intents file. 
      
      Parse haroun/intents folder to list of intents file.
      Normally one file per available domains.
      Generate one intents file and parse it with rhasspy-nlu.
      
      Returns
      _______
      intents : Rhasspy NLU intents list.
    
    """
    
    # Intents directory path.
    intentsPath=DOSSIER_RACINE+"intents/"
    
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
  def getSlots(self):
    
    """ 
      Acquire slots file list and create a slots dict. 
      
      Returns
      _______
      slots : Rhasspy NLU slots dict.
    
    """
    
    # Slots directory path.
    slotsPath=DOSSIER_RACINE+"slots/"
    
    # Browse through slots files 
    slotsFiles = []    
    for(dirPath, dirNames, fileNames) in os.walk(slotsPath):
      # [DEBUG]
      #print('Looking in slots directory : '+slotsPath+", listing files :")
      #print(fileNames)
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
      Acquire domains knowledge. 
      
      Transform intents into graph training, replace slots if necessary.
      
      Returns
      _______
      void
    
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
    
  def generateStimulus(self, source, source_id, sentence, parent_id):
  
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
        parent_interaction_id : String (optionnal)
          Uniq identifier for parent interaction if Stimulus is due cause of previous interaction. [Default = null]
      ---
      Returns
        stimulus : Stimulus
          Stimulus concept object created with scripts call infos.
    """
    
    # Create stimulus from script call infos.
    stimulus = Stimulus(source, source_id, sentence, parent_id)
    
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
      Generate Interaction concept object. 
      Transform script call infos, to create a Haroun Stimulus containing infos to generate an Interaction.
      ---
      Parameters
        stimulus : Stimulus
          Stimulus source origin of the interaction.
      ---
      Returns
        Interaction : Modified interaction with domain and skill infos.
          Return None if error.
    """
    
    # Create interaction from stimulus.
    interaction = Interaction(stimulus)
    
    # Return interaction ready to interact.
    return interaction
    
  # ! - Interaction management.
  
  def manageInteraction(self, interaction):
    
    """ 
      Manage interaction. 
      Interaction analysis, check NLU of the interaction sentence to defined instance.
      Correct slots if neccessary.
      ---
      Parameters
        interaction : Interaction
          Interaction concept object generate from trigger Stimulus.
      ---
      Returns
        Interaction : Modified interaction with domain and skill infos.
          Return None if error.
    """
    
    # Interaction interpretation. 
    modified_interaction = self.interpreter(interaction)
    # if interpretation failed.
    if not modified_interaction :
      # Return interaction message error.
      interaction.addError(f"Interaction interpretation failed. [Error #4].")
    else:
      # [DEBUG]
      interaction.addResponse(str(interaction.intent))
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
      Interpreter method, apply NLU analysis on Interaction sentence.
      Interpretation of Interaction sentence via rhasspy-nlu.
      Try to retrieve a recognition dict, if success then create define an the interaction intent attribut from it.
      ---
      Parameters
        interaction : Interaction
          Interaction concept object generate from trigger Stimulus.
      ---
      Returns
        interaction : Interpretation of interaction success, recognition and intent attributs are now defined.
    """
    
    # [DEBUG]
    #print('Interaction sentence : '+self.stimulus.sentence)
    #print('----------------------------------------')
    
    # Stimulus sentence pre-treatment.
    interaction.stimulus.sentence = interaction.stimulus.sentence.lower()
    interaction.stimulus.sentence = interaction.stimulus.sentence.replace(',',"")
    
    # Perform intent recognition in Interaction sentence thanks to training graph.
    recognitions = rhasspynlu.recognize(interaction.stimulus.sentence, self.intents_graph, fuzzy=True)
    
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
      Returns
        Interaction : Modified interaction with domain and skill infos.
          Return None if error.
      
    """
    
    # Define interaction domain and method name.
    interaction_domain_name = None
    interaction_method_name = None
    
    # Find Domain from Interaction Intent label.
    for domain in self.domains :
      # If domain match label.
      if interaction.intent.label.split(".")[0].lower() == domain.lower():
        # Define interaction domain name.
        interaction_domain_name = domain
        # Retieve interaction method name.
        interaction_method_name = interaction.intent.label.split(".")[1]
    
    # Check if interaction domain found.
    if interaction_domain_name is None :
      # Error message.
      interaction.addError(f"No domain '{interaction.intent.label}' found for this intent. [Error #5]")
      # Return None (error)
      return None
      
    # Instanciate domain on interaction.
    interaction.domain = Domain(interaction_domain_name)
      
    # Check if method exist.
    if interaction_method_name is not None :
      if not interaction.domain.methodExist(interaction_method_name) :
        # Error message.
        interaction.addError(f"No method '{interaction.intent.label}' found for this intent on domain '{interaction_domain_name}'. [Error #5]")
        # Return None (error)
        return None
      
    # Instanciation interaction skill.
    interaction.skill = Skill(interaction_domain_name, interaction_method_name)
      
    # Return modified interaction.
    return interaction
        
  def executeSkill(self, interaction):
    
    """ 
      Execute Skill via Domain function.  
      
      Instanciate the correct domain class for the skill. Prepare domain method call with correct info from intent. Then execute the method and retrieve execute return infos.
      
      Parameters
      ----------
      interaction : Interaction
        Interaction concept object generate from trigger Stimulus.
      Returns
      _______
      Interaction : Modified interaction with domain and skill infos.
        Return None if error.
      
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
      Create interaction response.  
      Parse interaction data, to generate an response with datas and sentence.
      ---
      Parameters
        interaction : Interaction
          Interaction for which to generate response.
      ---
      Returns
        Interaction : Modified interaction with domain and skill infos.
          Return None if error.
    """
    
    # Retrieve skill execution return values.
    interaction.addResponse(interaction.skill.return_values)
    
    # Return modified interaction
    return interaction

  # ! Consciousness (Reflexivity)

  def getStatesOfMind(self):
    
    """ 
      getStatesOfMind method, allow reflexivity management.
      --- 
      Return 
        Curent states of mind.
      
    """
    
    # Re-calculate awareness values.
    
    
    # Return
    return {}


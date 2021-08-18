#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : 
#
#
# Haroun dependancies : 
#
#
# Import consciousness class.
from core.consciousness.Conscious import *
from core.consciousness.Me import *
#
# Import concepts class.
from core.concepts.Domain import *
from core.concepts.Skill import *
from core.concepts.Stimulus import *
from core.concepts.Interaction import *
from core.concepts.Intent import *
from core.concepts.Memory import *
# Import functools
from functools import *
# Import utils
from utils.debug import *
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
    self.skills = self.getSkills()
    
    # Available intents list. 
    self.intents =  self.getIntents()
    
    # Available slots for replacements in intents.
    self.replacements_slots = self.getSlots()
    
    # IntentToSkill dictionnary, create a dict for "Intent to Skill" conversion. 
    self.intentToSkill = {}
    
    # Training rhasspy-nlu graph from known intents. 
    self.intents_graph = None
  
    # Memories 
    self.memories = Memory()
    
    # Training brain by creating intents graph.
    self.training()

  # ! - Initialisation.
  
  @debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getDomains(self):
    
    """ 
      Acquire domains available list. 
      
      Parse haroun/domains folder to define list of available domains.
      
      Returns
      _______
      void
    
    """
    
    # Browse through domains files 
    files = []
    for(dirpath, dirnames, filenames) in os.walk(DOSSIER_RACINE+"domains"):
      files.extend(filenames)
      break
    
    # Load every domain class to create all specifics slots.
    domains = {}
    for file in files :
      print("Domain : "+file)
      #loadSpecificsSlots = getattr(__import__("domains."+file.split('.')[0], fromlist=["loadSpecificsSlots"]), "loadSpecificsSlots")
    
    # Return
    return files
  
  @debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getSkills(self):
    
    """ 
      Acquire skills available list. 
      
      Parse haroun/skills folder to define list of available skills.
      
      Returns
      _______
      void
    
    """
    
    # Browse through skills files 
    files = []
    for(dirpath, dirnames, filenames) in os.walk(DOSSIER_RACINE+"skills"):
      files.extend(filenames)
      break
    
    # Return
    return files
    
  
  @debug("verbose", True)
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
  
  @debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def getSlots(self):
    
    """ 
      Acquire slots file list and create a replacements_slots dict. 
      
      Returns
      _______
      replacement_slot : Rhasspy NLU slots dict.
    
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
      
    """ Create replacements_slots dict from slots files. """
    
    # Replacement slots dict.
    replacements_slots = {}
      
    # Iterate through slotsFiles list
    for fileName in slotsFiles:
      
      # Construct file path.
      filePath = slotsPath+fileName
      
      # Retrieve slot file content.
      with open(filePath) as fileBuffer:
        
        # Read the data from file. 
        FileContent = fileBuffer.read()
        
        # Retrieve all slots in file and separate them with pipe.
        slots = FileContent.replace("\n", " | ")
      
        # Construct replacements_slots.
        key = "$"+fileName
        value = [rhasspynlu.Sentence.parse(slots)]
        
        # Add it to replacement slots dict.
        replacements_slots[key] = value
    
    # Return
    return replacements_slots
      
  
  # ! - NLU training.
  
  @debug("verbose", True)
  @lru_cache(maxsize=128, typed=True)
  def training(self):
    
    """ 
      Acquire domains knowledge. 
      
      Transform intents into graph training, replace slots if necessary.
      
      Returns
      _______
      void
    
    """
    
    # [DEBUG]
    #print('Replacement slots : ')
    #print(self.replacements_slots)
    #print('----------------------------------------')
    
    # Generate intents training graph from list of known intents.
    self.intents_graph = rhasspynlu.intents_to_graph(self.intents, replacements = self.replacements_slots)
            
    # End.
    return
      
    
  def SkillsIntentsAnalysis(self, interaction):
   
    """ 
      Create a conversion dict from intent to skill. 
      
      .skills files contains "Intent to Skill" association for each domain.
      This function retrieve Skills files list for each domain and parse them to fill the "Intent to Skill" associated dictionnary.
      
      Parameters
      ----------
      interaction : Interaction
        Interaction created from stimulus.
      
      Returns
      _______
      void
    
    """
    
    # Retrieve Skills files list.
    
    # For each file.
    
      # Load "Intent to Skill" file. 
  
    # End.
    return
  

  # ! - Stimulus management.
    
  def generateStimulus(self, source, source_id, sentence, parent_id):
  
    """ 
      Generate Stimulus concept object. 
      
      Transform script call infos, to create a Haroun Stimulus containing infos to generate an Interaction.
      
      Parameters
      ----------
      source : String
        Label for stimulus source origin.
      source_id : String
        Uniq identifier for stimulus source origin.
      sentence : String (optionnal)
        Sentence of the stimulus. [Default = '']
      parent_interaction_id : String (optionnal)
        Uniq identifier for parent interaction if Stimulus is due cause of previous interaction. [Default = null]
      
      Returns
      _______
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
    
    
  # ! - Interaction management.
  
  def createInteraction(self, stimulus):
  
    """ 
      Generate Interaction concept object. 
      
      Transform script call infos, to create a Haroun Stimulus containing infos to generate an Interaction.
      
      Parameters
      ----------
      stimulus : Stimulus
        Stimulus source origin of the interaction.
          
      Returns
      _______
      interaction : Interaction
        Interaction concept object created with stimulus infos.
      
    """
    
    # Create interaction from stimulus.
    interaction = Interaction(stimulus)
    
    # Return interaction ready to interact.
    return interaction
    
    
  def initiate(self, interaction):
    
    """ 
      Initiate interaction. 
      
      Interaction analysis, check NLU of the interaction sentence to defined instance.
      Correct slots if neccessary.
      
      
      Parameters
      ----------
      interaction : Interaction
        Interaction concept object generate from trigger Stimulus.
      
      
      Returns
      _______
      interaction : Interaction
        Interaction concept object modified with intents and slots.
      
    """
    
    # Interaction sentence NLU analysis thanks to intents training graph.
    if not interaction.interpreter(self.intents_graph) :
      # [DEBUG]
      print("Interaction interpretation failed. [Error #4].")
      print('----------------------------------------')
    
    # Defined Skill that is associated with this intents.
    skill = self.analysis(interaction)
    
    # If Interaction analysis defined a skill 
    if(skill):
      # And then execute the Skill via the Domain.
      skill_execution_results = self.executeSkill(skill)
    else:  
      # [DEBUG]
      return
      
    # If there is a skill execution result.
    if(skill_execution_results):
      # We have to analyse results to create an interaction response.
      response_infos = skill.analysis(skill_execution_results)
      # Add response_infos to interaction.response
      interaction.response.add(response_infos)
      
      
    # Generate interaction response.
    self.response(interaction)
    
    # Return modified interaction.
    return interaction    

  #@debug("verbose", True)
  def analysis(self, interaction):
    
    """ 
      Analyse interaction to define skill from intent. 
      
      Interaction analysis, check NLU recognition dict of the interaction to define skill to apply.
      Correct intent entities if necessary and define slots from them.
      
      Parameters
      ----------
      interaction : Interaction
        Interaction concept object generate from trigger Stimulus.
      
      Returns
      _______
      skill : Skill
        Skill concept object defined from Interaction intent.
      
    """
    
    # [DEBUG]
    print('----------------------------------------')
    print("Intent object  : ")
    print(interaction.intent)
    print('----------------------------------------')
    # [DEBUG]
    return
    
    # Find Skill from Interaction Intent label.
    try:
      skill_infos = self.intentToSkill[interaction.intent.label]
    except KeyError:
      print("No skill found for this intent. [Error #5]")
    
    # [DEBUG]
    return
    
    # Create Skill from skill_info.
    skill = Skill()
    
    # Return skill
    return skill
        
  def executeSkill(self):
    
    """ 
      Execute Skill via Domain function.  
      
      Instanciate the correct domain class for the skill. Prepare domain method call with correct info from intent. Then execute the method and retrieve execute return infos.
      
      Parameters
      ----------
      skill : Skill
        Skill concept object to execute.
      
      Returns
      _______
      response_infos : Dict
        Domain method execution returned infos.
      
    """
    
    # We can find a Domain for this Skill.
    domain = skill.getDomain()
  
    # Execute the Skill via the Domain, and retrieve returned infos.
    response_infos = domain.execute(skill)
    
    # Return response_infos.
    return response_infos

  def response(self, interaction):
    
    """ 
      Create interaction response.  
      
      Parse interaction data, to generate an response with datas and sentence.
      
      Parameters
      ----------
      interaction : Interaction
        Interaction for which to generate response.
      
      Returns
      _______
      void
      
    """
    
    # Generate response from interaction.
    
    
    return

  # ! Consciousness (Reflexivity)

  def awareness(self):
    
    """ 
      Awareness method, allow reflexivity management.  
      
      Returns
      _______
      void.
      
    """
    
    # Re-calculate awareness values.
    
    
    # Return
    return


#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#
# Core dependencies : 
from core.Brain import *
#
# ! - Globals : 
#
# Text encode type
Encodage = 'utf-8'
#
#
class Haroun:
  
  """ Haroun home assistant main class. """
  
  def __init__(self):
    
    """ Haroun class constructor """
    
    # Brain instanciation.
    self.brain = Brain()


  def getStimulus(self, source, source_id, sentence, parent_id): 
    
    """ 
      Retrieve call info. 
    
      Use haroun brain to create and return Stimulus Object.
      
      Returns
      _______
      stimulus : Stimulus
        Stimulus concept object created from call infos.
    """
    
    # Generate stimulus from call info.
    stimulus = self.brain.generateStimulus(source, source_id, sentence, parent_id)
    
    # If we manage to understand stimulus.
    if(stimulus):
      # Ask Haroun to initiate interaction.
      if(self.brain.initiate(interaction)):
        # When interaction treatment is done, return interaction answer.
        return interaction.answer
      else:
        # [DEBUG]
        return "Désolé, mais je n'ai pas compris ce que je dois faire."
    else:
      # [DEBUG]
      return "Que voulez vous dire par : " + interaction.sentence
    
    # Return stimulus.
    return stimulus
    
    
  def interact(self, stimulus):
    
    """
      Manage assistant interaction.
  
      Initiate interaction from stimulus in Haroun Brain.
  
      Parameters
      ----------
      source : int
        Description of arg1
      source_id : str
        Description of arg2
      sentence : str
        Description of arg2
      parent_id : str
        Description of arg2
        
      Returns
      -------
      void
    """
        
    # Use brain to analyse stimulus and create interaction.
    interaction = self.brain.createInteraction(stimulus, Encodage)
    # If we manage to understand stimulus, we can know initiate interaction.
    if(interaction):
      # Ask Haroun to initiate interaction.
      interaction = self.brain.initiate(interaction)
      # If interaction was treated with success.
      if(interaction):
        # Return interaction answer.
        return interaction.answer
      else:
        # [DEBUG]
        return "Désolé, mais je n'ai pas compris ce que je dois faire."
    else:
      # [DEBUG]
      return "Que voulez vous dire par : " + interaction.sentence


#####################################################################################################   
#                                            MAIN                                                   #
#####################################################################################################   

# ! Init Haroun :

'''Haroun instanciation'''
Haroun = Haroun()

# Execute if run as script. 
if __name__ == "__main__":

  '''Main executed code, for script call.'''
  
  # ! - Script call params : 
  
  # If sentence is provide.
  if(len(sys.argv) > 1):
    # Sentence from triggered interaction.
    sentence = sys.argv[1]
  else:
    # [DEBUG]
    print("Vous n'avez rien demandé")
    # End.
    sys.exit()
  
  # DEBUG
  print(sentence)
  
  # ! - Init interaction :
  
  # Launch Haroun to interact with stimulus.
  answer = Haroun.interact(sentence)
  
  # [DEBUG]
  print(answer.texte)
  
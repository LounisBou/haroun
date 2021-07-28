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


  def call(self, source, source_id, sentence, parent_interaction_id): 
    
    """ 
      Retrieve call info. 
    
      Use haroun brain to create and return Stimulus Object.
      
      Parameters
      ----------
      source : String
        Label for stimulus source origin.
      source_id : String
        Uniq identifier for stimulus source origin.
      sentence : String (optionnal)
        Sentence of the stimulus. [Default = '']
      parent_interaction_id : String (optionnal)
        Uniq identifier for parent interaction if Stimulus is due cause of previous interaction. [Default = None]
      
      Returns
      _______
      stimulus : Stimulus
        Stimulus concept object created from call infos.
    """
    
    # Generate stimulus from call info.
    stimulus = self.brain.generateStimulus(source, source_id, sentence, parent_interaction_id)
    
    # If we manage to understand stimulus.
    if(stimulus):
      # Check if stimulus need interaction.
      if(stimulus.needInteraction()):
        # Haroun create an interaction with user.
        interaction = self.brain.createInteraction(stimulus);
        # If interaction is ready.
        if(interaction):
          # Ask Haroun to initiate interaction.
          self.brain.initiate(interaction)
          # When interaction treatment is done, return interaction response.
          return interaction.response
        else:
          # [DEBUG]
          print("Interaction error. [Error #3]")
      else:
        # [DEBUG]
        return ("No interaction needed. [Error #2]")
    else:
      # [DEBUG]
      return ("Stimulus error. [Error #1]")
    
    # [DEBUG]
    return False
    

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
  
  # ! - Init interaction :
  
  # Launch Haroun stimulus analisys.
  response = Haroun.call("DEBUG", 0, sentence, None)
  
  # [DEBUG]
  print(response)
  
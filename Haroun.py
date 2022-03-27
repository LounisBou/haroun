#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#
# Import sys
import sys
# Core dependencies : 
from core.Brain import Brain
#
# ! - Globals :  coucou
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
      Response : String 
        Interaction response text.
    """
    
    # Generate stimulus from call info.
    stimulus = self.brain.generateStimulus(source, source_id, sentence, parent_interaction_id)
    
    # If we manage to understand stimulus.
    if stimulus :
      # Check if stimulus need interaction.
      if stimulus.needInteraction() :
        # Haroun create an interaction with user.
        interaction = self.brain.createInteraction(stimulus);
        # If interaction is ready.
        if interaction :
          # Ask Haroun to manage interaction.
          interaction = self.brain.manageInteraction(interaction)
          # When interaction treatment is done, get interaction response msg_text.
          interaction_reponse_msg = f"{interaction.response.msg_text}"
          # If error occured.
          if interaction.error :
            # Add error message to interaction response error_text.
            interaction_reponse_msg = f"Error : {interaction.response.error_text}"
          # Return interaction response message.
          return interaction_reponse_msg
        else:
          # [DEBUG]
          return "Interaction error. [Error #3]" 
      else:
        # [DEBUG]
        return "No interaction needed. [Error #2]"
    else:
      # [DEBUG]
      return "Stimulus error. [Error #1]"
    
    # [DEBUG]
    return "Call error. [Error #0]"
    

#####################################################################################################   
#                                            MAIN                                                   #
#####################################################################################################   

# ! Init Haroun :

# Execute if run as script. 
if __name__ == "__main__":

  '''Haroun instanciation'''
  Haroun = Haroun()

  '''Main executed code, for script call.'''
  
  # ! - Script call params : 
  
  # If sentence is provide.
  if(len(sys.argv) > 1):
    # Sentence from triggered interaction.
    sentence = sys.argv[1]
     
     # ! - Init interaction :
      
    # Launch Haroun stimulus analisys.
    response = Haroun.call("DEBUG", 0, sentence, None)
    
    # [DEBUG]
    print(response)
  else:

    while True :
      
      # Ask user for sentence.
      sentence = input(" -?- : ")
      
      # ! - Init interaction :
      
      # Launch Haroun stimulus analisys.
      response = Haroun.call("DEBUG", 0, sentence, None)
      
      # [DEBUG]
      print(response)
  
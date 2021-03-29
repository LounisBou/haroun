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
    
    
  def interact(self, source, source_id, sentence, parent_id):
    
    """
      Manage assistant interaction.
  
      Initiate interaction in Haroun Brain.
  
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

    # On demande à Haroun d'analyser la question.
    if(self.cerveau.analyse(question, Encodage) == 1):
      # On demande à Haroun d'exécuter la demande.
      if(self.cerveau.execute() == 1):
        # Reponse
        return self.cerveau.reponse.texte
      else:
        # DEBUG
        return "Désolé, mais je n'ai pas compris ce que je dois faire."
    else:
      # DEBUG
      return "Que voulez vous dire par : " + self.cerveau.question.texte


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
  print(question)
  
  # ! - Init interaction :
  
  # Launch Haroun interaction.
  answer = Haroun.interact(sentence)
  
  # [DEBUG]
  print(answer)
  
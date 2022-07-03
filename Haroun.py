#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#
# Import sys
import sys
# Import asyncio
import asyncio
# Import telethon (for telegram bot message)
from telethon import TelegramClient, events
from telethon.tl.types import PeerChat, PeerChannel
from telethon.errors import SessionPasswordNeededError
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
    
# ! Telegram session manager :

async def startTelegramSession(Haroun):
    
    # Create the client and connect
    #client = TelegramClient(username, api_id, api_hash)
    async with TelegramClient("Haroun", 13960268, "f081cd15e48f08f3743443975326189f") as client :
    
    
        # Start the client with Izno user session.
        #started = await client.start(phone="0768229203")
        
        # Start the client with Haroun bot session.
        started = await client.start(bot_token="1785349151:AAHtHZafv_Hx9cBRk0eO6-RjrRqm06ENjdA")
        
        
        
        # list all sessions
        print(client.session.list_sessions())
        
        # Create new message event listener method.
        @client.on(events.NewMessage(chats=[-1001368892848]))
        async def new_message_handler(event):
            # Get message id.
            message_id = event.message.id
            # Get message datetime.
            message_datetime = event.message.date
            # Get message content.
            message_content = event.message.message
            # Get user id that send message.
            user_id = event.message.from_id.user_id
            print(f" #{message_id} new message from {user_id} at {message_datetime}")
            print(f" {message_content} ")
            
            # Try to call for Haroun answer.
            # Launch Haroun stimulus analisys.
            response = Haroun.call("Haroun Telegram Bot", 0, message_content, None)
            
            # [DEBUG]
            print(response)
            
            # Get chat entity by chat_id.
            entity = await client.get_entity(-1001368892848)
            
            # Send response back.
            await client.send_message(entity=entity, message=response)
            
        
        # Async loop for client.
        await client.run_until_disconnected()
        
        # delete current session (current session is associated with `username` variable)
        #await client.log_out()
        

#####################################################################################################   
#                                            MAIN                                                   #
#####################################################################################################   







# ! Init Haroun :

# Execute if run as script. 
if __name__ == "__main__":

  # Haroun instanciation
  Haroun = Haroun()
  
  # Launch telegram session     
  asyncio.run(startTelegramSession(Haroun))
  
  
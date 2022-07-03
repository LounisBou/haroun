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
# Text encode type
# See https://my.telegram.org/apps
TG_CLIENT_NAME = "Haroun"
TG_CLIENT_API_ID = 13960268
TG_CLIENT_API_HASH = "f081cd15e48f08f3743443975326189f"

# Haroun bot token.
TG_HAROUN_BOT_TOKEN = "1785349151:AAHtHZafv_Hx9cBRk0eO6-RjrRqm06ENjdA"

# Haroun listening chat id.
TG_HAROUN_CHAT_ID = -1001368892848

#
#
class Haroun(object):
  
  """ Haroun home assistant main class. """
  
  def __init__(self):
    
    """ Haroun class constructor """
    
    # Brain instanciation.
    self.brain = Brain()


  async def call(self, source, source_id, sentence, user_id, interaction_id, parent_interaction_id, origin_datetime): 
    
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
      user_id : Int (optionnal)
          Uniq identifier for user who initiate interaction. [Default = null]
      interaction_id : Int (optionnal)
          Uniq identifier for interaction. [Default = null]
      parent_interaction_id : Int (optionnal)
        Uniq identifier for parent interaction if Stimulus is due cause of previous interaction. [Default = None]
      origin_datetime : Datetime (optionnal)
        Datetime origin for stimulus. [Default = null]
      Returns
      _______
      Response : String 
        Interaction response text.
    """
    
    # Generate stimulus from call info.
    stimulus = self.brain.generateStimulus(
      source, 
      source_id, 
      sentence, 
      user_id, 
      interaction_id, 
      parent_interaction_id, 
      origin_datetime
    )
    
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
    
  
  async def startTelegramSession(self, tg_client_name, tg_client_api_id, tg_client_api_hash, tg_haroun_bot_token, tg_chat_id):
      
    """ 
      Start Telegram client session.
    
      Create new message function handler on chat group and call Haroun on every new message.
      
      Parameters
      ----------
      tg_client_name : String
        Telegram client name.
      tg_client_api_id : Int
        API Uniq identifier for client app.
      tg_client_api_hash : String
        API client app hash.
      tg_haroun_bot_token : String
        Uniq token identifier for haroun telegram bot.
      tg_chat_id : Int
        Uniq telegram chat id, where haroun bot will listen for message. Haroun bot should already be a chat member.
      
      -----------
      Return 
    """   
    
    # Create the client and connect
    async with TelegramClient(tg_client_name, tg_client_api_id, tg_client_api_hash) as client :
    
      # Start the client with Izno user session.
      #started = await client.start(phone="0768229203")
      
      # Start the client with Haroun bot session.
      started = await client.start(bot_token=tg_haroun_bot_token)        
      
      # list all sessions
      print(client.session.list_sessions())
      
      # Create new message event listener method.
      @client.on(events.NewMessage(chats=[tg_chat_id]))
      async def new_message_handler(event):
        
        # Get message id.
        message_id = event.message.id
        # Get message datetime.
        message_datetime = event.message.date
        # Get message content.
        message_content = event.message.message
        # Get user id that send message.
        user_id = event.message.from_id.user_id
        # Get current channel id.
        tg_response_chat_id = event.peer_id.channel_id
        
        # [DEBUG]
        print(f"{event.message}")
        print(f" #{message_id} new message from {user_id} at {message_datetime}")
        print(f" {message_content} ")
        
        # Try to call for Haroun answer.
        # Launch Haroun stimulus analisys.
        response = await self.call(
          tg_client_name, 
          tg_chat_id, 
          message_content,
          user_id, 
          message_id, 
          None, 
          message_datetime
        )
        
        # [DEBUG]
        print(response)
        
        # Get chat entity with message channel id.
        chat_entity = await client.get_entity(tg_response_chat_id)
        
        # Send response back.
        await client.send_message(entity=chat_entity, message=response)
      
      # Async loop for client.
      await client.run_until_disconnected()
      
      # delete current session (current session is associated with `username` variable)
      #await client.log_out()
        

#####################################################################################################   
#                                            MAIN                                                   #
#####################################################################################################   

# Execute if run as script. 
if __name__ == "__main__":
  
  # Haroun instanciation
  haroun = Haroun()
  
  # Launch telegram session     
  asyncio.run(
    haroun.startTelegramSession(
      TG_CLIENT_NAME, 
      TG_CLIENT_API_ID, 
      TG_CLIENT_API_HASH, 
      TG_HAROUN_BOT_TOKEN, 
      TG_HAROUN_CHAT_ID
    )
  )
  
  
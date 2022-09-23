#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#
# Import sys
import sys
# Import asyncio
import asyncio
# Import logging library
import logging
# Import pretty errors
#import pretty_errors
# Import sys.path as syspath
from sys import path as syspath
# Import os.path and os.remove
from os import path, remove
# Import configparser.
from configparser import ConfigParser
# Import datetime.date
from datetime import date
# Import telethon (for telegram bot message)
from telethon import TelegramClient, events
from telethon.tl.types import PeerChat, PeerChannel
from telethon.errors import SessionPasswordNeededError
# Core dependencies : 
from core.Brain import Brain
#
#
# Gloabls : 
LOG_LEVELS = {
    'CRITICAL' : logging.CRITICAL,
    'ERROR' : logging.ERROR,
    'WARNING' : logging.WARNING,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG
}
#
# Current, and root paths.
ROOT_PATH = path.dirname(path.abspath(__file__))+'/'
syspath.append(ROOT_PATH)
#
class Haroun(object):
    
    """ Haroun home assistant main class. """
    
    def __init__(self):
        
        """ Haroun class constructor """
        
        # Create configuration dict by loading Haroun configuration file.
        self.config = self.load_config()
        
        # Get current date.
        today_date = date.today()
        
        # Date string.
        today_date_string = today_date.strftime("%d-%m-%Y")
        
        # Logging configuration.
        logging.basicConfig(
            #filename=f'{ROOT_PATH}log/{today_date_string}.log', 
            stream=sys.stdout, 
            encoding=self.config['haroun']['ENCODAGE'], 
        )
        
        # Set logging level.
        logging.getLogger().setLevel(self.config['haroun']['LOG_LEVEL'])
        
        # [DEBUG]
        if(logging.root.level == logging.INFO):
            print(f"\n\n -------------------------------------------------------------------- \n\n")
        
        # [LOG]
        logging.info(f"Haroun is starting...\n\n")
        
        # Brain instanciation.
        self.brain = Brain(self.config)

    def load_config(self):
        
        """ 
            Get config from config/haroun.ini.
            ---
            Return : dict
                Configuration dict.
        """
        
        # Create a config dict.
        config = {}
        
        # Haroun config file path.
        haroun_config_file_path = f"{ROOT_PATH}config/haroun.ini"
        
        # Check if config exist.
        if path.exists(haroun_config_file_path):
        
            # See configparser 
            configParser = ConfigParser()
        
            # Parse haroun.ini config file.
            configParser.read(haroun_config_file_path)
             
            # Get config parser sections.
            sections = configParser.sections()
            
            # Get all sections.
            for section_name in sections:
                config[section_name] = configParser[section_name]
            
        else:
            # [LOG]
            logging.critical(f"Fatal error : config file {haroun_config_file_path} doesn't exist.")
            # Exit program.
            quit()
            
        # Return config dict.
        return config
    
    

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
        stimulus = self.brain.generate_stimulus(
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
            if stimulus.need_interaction() :
                # Haroun create an interaction with user.
                interaction = self.brain.create_interaction(stimulus);
                # If interaction is ready.
                if interaction :
                    # Ask Haroun to manage interaction.
                    interaction = self.brain.manage_interaction(interaction)
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
                
    
    async def start(self):
        
        """
            Start Haroun listening session.
            
            Create a telegram session with asyncio loop to retrieve message.
            
        """
        
        # Retrieving Telegram config from brain config.
        try:
            tg_client_name = self.brain.config['telegram']['client_name']
            tg_client_api_id = int(self.brain.config['telegram']['client_api_id'])
            tg_client_api_hash = self.brain.config['telegram']['client_api_hash']
            tg_haroun_bot_token = self.brain.config['telegram']['haroun_bot_token']
            if self.brain.config['haroun']['debug_mode'] == "True" :
                tg_chat_id = int(self.brain.config['telegram']['haroun_debug_chat_id'])
            else:
                tg_chat_id = int(self.brain.config['telegram']['haroun_chat_id'])
        except:
            print(f"Enable to get Telegram config to initiate Telegram session. Please check your config file.")
        
        # Launch telegram bot listening session.
        await self.start_telegram_session(
            tg_client_name, 
            tg_client_api_id, 
            tg_client_api_hash, 
            tg_haroun_bot_token, 
            tg_chat_id
        )
        
    
    async def start_telegram_session(self, tg_client_name, tg_client_api_id, tg_client_api_hash, tg_haroun_bot_token, tg_chat_id):
            
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
        client = await TelegramClient(None, tg_client_api_id, tg_client_api_hash).start(bot_token=tg_haroun_bot_token)

        # Get Haroun user id.
        haroun_user_id = tg_haroun_bot_token.split(':')[0]
        
        # Use async telegram client.
        async with client :
        
            # Start the client with Izno user session.
            #started = await client.start(phone="0768229203")
            
            # Start the client with Haroun bot session.
            #started = await client.start(bot_token=tg_haroun_bot_token)        
            
            # list all sessions
            #print(client.session.list_sessions())
            
            # Create new message event listener method.
            @client.on(events.NewMessage(chats=[tg_chat_id]))
            async def new_message_handler(event):

                # Audio flag.
                audio = False

                # [LOG]
                logging.debug(f"New message : {event.message.__dict__}")

                # If message contains media file.
                if event.message.media_unread :
                    
                    # [LOG]
                    logging.debug(f"New message media document : {event.message.media.document.__dict__}")
                    
                    # If message contains audio file.
                    if event.message.media.document.mime_type == 'audio/ogg' :

                        # Test retrieving audio file from message.
                        audio_path = await client.download_media(event.message.media, f"{ROOT_PATH}tmp/tg-audio-{event.message.media.document.id}.ogg")

                        # [LOG]
                        logging.info(f"Audio file retrieved : {audio_path}")

                        # Use brain ear to transcribe audio file.
                        audio_message = self.brain.ear.transcribe(audio_path)

                        # [LOG]
                        logging.info(f"Audio file transcribed : {audio_message}")

                    else:
                        # [LOG]
                        logging.info(f"Unsupported media type : {event.message.media.document.mime_type}")
                    
                # Get message id.
                message_id = event.message.id
                # Get message datetime.
                message_datetime = event.message.date
                # Get message content.
                message_content = event.message.message
                # If no content message but audio message.
                if not message_content and audio_message :
                    # Get audio message as message_content.
                    message_content = audio_message
                    # Audio flag.
                    audio = True
                # If message from chat.
                if event.message.from_id :
                    user_id = event.message.from_id.user_id
                    # Get current channel id.
                    #tg_response_chat_id = event.peer_id.channel_id
                    tg_response_chat_id = event.peer_id.chat_id
                else:
                    # Get user id that send message.
                    user_id = tg_chat_id
                    # Get current channel id.
                    tg_response_chat_id = tg_chat_id
                
                # If message is not empty.
                if message_content.strip() :

                    # Ignore message if it's from Haroun.
                    if str(user_id).strip() != haroun_user_id.strip() :

                        # [LOG]
                        logging.info('\n\n----------------------------------------')
                        logging.info(f"Incoming message : \n #{message_id} new message from {user_id} at {message_datetime}")
                        logging.info(f"Message : {message_content}\n\n")

                        # Audio debug mode.
                        if self.brain.config['haroun']['audio_debug'] == 'True' :
                            
                            # Set audio message as response.
                            response = message_content

                        else:

                            # Call for Haroun.
                            response = await self.call(
                                tg_client_name, 
                                tg_chat_id, 
                                message_content,
                                user_id, 
                                message_id, 
                                None, 
                                message_datetime
                            )
                            
                            # [LOG]
                            logging.info(f"Response : {response} \n\n")

                        # Get chat entity with message channel id.
                        chat_entity = await client.get_entity(tg_response_chat_id)

                        # If message is from audio source.
                        if audio and self.brain.config['haroun']['audio_response'] == 'True' :
                            # Create audio response.
                            reponse_file_path = self.brain.mouth.generateAudio(response)
                            # Send audio response.
                            await client.send_file(chat_entity, reponse_file_path, voice_note=True)
                            # Send text response.
                            #await client.send_message(entity=chat_entity, message=response)
                            # Delete response file.
                            remove(reponse_file_path)
                        else:
                            # Send text response.
                            await client.send_message(entity=chat_entity, message=response)
            
            # [LOG]
            logging.info('\n\n')
            logging.info(f"Haroun is listening...\n\n")
                        
            # Async loop for client.
            await client.run_until_disconnected()
            
            # [LOG]
            logging.error(f"Haroun telegram bot have been disconnected.\n")
            
            # Delete client bot current session.
            #await client.log_out()
                

#####################################################################################################   
#                                            MAIN                                                   #
#####################################################################################################   

# Execute if run as script. 
if __name__ == "__main__":
    
    # Haroun instanciation
    haroun = Haroun()
    
    # Launch telegram session     
    asyncio.run(haroun.start())
    
    
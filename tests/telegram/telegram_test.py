#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#
# ! Imports : 
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import PeerChat, PeerChannel
from telethon.errors import SessionPasswordNeededError

def telegramClientStart():

    # Create the client and connect
    #client = TelegramClient(username, api_id, api_hash)
    with TelegramClient("Haroun", 13960268, "f081cd15e48f08f3743443975326189f") as client :
        
        # Start the client with Haroun bot session.
        started = client.start(bot_token="1785349151:AAHtHZafv_Hx9cBRk0eO6-RjrRqm06ENjdA")
                
        # list all sessions
        print(client.session.list_sessions())
        
        # Create new message event listener method.
        @client.on(events.NewMessage(chats=[-1001368892848]))
        def new_message_handler(event):
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
        
        # Async loop for client.
        asyncio.run(client.run_until_disconnected())
        
        # delete current session (current session is associated with `username` variable)
        #await client.log_out()
        

        
telegramClientStart()

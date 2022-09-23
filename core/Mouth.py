#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#
# Libraries dependancies :
#
# Import subprocess library.
import subprocess
# Import sys.path as syspath
from sys import path as syspath
# Import os.path and os.walk
from os import path
# Import pyttsx3 library.
import pyttsx3
# Import logging library
import logging
# Import time library.
from time import time
#
# Gloabls : 
#
# Current, and root paths.
CURRENT_PATH = path.dirname(path.abspath(__file__))+'/'
ROOT_PATH = path.dirname(path.abspath(CURRENT_PATH))+'/'
syspath.append(ROOT_PATH)
#
#
class Mouth(object):  

    """ Mouth class for Haroun. """

    def __init__(self):

        """ 
            __init__ : Mouth class constructor.
        """

        # Define pyttsx3 engine.
        self.engine = pyttsx3.init()

        # Define pyttsx3 voice.
        self.engine.setProperty('voice', 'french')

    def generateAudio(self, text):

        """
            Use pyttsx3 TTS API to create audio speak file from text.
            ---
            Parameters
                text : String
                    Text to speak.
            --- 
            Return String
                Transcribed text audio file path.
        """

        # Define pyttsx3 rate.
        self.engine.setProperty('rate', 150)
        
        # Define audio file path.
        audio_mp3_file_path = ROOT_PATH+'tmp/response'+str(time())+'.mp3'
        
        # Save voice generated as audio file (mp3 or wav).
        self.engine.save_to_file(text, audio_mp3_file_path)

        # Run and wait commands.
        self.engine.runAndWait()

        # Convert audio file to ogg format.
        audio_ogg_file_path = audio_mp3_file_path.replace('.mp3', '.ogg')
        with subprocess.Popen(
            ["ffmpeg", "-loglevel", "quiet", "-i", audio_mp3_file_path, "-acodec", "libvorbis", "-q:a", "4", audio_ogg_file_path],
            stdout=subprocess.PIPE
        ) as process:
            for line in process.stdout:
                logging.info(line)  

        # Delete mp3 audio file.
        subprocess.Popen(
            ["rm", audio_mp3_file_path],
            stdout=subprocess.PIPE
        )

        # Return audio ogg file path.
        return audio_ogg_file_path
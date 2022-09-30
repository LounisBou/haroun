#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#
# Import subprocess library.
import subprocess
# Import json library.
import json
# Import vosk library.
from vosk import Model, KaldiRecognizer, SetLogLevel
# Import logging library
import logging
#
#
# Define sample rate.
SAMPLE_RATE = 16000
#
class Ear(object):  
  
    """ Ear class for Haroun. """

    def __init__(self):

        """ 
            __init__ : Ear class constructor.
        """

        # You can set log level to -1 to disable debug messages
        SetLogLevel(0)

        # Define language model to use.
        #model = Model(lang="fr")

        # You can also init model by name or with a folder path
        self.model = Model(model_name="vosk-model-fr-0.6-linto-2.2.0")

        # Define Kaldi recognizer.
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)

    def transcribe(self, audio_file_path, delete_audio_file = True):

        """
            Use Vosk STT API to transcribe audio file into text.
            ---
            Parameters
                audio_file_path : String
                    Audio file path.
                delete_audio_file : Boolean
                    Delete audio file after transcription. [Default = True]
            --- 
            Return String
                Transcribed text.
        """

        # Define ffmpeg process to convert audio file into wav format.
        with subprocess.Popen(
            ["ffmpeg", "-loglevel", "quiet", "-i", audio_file_path, "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
            stdout=subprocess.PIPE
        ) as process:

            # Listenning loop.
            while True:

                # Read data.
                data = process.stdout.read(4000)

                # If data is empty.
                if len(data) == 0:
                    # Break listenning loop.
                    break

                # If data is valid.
                if self.recognizer.AcceptWaveform(data):
                    # [LOG]
                    logging.debug(self.recognizer.Result())
                else:
                    # [LOG]
                    logging.debug(self.recognizer.PartialResult())

            # Get final result.
            result = json.loads(self.recognizer.FinalResult())

            # If delete audio file is True.
            if delete_audio_file :
                # Delete audio file.
                subprocess.run(["rm", audio_file_path])

            # Return final result text.
            return result["text"]

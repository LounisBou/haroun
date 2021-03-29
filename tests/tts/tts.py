#!/usr/bin/env python3

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Text-To-Speech API sample application .
Example usage:
    python tts.py
"""

# Import sys library for args.
import sys

# playsound module is a cross platform module that can play audio files
from playsound import playsound

# tts
def tts(text):
  # [START tts_quickstart]
  """Synthesizes speech from the input string of text or ssml.
  Note: ssml must be well-formed according to:
      https://www.w3.org/TR/speech-synthesis/
  """
  from google.cloud import texttospeech

  # Instantiates a client
  client = texttospeech.TextToSpeechClient()

  # Set the text input to be synthesized
  synthesis_input = texttospeech.SynthesisInput(text=text)

  # Build the voice request, select the language code ("fr-FR") and the ssml
  # voice gender ("neutral")
  voice = texttospeech.VoiceSelectionParams(
    language_code="fr-FR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
  )

  # Select the type of audio file you want returned
  audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
  )

  # Perform the text-to-speech request on the text input with the selected
  # voice parameters and audio file type
  response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
  )

  # The response's audio_content is binary.
  with open("/tmp/tts.mp3", "wb") as out:
  
    # Write the response to the output file.
    out.write(response.audio_content)
    
    #print('Audio content written to file "tts.mp3"')
    
  # Play mp3 generated response's audio file.
  playsound('/tmp/tts.mp3')

# ???
if __name__ == "__main__":

  # Retrieve argument 1 as text to transform
  text = sys.argv[1]
  
  # DEBUG
  #print(text)
  
  #print 'Number of arguments:', len(sys.argv), 'arguments.'
  #print 'Argument List:', str(sys.argv)
  
  # Call tts conversion method.
  tts(text)


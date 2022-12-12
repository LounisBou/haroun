#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Libraries dependancies : #
#
# Import core concept domain.
from core.concepts.Domain import Domain 
# Import openAI API.
import openai
#
#
# Domain globals : 
#
# Needed slots list.
SLOTS_FILES = []
# TEST OPENAI API
TEST_API = False
# DEBUG MODE
DEBUG = False

# Default openAI parameters
DEFAULT_MODEL = "text-davinci-003"
DEFAULT_TEMPERATURE = 0.5
DEFAULT_MAX_TOKEN = 4096
DEFAULT_STOP = ["\n", "  ", " "]

# Defaut chat parameters
DEFAULT_USERNAME = "Izno"
DEFAULT_BOTNAME = "Haroun"
QUIT_KEYWORDS = ["quit", "exit", "bye", "au revoir", "aurevoir", "ciao", "stop", "end"]
#
# ! DOMAIN 
#
class Openia(Domain):
    
    def __init__(self):
        
        """ Class constructor. """
                
        # Init parent class Domain.
        super().__init__()
        
        # Load openAI API key
        openai.api_key = self.config['openai']['api_key']

        # Create completion engine.
        self.engine = openai.Completion

    def test(self, prompt = "Dit ceci est un test"):

        """ 
            Test the openAI API completion engine
            ---
            Parameters:
                prompt: str
                    The prompt to complete
            ---
            Returns: str
                The completion
        """

        # Ask for the completion
        response = self.engine.create(
            model=DEFAULT_MODEL, 
            prompt=prompt, 
            temperature=DEFAULT_TEMPERATURE, 
            max_tokens=DEFAULT_MAX_TOKEN - len(prompt)
        )

        # If debug mode
        if DEBUG:
            # Print the response
            print(f"response : {response}")
            print(f"completion : {response['choices'][0]['text'].strip()}")

        # Return the completion
        return response["choices"][0]["text"].strip()


    @staticmethod
    def complete(self, prompt, temperature=DEFAULT_TEMPERATURE, max_tokens=DEFAULT_MAX_TOKEN, stop=DEFAULT_STOP):

        """ 
            Complete the prompt with openAI API 
            ---
            Parameters:
                prompt: str
                    The prompt to complete
                temperature: float
                    The temperature of the model
                max_tokens: int
                    The maximum number of tokens to generate
                stop: list
                    The list of tokens to stop the completion
            ---
            Returns: str
                The completion
        """

        # If arguments are None
        if temperature is None:
            # Set the default temperature
            temperature = DEFAULT_TEMPERATURE
        if max_tokens is None:
            # Set the default max token
            max_tokens = DEFAULT_MAX_TOKEN
        if stop is None:
            # Set the default stop
            stop = DEFAULT_STOP

        # Max token must take prompt length into account
        if max_tokens + len(prompt) >= DEFAULT_MAX_TOKEN:
            # Remove the prompt length from the max token
            max_tokens = DEFAULT_MAX_TOKEN - len(prompt)

        # If debug mode
        if DEBUG:
            # Print the arguments
            print(f"Prompt : {prompt}")
            print(f"Temperature : {temperature}")
            print(f"Max token : {max_tokens}")
            print(f"Stop : {stop}")

        # Create the request
        request = self.engine.create(
            model=DEFAULT_MODEL, 
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # If debug mode
        if DEBUG:
            # Print the request
            print(f"Request : {request}")
            # Print the completion
            print(f"Completion : {request['choices'][0]['text'].strip()}")

        # Return the completion
        return request["choices"][0]["text"].strip()

    @staticmethod
    def chat(self, sentence, username="Humain", botname="IA", temperature=None, max_tokens=None, stop=None):

        """ 
            Get chat response to a sentence using openIA completion engine
            ---
            Parameters:
                sentence: str
                    The sentence to complete
                username: str
                    The name of the user
                botname: str
                    The name of the bot
                temperature: float
                    The temperature of the model
                max_tokens: int
                    The maximum number of tokens to generate
                stop: list
                    The list of tokens to stop the completion
            ---
            Returns: str
                The chat response
        """

        # Ask for the completion
        response = self.complete(
            prompt=f"{username} : {sentence}\n{botname} : ", 
            temperature=temperature, 
            max_tokens=max_tokens,
            stop=stop
        )

        # Return the completion as response
        return response
    

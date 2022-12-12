#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

""" Importing libraries """
import openai
import sys
import os

""" Constants """

# Default openAI parameters
DEFAULT_MODEL = "text-davinci-003"
DEFAULT_TEMPERATURE = 0.5
DEFAULT_MAX_TOKEN = 4096
DEFAULT_STOP = ["\n", "  ", " "]

# Defaut chat parameters
DEFAULT_USERNAME = "Izno"
DEFAULT_BOTNAME = "Haroun"
QUIT_KEYWORDS = ["quit", "exit", "bye", "au revoir", "aurevoir", "ciao", "stop", "end"]


""" Class """
class OpenAI:

    def __init__(self, api_key, debug = False):
        
        """ 
            Class constructor 
            ---
            Parameters:
                api_key: str
                    The openAI API key
                debug: bool
                    The debug mode
        """
    
        # Load openAI API key
        openai.api_key = api_key

        # Set debug mode
        self.debug = debug

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
        response = openai.Completion.create(
            model=DEFAULT_MODEL, 
            prompt=prompt, 
            temperature=DEFAULT_TEMPERATURE, 
            max_tokens=DEFAULT_MAX_TOKEN - len(prompt)
        )

        # If debug mode
        if self.debug:
            # Print the response
            print(f"response : {response}")
            print(f"completion : {response['choices'][0]['text'].strip()}")

        # Return the completion
        return response["choices"][0]["text"].strip()


    
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
        if self.debug:
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
        if self.debug:
            # Print the request
            print(f"Request : {request}")
            # Print the completion
            print(f"Completion : {request['choices'][0]['text'].strip()}")

        # Return the completion
        return request["choices"][0]["text"].strip()

    
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

""" Main """
if __name__ == "__main__":

    # Get -a or --api argument
    if "-a" in sys.argv or "--api" in sys.argv:
        # Get the API key
        api_key = sys.argv[sys.argv.index("-a") + 1]
    else:
        # Load the openAI API key
        api_key = os.environ.get("OPENAI_API_KEY")

    # Get -d or --debug argument
    if "-d" in sys.argv or "--debug" in sys.argv:
        # Set debug mode
        debug = True

    # Get -t or --test argument
    if "-t" in sys.argv or "--test" in sys.argv:
        # Set test mode
        test_api = True

    # Create openIA instance
    openAI = OpenAI(api_key, debug)

    # If test mode
    if test_api:
        # Test the openAI API
        reponse = openAI.test("Humain : Bonjour\nIA : ")
        # Print the response
        print(f"A.I. : {reponse}")
        exit()
    
    # Loop while the user doesn't want to quit.
    while True:

        # Ask for the sentence.
        sentence = input(f"{DEFAULT_USERNAME} : ")

        # openIA chat completion.
        response = openAI.chat(sentence, DEFAULT_USERNAME, DEFAULT_BOTNAME)

        # Print the response
        print(f"{DEFAULT_BOTNAME} : {response}")

        # If user sentence contains a quit keyword
        if any([keyword.lower() in sentence.lower() for keyword in QUIT_KEYWORDS]):
            break
    
    # Exit
    exit()



    
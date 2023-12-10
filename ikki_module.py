import os
import numpy as np
#import urllib.request as ur
#import ipywidgets as widgets
import openai
from IPython.display import IFrame, HTML
from dotenv import load_dotenv


class ChatGPT:
    '''A class to interact with OpenAI ChatGPT model '''

    def __init__(self):
        # Load the environmental variables from the .env file
        load_dotenv()

        # Retrieve the OPENAI_API_KEY environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")

        # Set the retrieved API key for the OpenAI library
        openai.api_key = self.api_key

        # Describe the behavior of the chatbot
        self.MAIN_ROLE = 'system'
        self.SECONDARY = 'user'

        # Total cost
        self.total_cost = 0

    def chatgpt_resumes(self,data,message):

        # Create a chat completion with the provided message and role
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": self.MAIN_ROLE, "content": message},
                {"role": self.SECONDARY, "content": data},
            ], temperature=0.1 )
        
        return response.model_dump()['choices'][0]['message']['content'], response
    
    def get_file_list():
        file_list=os.listdir()
        return file_list
    
    def chatgpt_textTo_audio(self,data):
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=data )
        return response

    
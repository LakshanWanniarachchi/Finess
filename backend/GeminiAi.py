import os
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
import json
# Load environment variables from .env file
load_dotenv()


class GeminiAi:

    def __init__(self):

        # Configure generative AI API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

    def text_gemini_text_generator(self, bmi, Calories , age , gender):
        # Call the Gemini AI API to generate content
        try:
             
             
             

                             
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"I want to get a meal plan , I am {gender} , my age is {age},My age is  my BMI is {bmi} , my calorie burn is like this {Calories}, I want Example meal plane only for 1 day")
           

            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return None

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.api_key = os.getenv("GENAI_API_KEY")

def generate_response(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content(prompt)
    return response.text
   
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Directory containing the PDFs
PDF_MINUTES = '/Users/arturoavalos/Documents/FED_chat/pdfs'
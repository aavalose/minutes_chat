import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI()

# Directory containing the PDFs
PDF_MINUTES = '/Users/arturoavalos/Documents/FED_chat/pdfs'
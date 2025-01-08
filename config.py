import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is loaded
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

# Define client as the OpenAI client
client = openai

# Directory containing the PDFs
PDF_MINUTES = '/Users/arturoavalos/Documents/FED_chat/pdfs'
import os
import base64
import PyPDF2
import streamlit as st
from config import PDF_MINUTES
from datetime import datetime

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_pdf_files():
    """Get a list of PDF files from the minutes directory."""
    if not os.path.exists(PDF_MINUTES):
        return []
    files = [f for f in os.listdir(PDF_MINUTES) if f.endswith('.pdf')]
    return sorted(files, reverse=True)  # Most recent first

def get_formatted_name(filename):
    # Convert 'minutes_YYYY-MM-DD.pdf' to a more readable format
    date_str = filename.replace('minutes_', '').replace('.pdf', '')
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return f"Minutes for {date_obj.strftime('%B %d, %Y')}"
    except ValueError:
        return filename

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def display_pdf(pdf_path):
    # Adjust the size to prevent overlap
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
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
    # Readthe PDF file
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # HTML template to render PDF using pdf.js
    pdf_display = f"""
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
    </head>
    <body>
        <canvas id="pdf-canvas" width="600" height="800"></canvas>
        <script>
            var pdfData = atob("{base64_pdf}");
            var loadingTask = pdfjsLib.getDocument({{data: pdfData}});
            loadingTask.promise.then(function(pdf) {{
                pdf.getPage(1).then(function(page) {{
                    var scale = 1.5;
                    var viewport = page.getViewport({{scale: scale}});
                    var canvas = document.getElementById('pdf-canvas');
                    var context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    var renderContext = {{
                        canvasContext: context,
                        viewport: viewport
                    }};
                    page.render(renderContext);
                }});
            }});
        </script>
    </body>
    </html>
    """

    # Display the PDF using Streamlit's HTML component
    st.components.v1.html(pdf_display, height=800, width=600)
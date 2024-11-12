import streamlit as st
import PyPDF2
import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

client = OpenAI()

# Directory containing the PDFs
pdf_minutes = '/Users/arturoavalos/Documents/FED_chat/pdfs'

# List all PDF files in the specified directory
def get_pdf_files():
    return [f for f in os.listdir(pdf_minutes) if f.endswith('.pdf')]

# Extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to chunk the extracted text into smaller parts
def chunk_text(text, chunk_size=2000):  # Increased chunk size
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_size += len(word) + 1  # +1 for space
        if current_size > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_size = len(word)
        else:
            current_chunk.append(word)
            
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

# Function to calculate cosine similarity
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

# Function to search for relevant chunks using semantic similarity
def search_relevant_chunks(chunks, query):
    # Get embeddings for query
    query_response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = query_response.data[0].embedding
    
    # Calculate similarities and store them with chunks
    chunk_similarities = []
    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        similarity = cosine_similarity(query_embedding, response.data[0].embedding)
        chunk_similarities.append((chunk, similarity))
    
    # Sort by similarity and return top chunks
    chunk_similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 5 chunks with similarity above 0.5
    relevant_chunks = [chunk for chunk, similarity in chunk_similarities if similarity > 0.5]
    return relevant_chunks[:5]  # Increased from 3 to 5 chunks and lowered threshold from 0.7 to 0.5

# OpenAI API function to generate a response based on the retrieved chunks
def ask_openai(query, chunks):
    combined_text = "\n\n".join(chunks)
    prompt = f"""Based on the following excerpts from FOMC minutes:

{combined_text}

Please provide a detailed and accurate answer to this question:
{query}

If the provided excerpts don't contain enough information to fully answer the question, please state that explicitly."""
    
    response = client.chat.completions.create(
        model="gpt-4",  # Using GPT-4 for better comprehension
        messages=[
            {"role": "system", "content": "You are an expert in monetary policy and Federal Reserve operations. Provide accurate, nuanced answers based only on the provided FOMC minutes excerpts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3  # Lower temperature for more focused responses
    )
    return response.choices[0].message.content.strip()

# Streamlit app layout
st.title("FOMC Minutes Analysis Assistant")
st.markdown("""
This tool helps you analyze Federal Open Market Committee (FOMC) meeting minutes.
Select a document and ask questions about monetary policy decisions, economic discussions, and more.
""")

# Option for the user to select a PDF
pdf_files = get_pdf_files()
pdf_selection = st.selectbox("Select FOMC Minutes:", pdf_files)

# Button to extract and display PDF content
if pdf_selection:
    pdf_path = os.path.join(pdf_minutes, pdf_selection)
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Show a preview of the first 500 characters of the PDF
    st.write(f"**Preview of {pdf_selection}:**")
    st.text_area("Extracted Text:", pdf_text[:500], height=200)
    
    # Ask a question about the PDF or request a summary
    user_input = st.text_input("What would you like to know about these minutes?")

    if st.button("Analyze"):
        if user_input:
            with st.spinner('Analyzing the document...'):
                # Chunk the text and search for relevant chunks
                chunks = chunk_text(pdf_text)
                relevant_chunks = search_relevant_chunks(chunks, user_input)

                if relevant_chunks:
                    # Generate a response using the relevant chunks
                    ai_reply = ask_openai(user_input, relevant_chunks)
                    st.write("**Analysis:**")
                    st.markdown(ai_reply)
                else:
                    st.warning("No relevant information found in the document. Please try rephrasing your question.")

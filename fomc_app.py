import streamlit as st
import PyPDF2
import os
import openai
import numpy as np

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

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

# Chunk text into overlapping parts for better context continuity
def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # Overlap for context
    return chunks

# Function to get embeddings for text
def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']

# Calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Get the most relevant chunks using embeddings
def search_relevant_chunks_with_embeddings(chunks, query, num_chunks=3):
    query_embedding = get_embedding(query)
    chunk_embeddings = [get_embedding(chunk) for chunk in chunks]
    
    similarities = [cosine_similarity(query_embedding, chunk_embedding) for chunk_embedding in chunk_embeddings]
    
    most_relevant_chunks = np.argsort(similarities)[-num_chunks:][::-1]
    return [chunks[i] for i in most_relevant_chunks]

# OpenAI API function to generate a response based on the retrieved chunks
def ask_openai(query, chunks):
    combined_text = "\n\n".join(chunks)
    prompt = f"Based on the following text from the document:\n\n{combined_text}\n\nAnswer the following question:\n\n{query}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Streamlit app layout
st.title("RAG-Enhanced Chatbox with PDF Reading and OpenAI")

# Option for the user to select a PDF
pdf_files = get_pdf_files()
pdf_selection = st.selectbox("Select a PDF to read:", pdf_files)

# Button to extract and display PDF content
if pdf_selection:
    pdf_path = os.path.join(pdf_minutes, pdf_selection)
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Show a preview of the first 500 characters of the PDF
    st.write(f"**Preview of {pdf_selection}:**")
    st.text_area("Extracted Text:", pdf_text[:500], height=200)
    
    # Ask a question about the PDF or request a summary
    user_input = st.text_input("Ask a question about the PDF or request a summary:")

    if st.button("Send"):
        if user_input:
            # Chunk the text and search for relevant chunks using embeddings
            chunks = chunk_text(pdf_text)
            relevant_chunks = search_relevant_chunks_with_embeddings(chunks, user_input)

            if relevant_chunks:
                # Generate a response using the relevant chunks
                ai_reply = ask_openai(user_input, relevant_chunks)
                st.write("**AI Response:**")
                st.write(ai_reply)
            else:
                st.write("No relevant information found in the document.")

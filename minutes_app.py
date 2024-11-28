import os
import streamlit as st
from scrapping_minutes import check_and_download_new_minutes  # Make sure the import path is correct
from src.pdf_utils import get_pdf_files, extract_text_from_pdf, display_pdf
from src.text_processing import chunk_text
from src.similarity import search_relevant_chunks
from src.openai_utils import ask_openai
from config import PDF_MINUTES  # Make sure this import is present too

st.title("FOMC Minutes Analysis Assistant")
st.markdown("""
This tool helps you analyze Federal Open Market Committee (FOMC) meeting minutes.
Select one or two documents and ask questions about monetary policy decisions, economic discussions, and more.
""")

# Check for new minutes at startup
with st.spinner('Checking for new FOMC minutes...'):
    new_files = check_and_download_new_minutes()
    if new_files:
        st.success("New FOMC minutes have been downloaded!")
        # Force refresh of pdf_files
        st.cache_data.clear()

# Get the list of PDF files AFTER potentially downloading new ones
pdf_files = get_pdf_files()

analysis_mode = st.radio("Select Analysis Mode:", ["Single Document", "Compare Documents"])

if analysis_mode == "Single Document":
    # Single document analysis UI and logic
    pdf_selection = st.selectbox("Select FOMC Minutes:", pdf_files)
    
    if pdf_selection:
        pdf_path = os.path.join(PDF_MINUTES, pdf_selection)
        pdf_text = extract_text_from_pdf(pdf_path)
        
        st.write("**PDF Document:**")
        display_pdf(pdf_path)
        
        user_input = st.text_input("What would you like to know about these minutes?")

        if st.button("Analyze"):
            if user_input:
                with st.spinner('Analyzing the document...'):
                    chunks = chunk_text(pdf_text)
                    relevant_chunks = search_relevant_chunks(chunks, user_input)

                    if relevant_chunks:
                        ai_reply = ask_openai(user_input, relevant_chunks)
                        st.write("**Analysis:**")
                        st.markdown(ai_reply)
                    else:
                        st.warning("No relevant information found in the document. Please try rephrasing your question.")

else:  # Compare Documents mode
    # Add vertical spacing between elements
    st.write("### Compare Two FOMC Minutes")
    st.write("---")  # Add a horizontal line for separation
    
    col1, col2 = st.columns(2, gap="large")  # Add gap between columns
    
    with col1:
        st.write("#### First Document")
        pdf_selection1 = st.selectbox("Select First FOMC Minutes:", pdf_files)
        if pdf_selection1:
            pdf_path1 = os.path.join(PDF_MINUTES, pdf_selection1)
            display_pdf(pdf_path1)
            
    with col2:
        st.write("#### Second Document")
        remaining_files = [f for f in pdf_files if f != pdf_selection1]
        pdf_selection2 = st.selectbox("Select Second FOMC Minutes:", remaining_files)
        if pdf_selection2:
            pdf_path2 = os.path.join(PDF_MINUTES, pdf_selection2)
            display_pdf(pdf_path2)
    
    # Add spacing before the input section
    st.write("---")
    
    if pdf_selection1 and pdf_selection2:
        user_input = st.text_input("What aspects would you like to compare between these minutes?")
        
        if st.button("Compare"):
            if user_input:
                with st.spinner('Analyzing both documents...'):
                    text1 = extract_text_from_pdf(pdf_path1)
                    text2 = extract_text_from_pdf(pdf_path2)
                    
                    chunks1 = chunk_text(text1)
                    chunks2 = chunk_text(text2)
                    relevant_chunks1 = search_relevant_chunks(chunks1, user_input)
                    relevant_chunks2 = search_relevant_chunks(chunks2, user_input)
                    
                    combined_chunks = []
                    for i, (chunk1, chunk2) in enumerate(zip(relevant_chunks1[:2], relevant_chunks2[:2])):
                        combined_chunks.extend([
                            f"Document 1 ({pdf_selection1}) - Excerpt {i+1}:",
                            chunk1,
                            f"\nDocument 2 ({pdf_selection2}) - Excerpt {i+1}:",
                            chunk2
                        ])
                    
                    if combined_chunks:
                        ai_reply = ask_openai(user_input, combined_chunks, compare_mode=True)
                        st.write("**Comparative Analysis:**")
                        st.markdown(ai_reply)
                    else:
                        st.warning("No relevant information found in the documents. Please try rephrasing your question.")
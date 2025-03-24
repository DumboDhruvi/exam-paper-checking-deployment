import streamlit as st
from main import *
from pdf_to_answer_dict import *

st.title("PDF to Text using OCR")

pdf_file = st.file_uploader("Upload a PDF", type="pdf")
ans_key_file = st.file_uploader("Upload a json", type="json")

if pdf_file is not None:
    api_key = "K85286034988957"  # Replace with actual API key
    marks = main_st(pdf_file, ans_key_file, api_key)
    st.text_area("Extracted Text", text, height=300)
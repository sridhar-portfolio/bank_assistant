import os
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from assistant import rag_function

# Streamlit automatically loads secrets into st.secrets or os.environ
api_key = st.secrets["OPENAI_API_KEY"]

# Get the directory where app.py is currently located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the safe path to your vector folder
vector_folder_path = os.path.join(current_dir, "vector_store")

st.title("🦜🔗 Quickstart App")

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "Wie hoch ist die Entgelte für Zahlungsverkehrsdienstleistungen für Bargeldeinzahlungen an eigene Kunden am Schalter?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        retrieved_context, response = rag_function(text, vector_folder_path, "giroplus_index", api_key)
        st.info(response)
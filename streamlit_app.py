import os
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from assistant import rag_function

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="YourFinBank Assistant",
    page_icon="🏦",
    layout="centered"
)

# Custom CSS Injection
st.markdown("""
<style>
    /* Hide default Streamlit footer and hamburger menu for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Style chat message containers */
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Custom header styling */
    .bank-header {
        background-color: #0F2942;
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Example usage of the header banner
st.markdown("""
<div class="bank-header">
    <h2>YourFinBank Virtual Assistant</h2>
    <p>Secure, 24/7 Support for Savings, Credit Cards, and Loans</p>
</div>
""", unsafe_allow_html=True)

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
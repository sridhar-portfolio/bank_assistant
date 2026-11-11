import os
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from assistant import rag_function

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="YourFinBank Assistant",
    page_icon="assets/icons8-chatbot-40.png",
    layout="centered"
)

##################### CSS #########################

# Custom CSS Injection
st.markdown("""
<style>
    /* Hide default Streamlit footer and hamburger menu for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Reduce the default top padding of the main container */
    .block-container {
        padding-top: 0rem;  /* Change to 1rem or 0rem to pull content even higher */
        padding-bottom: 0rem;
    }

    /* Main App Background & Theme */
    .stApp {
        background-color: #020617; /* slate-950 */
        color: #f8fafc;            /* slate-50 */
    }

    /* Style the Chat Container Card */
    .chat-card {
        background-color: #0f172a; /* slate-900 */
        border: 1px solid #334155; /* slate-700 */
        border-radius: 1rem;
        padding: 20px;
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.5);
    }

    /* Style Chat Input to match dark mode */
    .stChatInputContainer input {
        background-color: #FFFFFF !important;
        color: #494848 !important;
        border: 1px solid #334155 !important;
        border-radius: 0.75rem !important;
    }

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

    /* Style for main assistant title/header */
    .assistant-title {
        font-size: 32px !important;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0px;
    }
    
    /* Style for 'Vorgeschlagene Fragen' section header */
    .section-header {
        font-size: 18px !important;
        font-weight: 600;
        color: #475569; /* Muted gray */
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Style Prompt Chips */
    .stButton > button {
        background-color: #D4D4D4 !important;
        color: #494848 !important;
        border: 1px solid #334155 !important;
        border-radius: 0.75rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-size: 12px !important;
    }
    .stButton > button:hover {
        background-color: #909090 !important;
        color: #ffffff !important;
        border-color: #909090 !important;
    }
</style>
""", unsafe_allow_html=True
)

##########################################################################

# Streamlit automatically loads secrets into st.secrets or os.environ
api_key = st.secrets["OPENAI_API_KEY"]

# Get the directory where app.py is currently located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the safe path to your vector folder
vector_folder_path = os.path.join(current_dir, "vector_store")

# =========================================================
# 1. HEADER SECTION (Place titles & captions here!)
# =========================================================

#st.markdown(
#    """
#    <p style="font-size: 15px; color: #475569; font-family: sans-serif; margin-top: 0px; line-height: 1.4;">
#        Fragen Sie mich alles zu den Produkten von YourFinBank, z. B. Girokonto, Sparkonto, Privatkredit oder Kreditkarte.
#    </p>
#    """,
#    unsafe_allow_html=True,
#)

# =========================================================
# 2. SESSION STATE & HISTORY
# =========================================================

# 1. Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Hallo! Ich bin Ihr KI-Banking-Assistent, der auf einer maßgeschneiderten RAG-Pipeline basiert. Fragen Sie mich alles zu Girokonten, Sparkonten, Kreditkarten, Privatkrediten und mehr."
    }]

# =========================================================
# 3. PINNED CHIPS AT THE TOP
# =========================================================

st.markdown(
    """
    <h1 style="font-size: 12px; font-weight: 500; color: #909090; font-family: sans-serif; margin-bottom: 2px;">
        💡 Vorgeschlagene Fragen
    </h1>
    """,
    unsafe_allow_html=True,
)

# Define your quick prompts
chips = [
    "Wie hoch ist die monatliche Kontoführungsgebühr?",
    "Wie hoch sind die Gebühren für Echtzeit-Überweisungsaufträge?"    
]

user_query = None

# Check if a chip button was clicked
for i, chip in enumerate(chips):
    if st.button(chip, use_container_width=True, key=f"chip_{i}"):
        user_query = chip

st.divider() # Adds a clean separation line below the chips

# =========================================================
# 4. CAPTURE CHAT INPUT (Floats at the bottom automatically)
# =========================================================
# Handle Chat Input (Standard Streamlit chat bar)
chat_input = st.chat_input("Geben Sie hier Ihre Frage ein ...")

# If the user typed something OR clicked a chip, process it
if chat_input:
    user_query = chat_input

# =========================================================
# 5. PROCESS INPUT & GENERATE RESPONSE
# =========================================================

if user_query:
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate assistant response (Replace this with your actual RAG backend call)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Dummy response for demonstration
        retrieved_metadata, bot_response = rag_function(user_query, vector_folder_path, "giroplus_index", api_key)
        
        response_placeholder.markdown(bot_response)

        retrieved_sources = [
            {
                "Title": f"{retrieved_metadata.get('product', 'Unknown Product')} ({retrieved_metadata.get('document_type', 'Policy')})",
                "Effective Date": retrieved_metadata.get('effective_date', 'N/A'),
                "Source URL": retrieved_metadata.get('source_url', '#')
            }
        ]
        # 3. Render them using the expander code
        with st.expander("📄 Offenlegungen und Dokumente anzeigen"):
            for source in retrieved_sources:
                st.markdown(f"- **{source['Title']}**")
                st.caption(f"Effective Date: {source['Effective Date']} | [Link]({source['Source URL']})")
        
    # Append assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_response, "sources": retrieved_sources})

# Force a rerun so the UI updates cleanly
    st.rerun()

# =========================================================
# 6. RENDER CONVERSATION HISTORY (Flows below the top chips)
# =========================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # <-- PARE IT HERE: Right inside the message loop!
        if "sources" in msg and msg["sources"]:
            with st.expander("📄 Offenlegungen und Dokumente anzeigen"):
                for source in msg["sources"]:
                    st.markdown(f"- **{source['Title']}**")
                    st.caption(f"Effective Date: {source['Effective Date']} | [Link]({source['Source URL']})")
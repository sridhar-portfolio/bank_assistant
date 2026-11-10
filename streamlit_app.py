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

##################### CSS #########################

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

##########################################################################

# Streamlit automatically loads secrets into st.secrets or os.environ
api_key = st.secrets["OPENAI_API_KEY"]

# Get the directory where app.py is currently located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the safe path to your vector folder
vector_folder_path = os.path.join(current_dir, "vector_store")

# 1. Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Initialize a variable to hold user input (from chat input OR chips)
user_query = None

st.title("🏦 YourFinBank Assistant")
st.caption("Ask me anything about savings accounts, credit cards, loans, and banking policies.")

# 3. Render Quick-Start Chips ONLY if the conversation is empty
if len(st.session_state.messages) == 0:
    st.markdown("### Suggested Questions")
    
    # Define your quick prompts
    chips = [
        "Wie hoch ist die Entgelte für Zahlungsverkehrsdienstleistungen für Bargeldeinzahlungen an eigene Kunden am Schalter?",
        "Wie hoch sind die Gebühren für Echtzeit-Überweisungsaufträge?",
        "Wie wäre es mit einem Ersatzpasswort? Kostet mich das etwas?",
        "Wie hoch ist die monatliche Kontoführungsgebühr?"
    ]
    
    # Create responsive columns for the chips
    col1, col2, col3 = st.columns(3)
    
    if col1.button(chips[0], use_container_width=True):
        user_query = chips[0]
    if col2.button(chips[1], use_container_width=True):
        user_query = chips[1]
    if col3.button(chips[2], use_container_width=True):
        user_query = chips[2]
    if col3.button(chips[3], use_container_width=True):
        user_query = chips[3]

# 4. Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # If the message has stored sources, render them in an expander
        if "sources" in message and message["sources"]:
            with st.expander("📄 View Source Disclosures & Documents"):
                for source in message["sources"]:
                    st.markdown(f"- **{source['Title']}**")
                    st.caption(f"Effective Date: {source['Effective Date']} | [Link]({source['Source URL']})")

# 5. Handle Chat Input (Standard Streamlit chat bar)
chat_input = st.chat_input("Type your banking question here...")

# If the user typed something OR clicked a chip, process it
if chat_input:
    user_query = chat_input

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
        with st.expander("📄 View Source Disclosures & Documents"):
            for source in retrieved_sources:
                st.markdown(f"- **{source['Title']}**")
                st.caption(f"Effective Date: {source['Effective Date']} | [Link]({source['Source URL']})")
        
    # Append assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_response, "sources": retrieved_sources})

#with st.form("my_form"):
#    text = st.text_area(
#        "Enter text:",
#        "Wie hoch ist die Entgelte für Zahlungsverkehrsdienstleistungen für Bargeldeinzahlungen an eigene Kunden am Schalter?",
#    )
#    submitted = st.form_submit_button("Submit")
#    if submitted:
#        retrieved_context, response = rag_function(text, vector_folder_path, "giroplus_index", api_key)
#        st.info(response)
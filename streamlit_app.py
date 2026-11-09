import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

st.title("🦜🔗 Quickstart App")

# Streamlit automatically loads secrets into st.secrets or os.environ
api_key = st.secrets["OPENAI_API_KEY"]


def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=api_key)
    st.info(model.invoke(input_text).content)


with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if not api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and api_key.startswith("sk-"):
        generate_response(text)
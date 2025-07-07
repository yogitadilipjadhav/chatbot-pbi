import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 AI Chatbot for Power BI")

# Initialize OpenAI Client
#openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY") or "sk-Your-OpenAI-Key-Here"
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# User Input
user_input = st.text_input("Ask me anything about your business data:")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert business analyst providing insights on consumer dynamics, volume, and spend."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5,
                max_tokens=500
            )
            message = response.choices[0].message.content.strip()
            st.success(message)
        except Exception as e:
            st.error(f"Error: {e}")

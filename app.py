import streamlit as st
import openai
 
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot for Power BI")
 
# Load API key
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key  # Still required for some environments, but optional in v1.x
 
# User Input
user_input = st.text_input("Ask me anything about your business data:")
 
if user_input:
    with st.spinner("Thinking..."):
        try:
            response = openai.chat.completions.create(  # ✅ FIXED HERE
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
OpenAI
We believe our research will eventually lead to artificial general intelligence, a system that can solve human-level problems. Building safe and beneficial AGI is our mission.
 

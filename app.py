import streamlit as st
import openai
 
st.title("🤖 AI Chatbot for Power BI")
 
# Load API key
openai.api_key = st.secrets["OPENAI_API_KEY"]
 
user_input = st.text_input("Ask me anything:")
 
if user_input:
    try:
     response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            max_tokens=500
        )
     st.success(response.choices[0].message.content.strip())
    except Exception as e:
        st.error(f"Error: {e}")

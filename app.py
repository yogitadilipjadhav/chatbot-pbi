import streamlit as st
import pandas as pd
import openai

# Set page configuration
st.set_page_config(page_title="Power BI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot for Power BI Dashboard")

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load the exported Power BI data
@st.cache_data
def load_data():
    return pd.read_csv("powerbi_dashboard_data.csv")

data = load_data()

# Extract distinct values for chatbot responses
available_columns = list(data.columns)
available_countries = sorted(data['Country'].dropna().unique())
available_products = sorted(data['Product'].dropna().unique())
available_years = sorted(data['Year'].dropna().unique())
available_quarters = sorted(data['Quarter'].dropna().unique())
available_months = sorted(data['Month'].dropna().unique())

# Input from user
user_input = st.text_input("Ask me anything about this dashboard:")

# Predefined answers using actual data
def get_predefined_response(question):
    q = question.lower()
    if "column" in q or "field" in q:
        return f"📊 The available columns are: **{', '.join(available_columns)}**"
    elif "country" in q:
        return f"🌍 Available countries: **{', '.join(available_countries)}**"
    elif "product" in q:
        return f"📦 Available products: **{', '.join(available_products)}**"
    elif "year" in q:
        return f"📅 Available years: **{', '.join(map(str, available_years))}**"
    elif "quarter" in q:
        return f"🕓 Available quarters: **{', '.join(available_quarters)}**"
    elif "month" in q:
        return f"📆 Available months: **{', '.join(available_months)}**"
    elif "summary" in q or "dashboard" in q:
        return "📝 This dashboard shows sales and discount trends by Country, Product, and Time."
    else:
        return None

# Generate response
if user_input:
    answer = get_predefined_response(user_input)
    
    if not answer:
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a Power BI dashboard."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5,
                max_tokens=500
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"⚠️ Error: {e}"
    
    st.write(answer)

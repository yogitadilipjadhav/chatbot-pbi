import streamlit as st 
import pandas as pd 
from openai import OpenAI 
import re

#Set page configuration
st.set_page_config(page_title="Power BI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot for Power BI Dashboard")

#Initialize OpenAI client (New API)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#Load Data (Cached for speed)
@st.cache_data 
def load_data(): 
    df = pd.read_csv('test-pbi-data.csv', encoding='utf-8', low_memory=False, dtype=str) 
    return df

df = load_data()
st.title("📊 AI Business Insights Chatbot (No Dropdowns)")

#Pre-load unique values for simple keyword extraction
brands = [str(b).lower() for b in df['BRAND'].dropna().unique()] 
markets = [str(m).lower() for m in df['MARKET_SHORT'].dropna().unique()] 
kpis = [str(k).lower() for k in df['KPI'].dropna().unique()] 
periods = [str(p).lower() for p in df['PERIOD'].dropna().unique()]

#Step 1: User Question Input
user_question = st.text_area("Ask your business question:", height=100)

#Keyword Extraction
def extract_keywords(question): 
    question_lower = question.lower() 
    found_brand = next((b for b in brands if b in question_lower), None) 
    found_market = next((m for m in markets if m in question_lower), None) 
    found_kpi = next((k for k in kpis if k in question_lower), None) 
    found_period = next((p for p in periods if p in question_lower), None) 
    return found_brand, found_market, found_kpi, found_period

#Step 2: Apply Filters Automatically
if st.button("Get AI Insight") and user_question.strip() != "":
    brand, market, kpi, period = extract_keywords(user_question)
 
    filtered_df = df.copy()
 
    if brand:
        filtered_df = filtered_df[filtered_df['BRAND'].str.lower() == brand]
    if market:
        filtered_df = filtered_df[filtered_df['MARKET_SHORT'].str.lower() == market]
    if kpi:
        filtered_df = filtered_df[filtered_df['KPI'].str.lower() == kpi]
    if period:
        filtered_df = filtered_df[filtered_df['PERIOD'].str.lower() == period]
 
    if not filtered_df.empty:
        summary_df = filtered_df.groupby(['BRAND', 'MARKET_SHORT', 'KPI', 'PERIOD'])['Value'].sum().reset_index()
        summary_df = summary_df.sort_values(by='Value', ascending=False).head(10)  # Limit to top 10 rows
        summary_text = summary_df.to_string(index=False)
    else:
        summary_text = "No matching data found."
 
    # Step 3: Generate AI Answer
    prompt = f"""
    You are an AI business analyst. Here is the data you can use:
 
    {summary_text}
 
    Answer the user's question in a concise and professional business tone:
 
    Question: {user_question}
    """
 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert business insights assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
 
    ai_answer = response.choices[0].message.content
 
    st.success(ai_answer)
 
    st.markdown(f"**Filters used:** Brand: `{brand}`, Market: `{market}`, KPI: `{kpi}`, Period: `{period}`")
 
    with st.expander("See Filtered Data"):
        st.dataframe(filtered_df)
else:
    st.info("Enter a question and click the button to get insights.")

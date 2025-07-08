import streamlit as st
import openai

# Set Streamlit page settings
st.set_page_config(page_title="Power BI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot for Power BI")

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Static Report Information
report_info = {
    "columns": ["Country", "Product", "Discounts", "Gross Sales"],
    "filters": ["Country", "Product", "Segment", "Manufacturer", "Brand", "Target Population", "Market"],
    "measures": ["Penetration (%)", "Manufacturer Share (%)", "Gross Sales", "Discounts"],
    "dashboard_summary": (
        "This dashboard provides insights into market performance, category trends, and manufacturer shares. "
        "You can filter by Country, Product, Segment, Brand to view Penetration %, Manufacturer Share %, Gross Sales, and Discounts."
    )
}

# User Input
user_input = st.text_input("Ask me anything about the dashboard:")

# Function to check for known questions
def predefined_response(question):
    question = question.lower()
    if "column" in question or "field" in question:
        return f"📊 The columns are: **{', '.join(report_info['columns'])}**"
    elif "filter" in question:
        return f"🔍 The filters available are: **{', '.join(report_info['filters'])}**"
    elif "measure" in question or "metric" in question or "kpi" in question:
        return f"📈 The measures shown are: **{', '.join(report_info['measures'])}**"
    elif "summary" in question or "dashboard" in question or "what does" in question:
        return f"📝 {report_info['dashboard_summary']}"
    else:
        return None

# Generate response
if user_input:
    # Check for predefined answers
    response_text = predefined_response(user_input)

    # If no predefined answer → Call OpenAI
    if not response_text:
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Power BI users."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5,
                max_tokens=500
            )
            response_text = response.choices[0].message.content.strip()
        except Exception as e:
            response_text = f"⚠️ Error: {e}"

    st.write(response_text)

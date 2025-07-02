# app.py
import streamlit as st
import pandas as pd

# 1. Load data from public Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1vbH4bWqwFVSWprF0U4wsyWFjtiSiVbW8/export?format=csv"

st.set_page_config(page_title="Partner Talktime Dashboard", layout="wide")
st.title("📞 Partner Engagement Dashboard")

# Load and prepare data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(sheet_url)
    df['Talktime_min'] = df['Talktime'] / 60  # Convert seconds to minutes

    # Categorize partners
    def status(row):
        if row['Calls'] == 0:
            return "🟥 Not Connected"
        elif row['Talktime_min'] < 1:
            return "🟨 <1 Min Talktime"
        else:
            return "🟩 Active"
    
    df['Status'] = df.apply(status, axis=1)
    return df

df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Talktime (min)", f"{df['Talktime_min'].sum():.1f}")
col2.metric("Total Partners", df.shape[0])
col3.metric("Partners with No Calls", (df['Calls'] == 0).sum())

# Filter options
status_filter = st.selectbox("📂 Filter by Partner Status", options=["All", "🟥 Not Connected", "🟨 <1 Min Talktime", "🟩 Active"])
if status_filter != "All":
    df = df[df['Status'] == status_filter]

# Display Table
st.subheader("📋 Partner-wise Details")
st.dataframe(df[['PartnerCode', 'Talktime_min', 'Calls', 'Status']].sort_values(by='Talktime_min', ascending=False), use_container_width=True)

# Bar Chart
st.subheader("📊 Talktime by Partner (in Minutes)")
st.bar_chart(df.set_index("PartnerCode")["Talktime_min"])

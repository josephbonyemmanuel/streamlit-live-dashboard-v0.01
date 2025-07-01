# app.py
import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Live Dashboard", layout="wide")

st.title("📊 Live Google Sheets Dashboard")

# 1. Load data from public Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1vbH4bWqwFVSWprF0U4wsyWFjtiSiVbW8/export?format=csv"
df = pd.read_csv(sheet_url)

# 2. Show data table
# st.subheader("📋 Data Table")
#st.dataframe(df)

# 3. Optional line chart
if 'talktime' in df.columns and 'partner' in df.columns:
    df = df.sort_values(by='talktime')
    st.line_chart(df.set_index('partner')['talktime'])
else:
    st.warning("Please make sure 'talktime' and 'partner' columns exist in your sheet.")

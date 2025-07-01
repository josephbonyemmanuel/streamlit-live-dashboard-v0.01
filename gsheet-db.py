# app.py
import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Live Dashboard", layout="wide")

st.title("📊 Live Google Sheets Dashboard")

# 1. Load data from public Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1JWSDu3P5wYeiuTWQQ-QfkwafOD_jZO2NjQflBsZLOj8/export?format=csv"
df = pd.read_csv(sheet_url)

# 2. Show data table
st.subheader("📋 Data Table")
st.dataframe(df)

# 3. Optional line chart
if 'Date' in df.columns and 'Sales' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    st.line_chart(df.set_index('Date')['Sales'])
else:
    st.warning("Please make sure 'Date' and 'Sales' columns exist in your sheet.")

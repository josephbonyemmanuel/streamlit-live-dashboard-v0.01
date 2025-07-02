import streamlit as st
import pandas as pd

sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    st.write("✅ Sheet loaded")
    st.write(df.head())
    st.write("📑 Columns:", df.columns.tolist())
except Exception as e:
    st.error(f"❌ Error loading sheet: {e}")

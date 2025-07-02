import streamlit as st
import pandas as pd

# 🔁 Step 1: Replace with your real Google Sheet ID
SHEET_ID = "1vbH4bWqwFVSWprF0U4wsyWFjtiSiVbW8"  # <-- 🔁 change this
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 🔧 Step 2: Page settings
st.set_page_config(page_title="Partner Engagement Dashboard", layout="wide")
st.title("📞 Partner Engagement Dashboard")

# 📥 Step 3: Load data directly
try:
    df = pd.read_csv(sheet_url)

    # Show raw columns (for debugging)
    st.write("🔍 Raw columns:", df.columns.tolist())

    # Check required columns
    if "partner" not in df.columns or "Talktime" not in df.columns or "Calls" not in df.columns:
        st.error("❌ Missing required columns: 'partner', 'Talktime', 'Calls'")
        st.stop()

    # Step 4: Clean up
    df.rename(columns={"partner": "PartnerCode"}, inplace=True)
    df = df[["PartnerCode", "Talktime", "Calls"]]  # Drop 'a' column

    # Step 5: Convert seconds to min

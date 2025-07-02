import streamlit as st
import pandas as pd

# ✅ Your actual Google Sheet ID
SHEET_ID = "1vbH4bWqwFVSWprF0U4wsyWFjtiSiVbW8"
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 🔧 Streamlit settings
st.set_page_config(page_title="Partner Engagement Dashboard", layout="wide")
st.title("📞 Partner Engagement Dashboard")

# 🔄 Load and process data
try:
    df = pd.read_csv(sheet_url)

    # ✅ Show raw columns for debug
    st.write("📑 Columns detected:", df.columns.tolist())

    # ✅ Check required columns
    expected_cols = {"partner", "Talktime", "Calls"}
    if not expected_cols.issubset(set(df.columns)):
        st.error("❌ Your sheet must contain columns: 'partner', 'Talktime', and 'Calls'")
        st.stop()

    # ✅ Rename + cleanup
    df.rename(columns={"partner": "PartnerCode"}, inplace=True)
    df = df[["PartnerCode", "Talktime", "Calls"]]
    df["Talktime_min"] = df["Talktime"] / 60

    # ✅ Categorize engagement
    def classify(row):
        if row["Calls"] == 0:
            return "🟥 Not Connected"
        elif row["Talktime_min"] < 1:
            return "🟨 <1 Min Talktime"
        else:
            return "🟩 Active"
    
    df["Status"] = df.apply(classify, axis=1)

    # ✅ KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Total T

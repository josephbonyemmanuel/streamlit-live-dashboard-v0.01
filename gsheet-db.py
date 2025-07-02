import streamlit as st
import pandas as pd

# 🟡 Step 1: Paste your Google Sheet ID here
SHEET_ID = "1AbCDEfghXYZ12345678"  # 🔁 Replace with your actual Google Sheet ID
sheet_url = f"https://docs.google.com/spreadsheets/d/1vbH4bWqwFVSWprF0U4wsyWFjtiSiVbW8/export?format=csv"

# 🟢 Step 2: Streamlit page config
st.set_page_config(page_title="Partner Engagement Dashboard", layout="wide")
st.title("📞 Partner Engagement Dashboard")

# 🔄 Step 3: Load and process data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(sheet_url)

    # Rename column: partner → PartnerCode
    df.rename(columns={"partner": "PartnerCode"}, inplace=True)

    # Keep only needed columns
    df = df[["PartnerCode", "Talktime", "Calls"]]

    # Convert talktime from seconds to minutes
    df["Talktime_min"] = df["Talktime"] / 60

    # Add engagement status
    def classify(row):
        if row["Calls"] == 0:
            return "🟥 Not Connected"
        elif row["Talktime_min"] < 1:
            return "🟨 <1 Min Talktime"
        else:
            return "🟩 Active"
    
    df["Status"] = df.apply(classify, axis=1)
    return df

df = load_data()

# 📊 Step 4: Show KPI Summary
col1, col2, col3 = st.columns(3)
col1.metric("📈 Total Talktime (min)", f"{df['Talktime_min'].sum():.1f}")
col2.metric("👥 Total Partners", df.shape[0])
col3.metric("📞 No Calls", (df["Calls"] == 0).sum())

# 🔍 Step 5: Filter by Status
status_filter = st.selectbox("📂 Filter by Partner Status", ["All", "🟥 Not Connected", "🟨 <1 Min Talktime", "🟩 Active"])
if status_filter != "All":
    df = df[df["Status"] == status_filter]

# 🧾 Step 6: Show Data Table
st.subheader("📋 Partner-wise Talktime")
st.dataframe(
    df[["PartnerCode", "Talktime_min", "Calls", "Status"]]
    .sort_values(by="Talktime_min", ascending=False),
    use_container_width=True
)

# 📉 Step 7: Show Bar Chart
st.subheader("📊 Talktime by Partner")
st.bar_chart(df.set_index("PartnerCode")["Talktime_min"])

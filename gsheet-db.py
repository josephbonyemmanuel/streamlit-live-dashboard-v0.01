import streamlit as st
import pandas as pd

# ✅ Use your actual Google Sheet ID here
SHEET_ID = "1vbH4bWqwFVSWprF0U4wsyWFjtiSiVbW8"
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 🔧 Streamlit page settings
st.set_page_config(page_title="Partner Engagement Dashboard", layout="wide")
st.title("📞 Partner Engagement Dashboard")

# 🔄 Load and process data
try:
    # 🟢 Read Google Sheet as CSV
    df = pd.read_csv(sheet_url)

    # 🧪 Debug: Show columns
    st.write("📑 Columns detected:", df.columns.tolist())

    # ✅ Check expected columns
    expected_cols = {"partner", "Talktime", "Calls"}
    if not expected_cols.issubset(set(df.columns)):
        st.error("❌ Your sheet must contain columns: 'partner', 'Talktime', 'Calls'")
        st.stop()

    # 🛠 Clean and transform
    df.rename(columns={"partner": "PartnerCode"}, inplace=True)
    df = df[["PartnerCode", "Talktime", "Calls"]]

    # 🔢 Convert columns to numbers
    df["Talktime"] = pd.to_numeric(df["Talktime"], errors="coerce").fillna(0)
    df["Calls"] = pd.to_numeric(df["Calls"], errors="coerce").fillna(0)

    # ⏱ Convert seconds to minutes
    df["Talktime_min"] = df["Talktime"] / 60

    # 🟦 Classify partner status
    def classify(row):
        if row["Calls"] == 0:
            return "🟥 Not Connected"
        elif row["Talktime_min"] < 1:
            return "🟨 <1 Min Talktime"
        else:
            return "🟩 Active"
    
    df["Status"] = df.apply(classify, axis=1)

    # 📊 Show KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Total Talktime (min)", f"{df['Talktime_min'].sum():.1f}")
    col2.metric("👥 Total Partners", df.shape[0])
    col3.metric("📞 No Calls", int((df["Calls"] == 0).sum()))
    

    # 🔍 Filter by status
    status_filter = st.selectbox(
        "📂 Filter by Partner Status",
        ["All", "🟥 Not Connected", "🟨 <1 Min Talktime", "🟩 Active"]
    )
    if status_filter != "All":
        df = df[df["Status"] == status_filter]

    # 🧾 Table view
    st.subheader("📋 Partner-wise Talktime")
    st.dataframe(
        df[["PartnerCode", "Talktime_min", "Calls", "Status"]]
        .sort_values(by="Talktime_min", ascending=False),
        use_container_width=True
    )


    # ✅ KPI: Minimum 1 min talktime to 71.5% of partners
    total_partners = df["PartnerCode"].nunique()
    met_target = df[df["Talktime_min"] >= 1].shape[0]
    achieved_pct = (met_target / total_partners) * 100
    
    # Show result
    if achieved_pct >= 71.5:
        st.success(f"✅ {achieved_pct:.1f}% of partners have ≥1 min talktime (Target: 71.5%)")
    else:
        st.error(f"⚠️ Only {achieved_pct:.1f}% of partners have ≥1 min talktime (Target: 71.5%)")
    
    # Optional: show visual progress
    st.progress(min(int(achieved_pct), 100))

    # 📈 Bar chart
    st.subheader("📊 Talktime by Partner")
    st.bar_chart(df.set_index("PartnerCode")["Talktime_min"])


except Exception as e:
    st.error(f"❌ Could not load or process Google Sheet: {e}")

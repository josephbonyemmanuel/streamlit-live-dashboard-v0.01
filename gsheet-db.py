import streamlit as st

import pandas as pd
import datetime

# --- Configuration ---
SHEET_ID = "1vbH4bWqwFVSWprF0U4wsyWFjtiSiVbW8"
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
st.set_page_config(page_title="SVRM Performance Dashboard", layout="wide")
st.title("📊 SVRM Incentive & Engagement Dashboard")

# --- Load Data ---
try:
    df = pd.read_csv(sheet_url)

    # ✅ Extract only required columns for analysis
    df = df[[
        "Partner code", "FRM Code", "Secondary RM Code", "First Activation Date",
        "MTD  APE", "Overall Talktime","Impact on First Activation Reg No.",
        "Impact APE"
    ]]

    # ✅ Rename columns for easier access
    df.rename(columns={
        "Partner code": "PartnerCode",
        "FRM Code": "FRM_Code",
        "Secondary RM Code": "Secondary_RM",
        "MTD  APE": "MTD_APE",
        "Overall Talktime": "Talktime",
        "First Activation Date": "First_Activation",
        "Impact on First Activation Reg No.":"My_Activation",
        "Impact APE":"SVRM_Business"
    }, inplace=True)

    # --- Clean & Prepare Data ---
    df["Talktime"] = pd.to_numeric(df["Talktime"], errors="coerce").fillna(0)
    df["MTD_APE"] = pd.to_numeric(df["MTD_APE"], errors="coerce").fillna(0)
    df["Talktime_min"] = (df["Talktime"] / 60).round(1)
    df["My_Activation"] = pd.to_numeric(df["My_Activation"], errors="coerce").fillna(0)
    df["SVRM_Business"] = pd.to_numeric(df["SVRM_Business"], errors="coerce").fillna(0)

    # ✅ Activation Flag
    df["Activated_By_Me"] = df["My_Activation"].apply(lambda x: "Yes" if x >= 1 else "No")

    # ✅ Partner Status by Talktime
    def status(row):
        if row["Talktime_min"] == 0:
            return "🟥 Not Connected"
        elif row["Talktime_min"] < 1:
            return "🟨 <1 Min"
        else:
            return "🟩 Connected"
    df["Status"] = df.apply(status, axis=1)

    # ✅ Metrics
    total_partners = df["PartnerCode"].nunique()
    connected_1min = df[df["Talktime_min"] >= 1].shape[0]
    connected_pct = (connected_1min / total_partners) * 100

    activated_count = df[df["Activated_By_Me"] == "Yes"].shape[0]
    activation_target = 26
    activation_score = min(activated_count / activation_target, 1.3) * 40

    # Business Score (AP)
    total_business = df["MTD_APE"].sum()
    my_business = df["SVRM_Business"].sum()
    business_pct = (my_business / total_business) * 100 if total_business > 0 else 0
    business_score = min(business_pct / 12, 1.3) * 40

    # Connectivity Score
    connectivity_score = min(connected_pct / 55, 1.3) * 20

    # Total Score
    total_score = activation_score + business_score + connectivity_score

    # 📅 Projection: Expected Business at Month End
    today = datetime.date.today().day
    last_day = (datetime.date.today().replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    days_in_month = last_day.day

    expected_business_pct = (business_pct / today) * days_in_month
    expected_business_pct = min(expected_business_pct, 130)

    # 🔲 KPI Meters
    st.subheader("📈 Business Progress")
    m1, m2 = st.columns(2)
    m1.metric("💼 Actual Business %", f"{business_pct:.1f}%", f"Target ≥ 12%")
    m2.metric("🔮 Expected EOM Business %", f"{expected_business_pct:.1f}%", f"Projection")

    st.subheader("🎯 Incentive KPI Breakdown")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🟢 Activation", f"{activated_count} / 26", f"{activation_score:.1f} pts")
    k2.metric("📦 Business %", f"{business_pct:.1f}%", f"{business_score:.1f} pts")
    k3.metric("📞 Connected >1 Min", f"{connected_pct:.1f}%", f"{connectivity_score:.1f} pts")
    k4.metric("🏁 Total Score", f"{total_score:.1f} / 130")

    if total_score >= 120:
        st.success("🎉 You're on track for maximum incentive!")
    elif total_score >= 100:
        st.info("👍 Safe zone. Push to cross 120.")
    else:
        st.warning("⚠️ Below target. Focus on activation, business & talktime.")

    # --- 📊 Business & Call Summary ---
    st.subheader("📌 Summary Metrics")
    
    # Total business
    total_business_value = df["MTD_APE"].sum()
    
    # Call Buckets
    not_connected = df[df["Talktime"] == 0].shape[0]
    less_than_1_min = df[(df["Talktime"] > 0) & (df["Talktime"] < 60)].shape[0]
    greater_than_1_min = df[df["Talktime"] >= 60].shape[0]
    
    # Business Buckets
    more_than_4k = df[df["MTD_APE"] > 4000].shape[0]
    zero_business = df[df["MTD_APE"] == 0].shape[0]
    less_than_4k = df[(df["MTD_APE"] > 0) & (df["MTD_APE"] <= 4000)].shape[0]
    
    # Display as columns
    s1, _ = st.columns(2)
    s1.metric("💰 Total Business", f"₹ {total_business_value:,.0f}")
    
    s2, s3, s4, s5, s6, s7 = st.columns(3)
    s2.metric("📞 Not Connected", not_connected)
    s3.metric("⏱️ <1 Min Talktime", less_than_1_min)
    s4.metric("📞 >1 Min Talktime", greater_than_1_min)
    s5.metric("🏆 > ₹4K Business", more_than_4k)
    s6.metric("🚫 ₹0 Business", zero_business)
    s7.metric("⚠️ < ₹4K Business", less_than_4k)

    
    # 🔍 Filter Section
    st.subheader("🔍 Partner Filter")
    filter_status = st.selectbox("Filter by Status", ["All", "🟥 Not Connected", "🟨 <1 Min", "🟩 Connected"])
    if filter_status != "All":
        df = df[df["Status"] == filter_status]

    # 📋 Partner Table
    st.subheader("📋 Partner-wise Performance")
    st.dataframe(df[[
        "PartnerCode", "FRM_Code", "Secondary_RM", "MTD_APE","SVRM_Business",
        "Talktime_min", "Activated_By_Me", "Status"
    ]].sort_values(by="Talktime_min", ascending=False), use_container_width=True)

    # 📊 Chart
    st.subheader("📊 Partner Talktime (mins)")
    st.bar_chart(df.set_index("PartnerCode")["Talktime_min"])

except Exception as e:
    st.error(f"❌ Error loading sheet: {e}")

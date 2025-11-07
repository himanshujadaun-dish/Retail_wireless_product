# ------------------------------------------------------------
# Wireless Cortex AI v4.4 — Feedback Analytics + Google Sheet Sync
# ------------------------------------------------------------
import streamlit as st
import pandas as pd
import time
from datetime import datetime
import uuid
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

# ------------------------------------------------------------
# GOOGLE SHEETS CONFIG
# ------------------------------------------------------------
INFO_SHEET_URL = "https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/edit?gid=0#gid=0"
LOG_SHEET_ID  = "1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y"
SERVICE_ACCOUNT_FILE = "google_sheet_token.json"

# ------------------------------------------------------------
# GOOGLE SHEET CONNECTION
# ------------------------------------------------------------
try:
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gclient = gspread.authorize(creds)
    gsheet = gclient.open_by_key(LOG_SHEET_ID).sheet1
except Exception as e:
    gsheet = None
    st.warning(f"⚠️ Could not connect to Google Sheets: {e}")

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# STATE
# ------------------------------------------------------------
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "page" not in st.session_state:
    st.session_state.page = "chat"  # default page

# ------------------------------------------------------------
# THEME COLORS
# ------------------------------------------------------------
if st.session_state.theme == "light":
    bg_grad, header_grad, text_color, box_color, accent = (
        "linear-gradient(180deg,#f9fbfd 0%,#f0f4f8 100%)",
        "linear-gradient(90deg,#004b91,#007acc)",
        "#000",
        "white",
        "#007acc",
    )
else:
    bg_grad, header_grad, text_color, box_color, accent = (
        "linear-gradient(180deg,#101010 0%,#1c1c1c 100%)",
        "linear-gradient(90deg,#0a1931,#001f3f)",
        "#f5f5f5",
        "#1a1a1a",
        "#4da8ff",
    )

# ------------------------------------------------------------
# STYLING
# ------------------------------------------------------------
st.markdown(f"""
<style>
.stApp {{
    background:{bg_grad};
    color:{text_color};
    font-family:'Segoe UI',sans-serif;
}}
header,footer{{visibility:hidden;}}
.chat-bubble-user{{background:#e8f3ff;padding:10px 15px;border-radius:15px;margin:5px 0;max-width:80%;}}
.chat-bubble-bot{{background:{box_color};padding:10px 15px;border-radius:15px;margin:5px 0;
 box-shadow:0 2px 8px rgba(0,0,0,0.2);max-width:80%;}}
.kpi-card{{background:{box_color};border-radius:15px;padding:15px;
 box-shadow:0 2px 5px rgba(0,0,0,0.25);text-align:center;
 transition:transform .2s ease,box-shadow .2s ease;}}
.kpi-card:hover{{transform:scale(1.03);box-shadow:0 4px 10px rgba(0,0,0,0.35);}}
.kpi-value{{font-size:24px;font-weight:bold;color:{accent};}}
.kpi-label{{color:gray;font-size:14px;}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------
with st.sidebar:
    st.title("📂 Navigation")
    if st.button("💬 Chat Assistant", use_container_width=True):
        st.session_state.page = "chat"; st.rerun()
    if st.button("📊 Feedback Analytics", use_container_width=True):
        st.session_state.page = "analytics"; st.rerun()
    st.markdown("---")

    if st.button("🌓 Toggle Dark / Light Mode", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()
    st.markdown("---")

# ------------------------------------------------------------
# PAGE: FEEDBACK ANALYTICS
# ------------------------------------------------------------
if st.session_state.page == "analytics":
    st.markdown(f"""
    <div style='text-align:center;padding:15px 0;background:{header_grad};
    color:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.2);'>
    <h1>📊 Feedback Analytics</h1></div>
    """, unsafe_allow_html=True)

    if gsheet:
        # Load feedback log
        data = pd.DataFrame(gsheet.get_all_records())
        if not data.empty:
            st.subheader("Overall Feedback Summary")
            total = len(data)
            thumbs_up = len(data[data["feedback"] == "thumbs_up"])
            thumbs_down = len(data[data["feedback"] == "thumbs_down"])
            approval_rate = round((thumbs_up / total) * 100, 1) if total else 0

            k1, k2, k3 = st.columns(3)
            k1.metric("👍 Positive Feedback", thumbs_up)
            k2.metric("👎 Negative Feedback", thumbs_down)
            k3.metric("✅ Approval Rate", f"{approval_rate}%")

            st.markdown("---")
            st.subheader("Trend Over Time")
            data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
            daily = data.groupby(data["timestamp"].dt.date)["feedback"].value_counts().unstack(fill_value=0)
            fig = px.line(daily, x=daily.index, y=["thumbs_up", "thumbs_down"],
                          markers=True, title="Feedback Trend")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.subheader("Top 5 Most Liked / Disliked Responses")

            top_like = (
                data[data["feedback"] == "thumbs_up"]["message"]
                .value_counts()
                .head(5)
                .reset_index()
                .rename(columns={"index": "Response", "message": "Count"})
            )
            top_dislike = (
                data[data["feedback"] == "thumbs_down"]["message"]
                .value_counts()
                .head(5)
                .reset_index()
                .rename(columns={"index": "Response", "message": "Count"})
            )

            c1, c2 = st.columns(2)
            with c1:
                st.write("👍 Most Liked Responses")
                st.dataframe(top_like)
            with c2:
                st.write("👎 Most Disliked Responses")
                st.dataframe(top_dislike)
        else:
            st.info("No feedback data found yet.")
    else:
        st.error("Google Sheets connection unavailable.")
    st.stop()

# ------------------------------------------------------------
# PAGE: CHAT ASSISTANT
# ------------------------------------------------------------

# HEADER
st.markdown(f"""
<div style='text-align:center;padding:15px 0;background:{header_grad};
color:white;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.2);'>
<h1>📶 Wireless Cortex AI</h1>
<p>Your Retail Wireless Data & Forecast Assistant</p></div>
""", unsafe_allow_html=True)

st.markdown(
    f"""<div style="text-align:center;margin-top:10px;">
    <a href="{INFO_SHEET_URL}" target="_blank"
    style="text-decoration:none;color:{accent};font-weight:500;font-size:15px;">ℹ️ Info</a>
    </div>""",
    unsafe_allow_html=True,
)
st.markdown("---")

# KPI OVERVIEW
st.subheader("📈 Cortex Quick Overview")
cols = st.columns(4)
for c, (v, l) in zip(cols, [("96.3%", "Forecast Accuracy"), ("420", "Active SKUs"),
                            ("4", "Channels"), ("3", "Delayed Shipments")]):
    c.markdown(f"<div class='kpi-card'><div class='kpi-value'>{v}</div>"
               f"<div class='kpi-label'>{l}</div></div>", unsafe_allow_html=True)

# ACTIVE DATA SOURCES
with st.expander("🧩 Active Data Sources"):
    st.markdown("""
| Data Source | Status |
|--------------|--------|
| 🛒 Sales | ✅ Connected |
| 🏭 Inventory | ✅ Connected |
| 🚚 Shipments | ✅ Connected |
| 💲 Pricing | ✅ Connected |
| 📈 Forecast | ✅ Connected |
""")
st.markdown("---")

# RESPONSES
faq = {
    "sales": "Top-selling devices: iPhone 16 (12.3K), Galaxy A15 (10.1K), Moto G (8.7K).",
    "inventory": "Low-stock SKUs: iPhone 15 Blue (Denver), Galaxy A15 (Dallas).",
    "shipments": "18,420 units shipped this week — some delays at Marceco.",
    "pricing": "Average margin 12.4%. Price drops on A15 and iPhone 15.",
    "forecast": "Forecast accuracy 96.3% in Oct; growth expected 10–12% MoM."
}
cats = {
    "🛒 Sales": ["What were the top-selling devices last month?"],
    "🏭 Inventory": ["Which SKUs are low in stock?"],
    "🚚 Shipments": ["Show delayed shipments by DDP."],
    "💲 Pricing": ["Which SKUs had price drops this week?"],
    "📈 Forecast": ["Show activation forecast by SKU."]
}

# CATEGORY PANEL
if not st.session_state.messages:
    st.info("💬 Hi! I’m Cortex AI. Ask me about Sales, Inventory, Shipments, Pricing, or Forecasts.")
    st.markdown("### 💬 Choose an option below for suggested questions or ask a question:")
    cols = st.columns(3)
    for i, (cat, qs) in enumerate(cats.items()):
        with cols[i % 3]:
            with st.expander(cat):
                for j, q in enumerate(qs):
                    if st.button(q, key=f"{cat}_{j}"):
                        st.session_state.messages.append({"role": "user", "content": q})
                        st.rerun()

# DISPLAY CHAT
for i, m in enumerate(st.session_state.messages):
    bubble = "chat-bubble-user" if m["role"] == "user" else "chat-bubble-bot"
    st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)
    if m["role"] == "bot":
        c1, c2 = st.columns([0.1, 0.9])
        with c1:
            if st.button("👍", key=f"up_{i}"):
                if gsheet:
                    gsheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       st.session_state.session_id, m["content"], "thumbs_up"])
                st.toast("✅ Thanks for your feedback!", icon="👍")
        with c2:
            if st.button("👎", key=f"down_{i}"):
                if gsheet:
                    gsheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       st.session_state.session_id, m["content"], "thumbs_down"])
                st.toast("⚠️ Feedback recorded", icon="👎")

# CHAT INPUT
if prompt := st.chat_input("Ask your question here…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# BOT RESPONSE
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    q = st.session_state.messages[-1]["content"]
    topic = next((t for t in faq if t in q.lower()), None)
    with st.spinner("🤖 Cortex AI is analyzing…"):
        for step in ["Analyzing data", "Querying Snowflake", "Generating insights"]:
            st.write(f"🔍 {step}…"); time.sleep(0.4)
    ans = faq.get(topic, "⚠️ LIMITED DATA — working on getting more sources in.")
    st.session_state.messages.append({"role": "bot", "content": ans})
    st.session_state.chat_sessions.append(
        {"timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
         "messages": st.session_state.messages.copy()})
    st.rerun()

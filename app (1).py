# ------------------------------------------------------------
# Wireless Cortex AI — Full Professional Version (Chat Sessions + SQL + Charts + Theme)
# ------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# INITIALIZE STATE
# ------------------------------------------------------------
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []  # List of sessions
if "messages" not in st.session_state:
    st.session_state.messages = []  # Current chat
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ------------------------------------------------------------
# THEME SWITCHER
# ------------------------------------------------------------
if st.session_state.theme == "light":
    bg_grad = "linear-gradient(180deg, #f9fbfd 0%, #f0f4f8 100%)"
    header_grad = "linear-gradient(90deg, #004b91, #007acc)"
    text_color = "#000000"
else:
    bg_grad = "linear-gradient(180deg, #1e1e1e 0%, #2c2c2c 100%)"
    header_grad = "linear-gradient(90deg, #111, #222)"
    text_color = "#ffffff"

# ------------------------------------------------------------
# STYLES
# ------------------------------------------------------------
st.markdown(f"""
<style>
.stApp {{
    background: {bg_grad};
    color: {text_color};
    font-family: 'Segoe UI', sans-serif;
}}
header, footer {{visibility: hidden;}}
.chat-bubble-user {{
    background-color: #e8f3ff;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    width: fit-content;
    max-width: 80%;
}}
.chat-bubble-bot {{
    background-color: #ffffff;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    width: fit-content;
    max-width: 80%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("🕘 Chat History")

    # Display saved sessions
    if st.session_state.chat_sessions:
        for i, session in enumerate(reversed(st.session_state.chat_sessions)):
            if st.button(f"💬 Chat {len(st.session_state.chat_sessions)-i} – {session['timestamp']}", use_container_width=True):
                st.session_state.messages = session["messages"].copy()
                st.experimental_rerun()
    else:
        st.caption("No saved chats yet.")

    st.markdown("---")

    # Theme toggle
    if st.button("🌓 Toggle Dark / Light Mode", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.experimental_rerun()

    st.markdown("---")

    # Download chat
    if st.session_state.messages:
        chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("⬇️ Download Current Chat", chat_text, "WirelessCortexChat.txt")
    else:
        st.caption("💡 Ask something to start a chat.")

    st.markdown("---")
    if st.button("🗑️ Start New Chat", use_container_width=True):
        st.session_state.messages = []
        st.experimental_rerun()

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown(f"""
<div style='text-align:center; padding:15px 0; background:{header_grad}; color:white; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.2);'>
  <h1 style='margin-bottom:0;'>📶 Wireless Cortex AI</h1>
  <p style='font-size:16px;'>Your Retail Wireless Data & Forecast Assistant</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
c1.metric("Data Refreshed", "Nov 7, 2025")
c2.metric("Active Data Sources", "4")

st.markdown("---")

# ------------------------------------------------------------
# STATIC KNOWLEDGE BASE
# ------------------------------------------------------------
faq_responses = {
    "sales": "Top-selling devices last month: iPhone 16 (12.3K), Galaxy A15 (10.1K), Moto G Stylus (8.7K). Indirect exceeded forecast by 8%.",
    "inventory": "SKUs low in stock: iPhone 15 Blue (Denver DC), Galaxy A15 (Dallas DC). Average inventory age: 26 days.",
    "shipments": "18,420 units shipped this week. Delays: Marceco (2 days), VIP Wireless (1 day).",
    "pricing": "Average margin: 12.4%. Price drops: Galaxy A15 (-$30), iPhone 15 (-$50) via Best Buy.",
    "forecast": "Forecast accuracy 96.3% in October. iPhone 16 and A15 expected to grow 10-12% MoM."
}

sql_templates = {
    "sales": "SELECT SKU, SUM(Units) AS Total_Units FROM SALES_DATA WHERE DATE BETWEEN '2025-10-01' AND '2025-10-31' GROUP BY SKU ORDER BY Total_Units DESC;",
    "inventory": "SELECT SKU, Location, On_Hand, Days_On_Hand FROM INVENTORY_SNAPSHOT WHERE On_Hand < 500;",
    "shipments": "SELECT DDP, COUNT(SKU) AS Units_Shipped, AVG(Delay_Days) FROM SHIPMENT_LOG WHERE WEEK = '2025-45' GROUP BY DDP;",
    "pricing": "SELECT SKU, MSRP, Promo_Price, Margin_Pct FROM PRICING_TABLE WHERE Channel IN ('Indirect','Retail');",
    "forecast": "SELECT SKU, Forecast_Units, Actual_Units, (Forecast_Units-Actual_Units) AS Variance FROM FORECAST_SUMMARY WHERE PERIOD='2025-Q4';"
}

# ------------------------------------------------------------
# DISPLAY CHAT
# ------------------------------------------------------------
if not st.session_state.messages:
    st.info("💬 Hi! I’m Cortex AI. Ask me about Sales, Inventory, Shipments, Pricing, or Forecasts.")

for msg in st.session_state.messages:
    bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-bot"
    st.markdown(f"<div class='{bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# CHAT INPUT
# ------------------------------------------------------------
if prompt := st.chat_input("Ask your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Intent detection
    topic = None
    for key in faq_responses.keys():
        if key in prompt.lower():
            topic = key
            break

    with st.spinner("Cortex AI is analyzing..."):
        time.sleep(1)

    # Response
    if topic:
        answer = faq_responses[topic]
    else:
        answer = "⚠️ LIMITED DATA — WORKING ON GETTING MORE DATA SOURCES IN."
    st.session_state.messages.append({"role": "bot", "content": answer})
    st.markdown(f"<div class='chat-bubble-bot'>{answer}</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # EXPANDABLE SQL + RESULTS + CHART
    # --------------------------------------------------------
    with st.expander("🧾 View SQL Query"):
        st.code(sql_templates.get(topic, "-- No SQL available for this query."), language="sql")

    # Tabs
    tab1, tab2 = st.tabs(["📋 Results", "📊 Chart"])
    with tab1:
        if topic:
            df = pd.DataFrame({
                "SKU": ["iPhone 16", "Galaxy A15", "Moto G Stylus", "TCL 40 SE"],
                "Units": [12300, 10100, 8700, 7600]
            })
        else:
            df = pd.DataFrame({"Message": ["No data available."]})
        st.dataframe(df, use_container_width=True)

    with tab2:
        chart_type = st.radio("Select Chart Type", ["Bar", "Line", "Pie"], horizontal=True)
        if topic:
            if chart_type == "Bar":
                fig = px.bar(df, x="SKU", y="Units", text="Units", title="Units by SKU")
            elif chart_type == "Line":
                fig = px.line(df, x="SKU", y="Units", markers=True, title="Units by SKU (Line)")
            else:
                fig = px.pie(df, names="SKU", values="Units", title="Units Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No chart available — limited data.")

    # --------------------------------------------------------
    # AUTO-SAVE SESSION
    # --------------------------------------------------------
    st.session_state.chat_sessions.append({
        "timestamp": datetime.now().strftime("%b %d, %I:%M %p"),
        "messages": st.session_state.messages.copy()
    })

    st.experimental_rerun()

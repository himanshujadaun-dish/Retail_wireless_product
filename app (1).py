# ------------------------------------------------------------
# Wireless Cortex AI v5.4 — Persistent Theme + Complete Answers
# ------------------------------------------------------------
# ✅ Dark/Light mode with persistent memory
# ✅ All questions in dropdowns now have answers
# ✅ “Data Limited” message for unknown questions
# ✅ Stable chat + polished UI from v5.3
# ------------------------------------------------------------

import streamlit as st
import time, random, datetime, copy
import pandas as pd
import plotly.express as px
from io import StringIO

# ------------------------------------------------------------
# 1. PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# 2. SESSION STATE INIT (with persistent theme)
# ------------------------------------------------------------
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = st.session_state.get("saved_theme", "light")
if "saved_theme" not in st.session_state:
    st.session_state.saved_theme = st.session_state.theme_mode
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []

# ------------------------------------------------------------
# 3. THEME HANDLING (with persistence)
# ------------------------------------------------------------
def toggle_theme():
    """Switch between dark and light themes"""
    new_theme = "dark" if st.session_state.theme_mode == "light" else "light"
    st.session_state.theme_mode = new_theme
    st.session_state.saved_theme = new_theme

theme = st.session_state.theme_mode

if theme == "dark":
    bg_color = "#0B1221"
    text_color = "#E0E6ED"
    card_color = "#111C33"
    accent_color = "#3C9DF3"
    chat_ai_color = "#1C2B47"
else:
    bg_color = "#F5F7FB"
    text_color = "#000000"
    card_color = "#FFFFFF"
    accent_color = "#007BFF"
    chat_ai_color = "#E6F2FF"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: background-color 0.5s ease, color 0.5s ease;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {accent_color};
    }}
    .chat-bubble-user {{
        background-color: {card_color};
        color: {text_color};
        padding: 10px 14px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }}
    .chat-bubble-ai {{
        background-color: {chat_ai_color};
        color: #E8EEF7;
        padding: 10px 14px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        animation: fadeIn 0.3s ease-in;
    }}
    .stMetric {{
        background: linear-gradient(145deg, {card_color}, {chat_ai_color});
        border-radius: 15px;
        padding: 10px;
        color: {text_color};
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(6px);}}
        to {{opacity: 1; transform: translateY(0);}}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 4. SIDEBAR (same, stable logic)
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")

    st.subheader("💬 Chat History")
    session_keys = list(st.session_state.chat_sessions.keys())
    if session_keys:
        chosen = st.radio("Previous Chats", session_keys, key="chat_radio")
        if st.button("📂 Load Chat", use_container_width=True):
            st.session_state.messages = copy.deepcopy(st.session_state.chat_sessions[chosen])
            st.rerun()
    else:
        st.caption("No previous chats yet.")

    if st.button("🗑️ Start New Chat", use_container_width=True):
        if st.session_state.messages:
            name = f"Chat {len(st.session_state.chat_sessions)+1}"
            st.session_state.chat_sessions[name] = copy.deepcopy(st.session_state.messages)
        st.session_state.messages = []
        st.rerun()

    st.button("🌗 Toggle Dark/Light Mode", on_click=toggle_theme, use_container_width=True)

    st.markdown("---")
    st.subheader("🔗 Info & Tools")
    st.markdown(
        "[📘 Open Info Sheet](https://docs.google.com/spreadsheets/d/1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y/edit?gid=0#gid=0)",
        unsafe_allow_html=True,
    )

    if st.session_state.messages:
        buffer = StringIO()
        for msg in st.session_state.messages:
            role = "USER" if msg["role"] == "user" else "CORTEX"
            buffer.write(f"[{role}] {msg['content']}\n")
        st.download_button(
            label="⬇️ Download Current Chat",
            data=buffer.getvalue(),
            file_name=f"WirelessCortexChat_{datetime.datetime.now():%Y%m%d_%H%M}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.download_button(
            label="⬇️ Download Current Chat",
            data="No chat available yet.",
            file_name="EmptyChat.txt",
            mime="text/plain",
            disabled=True,
            use_container_width=True,
        )

    st.markdown("---")
    st.caption("**Wireless Cortex AI v5.4 | Last Updated Nov 2025**")

# ------------------------------------------------------------
# 5. HEADER + KPI
# ------------------------------------------------------------
st.markdown(
    f"""
    <h1 style='text-align:center;color:{accent_color};'>📶 Wireless Cortex AI</h1>
    <p style='text-align:center;font-size:18px;color:gray;'>Your Retail Intelligence Companion</p>
    """,
    unsafe_allow_html=True,
)
cols = st.columns(4)
with cols[0]:
    st.metric("📈 Forecast Accuracy", f"{random.uniform(88,95):.1f}%")
with cols[1]:
    st.metric("📦 Active SKUs", f"{random.randint(2800,4200):,}")
with cols[2]:
    st.metric("🔋 Total Activations (7d)", f"{random.randint(23000,38000):,}")
with cols[3]:
    sources = ["Sales","Inventory","Shipments","Pricing","Forecast"]
    connected = [f"{s} ✅" if random.random()>0.2 else f"{s} ❌" for s in sources]
    st.selectbox("🌐 Active Data Sources", connected)

# ------------------------------------------------------------
# 6. FAQ QUESTIONS & ANSWERS
# ------------------------------------------------------------
faq = {
    "Sales": {
        "What were the top-selling devices last month?":
            "📊 Top-selling devices were iPhone 16 Pro Max (18%), Samsung A15 (15%), and Moto G Stylus (12%).",
        "Show me sales trends by channel.":
            "📈 Indirect grew 12% MoM, National Retail remained stable, and Web sales increased 8%.",
        "Which SKUs have the highest return rate?":
            "⚠️ Moto G Stylus had the highest return rate at 4.2%, mainly due to screen defects.",
        "Compare iPhone vs Samsung sales this quarter.":
            "📊 iPhone holds 54% market share vs Samsung’s 41%, driven by iPhone 16 launches.",
        "What are the sales forecasts for next month?":
            "🔮 Projected +6% MoM growth in total activations with strong demand for iPhone 16 Pro Max.",
    },
    "Inventory": {
        "Which SKUs are low in stock?":
            "🏭 iPhone 16 128GB and Samsung A15 Blue are under critical threshold in West Coast DCs.",
        "Show inventory aging by warehouse.":
            "⏳ Denver DC: Avg 32 days; Dallas DC: 28 days; NY DC: 21 days — within acceptable limits.",
        "How many iPhone 16 units are in Denver DC?":
            "📦 1,478 iPhone 16 units currently available in Denver DC.",
        "List SKUs with overstock conditions.":
            "⚠️ Overstock: Moto G Power and Samsung A03 (both exceeding 45 days of coverage).",
        "What's the daily inventory update feed?":
            "🕓 Inventory feed updated every 4 hours via Dataiku pipeline ID INV_2025_09.",
    },
    "Shipments": {
        "Show delayed shipments by DDP.":
            "🚚 Marceco and Brightstar delayed 12% of shipments due to weather conditions in midwest.",
        "How many units shipped this week?":
            "📦 18,412 units shipped week-to-date across all channels.",
        "Which SKUs are pending shipment confirmation?":
            "⚙️ 230 SKUs pending confirmation — 60% Apple, 25% Samsung, 15% others.",
        "Track shipment status for iPhone 16 Pro Max.":
            "📍 Last scanned in Dallas, TX — expected delivery in 2 days.",
        "List DDPs with recurring delays.":
            "⏰ Brightstar, Marceco, and Synnex flagged for >5 delay events last quarter.",
    },
    "Pricing": {
        "Show current device pricing by channel.":
            "💰 iPhone 16 Pro Max: $1099 (Web), $1049 (Indirect); Samsung A15: $499 (all channels).",
        "Which SKUs had price drops this week?":
            "📉 Samsung A15 (-$30), Moto G Stylus (-$25), and TCL 40 (-$15).",
        "Compare MSRP vs promo prices.":
            "💵 Avg promo discount: 9.8% below MSRP; Apple discounts remain lowest at 5%.",
        "Show competitor pricing insights.":
            "🏷️ Competitors like Cricket and Metro priced iPhone 15 $20 below Boost MSRP.",
        "What’s the margin for iPhone 16 Pro Max?":
            "💸 Current gross margin: 12.5%, up 1.1% MoM due to reduced freight costs.",
    },
    "Forecast": {
        "Show activation forecast by SKU.":
            "🔮 iPhone 16 Pro Max: 24.3K units forecasted for next month; Samsung A15: 18.9K units.",
        "Compare actual vs forecast for Q3.":
            "📊 Forecast Accuracy: 91.4%; Actuals exceeded forecast in August by 5%.",
        "Which SKUs are forecasted to grow fastest?":
            "🚀 Samsung A15 and Moto G Stylus projected +14% growth next cycle.",
        "Show forecast accuracy trend by month.":
            "📈 Accuracy improved from 86% (July) → 89% (Aug) → 91% (Sep).",
        "Update forecast model inputs from Dataiku.":
            "⚙️ O9 model inputs refreshed automatically via task ‘O9_SKU_FORECAST_LOAD’.",
    },
}

# ------------------------------------------------------------
# 7. QUESTION PICKER
# ------------------------------------------------------------
if not st.session_state.messages:
    st.markdown("### 💬 Choose an option below for suggested questions or ask a question")
    for category, questions in faq.items():
        with st.expander(f"📂 {category}"):
            q = st.selectbox(
                f"Select a {category} question:",
                ["-- Choose --"] + list(questions.keys()),
                key=f"dd_{category}",
            )
            if q != "-- Choose --":
                st.session_state.messages.append({"role": "user", "content": q})
                st.rerun()

# ------------------------------------------------------------
# 8. DISPLAY CHAT
# ------------------------------------------------------------
for msg in st.session_state.messages:
    bubble = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
    st.markdown(f"<div class='{bubble}'>👤 {msg['content']}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 9. CHAT INPUT + LOGIC
# ------------------------------------------------------------
prompt = st.chat_input("Ask about sales, devices, or logistics…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("🤖 Cortex AI is thinking..."):
        time.sleep(1.2)

    # Match user query to known answers
    reply = None
    for cat, qa in faq.items():
        for q, a in qa.items():
            if q.lower() in prompt.lower():
                reply = a
                break

    # Default fallback
    reply = reply or "⚠️ Data Limited — working to get more data sources in"

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # SQL and chart preview
    sql = f"SELECT * FROM demo_table WHERE topic LIKE '%{prompt[:20]}%';"
    df = pd.DataFrame({
        "SKU": ["A15", "A16", "iPhone 16", "Moto G"],
        "Sales": [random.randint(1000, 3000) for _ in range(4)],
        "Forecast": [random.randint(1000, 3000) for _ in range(4)],
    })

    with st.expander("🧮 View SQL Query Used"):
        st.code(sql, language="sql")

    tab1, tab2 = st.tabs(["📊 Results", "📈 Chart"])
    with tab1:
        st.dataframe(df, use_container_width=True)
    with tab2:
        chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Area", "Pie"], key="chart")
        if chart_type == "Bar":
            fig = px.bar(df, x="SKU", y=["Sales", "Forecast"])
        elif chart_type == "Line":
            fig = px.line(df, x="SKU", y=["Sales", "Forecast"])
        elif chart_type == "Scatter":
            fig = px.scatter(df, x="SKU", y="Sales", size="Forecast")
        elif chart_type == "Area":
            fig = px.area(df, x="SKU", y=["Sales", "Forecast"])
        else:
            fig = px.pie(df, names="SKU", values="Sales")
        st.plotly_chart(fig, use_container_width=True)

    fb = st.columns([0.1, 0.1, 0.8])
    with fb[0]:
        if st.button("👍", key=f"up_{len(st.session_state.messages)}"):
            st.session_state.feedback_log.append({"q": prompt, "fb": "up"})
    with fb[1]:
        if st.button("👎", key=f"down_{len(st.session_state.messages)}"):
            st.session_state.feedback_log.append({"q": prompt, "fb": "down"})

    st.rerun()

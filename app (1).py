# ------------------------------------------------------------
# Wireless Cortex AI v5.5 — Stable Runtime Edition
# ------------------------------------------------------------
# ✅ Fix: App no longer freezes or hangs after asking questions
# ✅ Stable rerun logic (no recursive reruns)
# ✅ Feedback buttons safe
# ✅ Persistent theme, full answers, fallback message all intact
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
# 2. SESSION STATE INIT
# ------------------------------------------------------------
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "saved_theme" not in st.session_state:
    st.session_state.saved_theme = st.session_state.theme_mode
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []

# ------------------------------------------------------------
# 3. THEME HANDLING (persistent)
# ------------------------------------------------------------
def toggle_theme():
    new_theme = "dark" if st.session_state.theme_mode == "light" else "light"
    st.session_state.theme_mode = new_theme
    st.session_state.saved_theme = new_theme

theme = st.session_state.theme_mode

# --- Color Palette ---
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
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 4. SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")

    st.subheader("💬 Chat History")
    session_keys = list(st.session_state.chat_sessions.keys())
    if session_keys:
        chosen = st.radio("Previous Chats", session_keys, key="chat_radio")
        if st.button("📂 Load Chat", use_container_width=True):
            st.session_state.messages = copy.deepcopy(st.session_state.chat_sessions[chosen])
            st.session_state.chat_sessions.pop(chosen)
            st.experimental_rerun()
    else:
        st.caption("No previous chats yet.")

    if st.button("🗑️ Start New Chat", use_container_width=True):
        if st.session_state.messages:
            name = f"Chat {len(st.session_state.chat_sessions)+1}"
            st.session_state.chat_sessions[name] = copy.deepcopy(st.session_state.messages)
        st.session_state.messages = []
        st.experimental_rerun()

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
    st.caption("**Wireless Cortex AI v5.5 | Last Updated Nov 2025**")

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
# 6. FAQ DICTIONARY
# ------------------------------------------------------------
faq = {
    "Sales": {
        "Show me sales trends by channel.": "📈 Indirect grew 12% MoM, National Retail stable, Web +8%.",
        "What were the top-selling devices last month?": "📊 iPhone 16 Pro Max (18%), Samsung A15 (15%).",
        "Compare iPhone vs Samsung sales this quarter.": "📊 iPhone holds 54% share vs Samsung 41%.",
        "Which SKUs have the highest return rate?": "⚠️ Moto G Stylus 4.2% due to display issues.",
        "What are the sales forecasts for next month?": "🔮 +6% MoM expected, led by iPhone 16 demand."
    },
    "Inventory": {
        "Which SKUs are low in stock?": "🏭 iPhone 16 128GB, A15 Blue low in West Coast DCs.",
        "Show inventory aging by warehouse.": "⏳ Denver: 32d; Dallas: 28d; NY: 21d.",
        "How many iPhone 16 units are in Denver DC?": "📦 1,478 units available in Denver DC.",
        "List SKUs with overstock conditions.": "⚠️ Moto G Power, Samsung A03 both overstocked.",
        "What's the daily inventory update feed?": "🕓 Updates every 4h via Dataiku INV_2025_09."
    },
    "Shipments": {
        "Show delayed shipments by DDP.": "🚚 Marceco, Brightstar delays due to weather.",
        "How many units shipped this week?": "📦 18,412 units shipped WTD.",
        "Which SKUs are pending shipment confirmation?": "⚙️ 230 pending (60% Apple, 25% Samsung).",
        "Track shipment status for iPhone 16 Pro Max.": "📍 Last scanned: Dallas, TX — ETA 2d.",
        "List DDPs with recurring delays.": "⏰ Brightstar, Marceco flagged >5 times last quarter."
    },
    "Pricing": {
        "Show current device pricing by channel.": "💰 iPhone 16: $1099 (Web), $1049 (Indirect).",
        "Which SKUs had price drops this week?": "📉 A15 (-$30), Moto G Stylus (-$25).",
        "Compare MSRP vs promo prices.": "💵 Avg discount: 9.8% below MSRP; Apple lowest (5%).",
        "Show competitor pricing insights.": "🏷️ Metro priced iPhone 15 $20 below Boost.",
        "What’s the margin for iPhone 16 Pro Max?": "💸 Margin: 12.5%, +1.1% MoM."
    },
    "Forecast": {
        "Show activation forecast by SKU.": "🔮 iPhone 16: 24.3K; Samsung A15: 18.9K next month.",
        "Compare actual vs forecast for Q3.": "📊 Accuracy: 91.4%; August +5% vs forecast.",
        "Which SKUs are forecasted to grow fastest?": "🚀 Samsung A15, Moto G Stylus +14%.",
        "Show forecast accuracy trend by month.": "📈 86% → 89% → 91% (July–Sep).",
        "Update forecast model inputs from Dataiku.": "⚙️ Inputs auto-refreshed via O9_SKU_FORECAST_LOAD."
    }
}

# ------------------------------------------------------------
# 7. QUESTION PICKER (if no chat yet)
# ------------------------------------------------------------
if not st.session_state.messages:
    st.markdown("### 💬 Choose an option below for suggested questions or ask a question")
    for category, qs in faq.items():
        with st.expander(f"📂 {category}"):
            q = st.selectbox(
                f"Select a {category} question:",
                ["-- Choose --"] + list(qs.keys()),
                key=f"dd_{category}",
            )
            if q != "-- Choose --":
                st.session_state.messages.append({"role": "user", "content": q})
                st.experimental_rerun()

# ------------------------------------------------------------
# 8. DISPLAY CHAT
# ------------------------------------------------------------
for msg in st.session_state.messages:
    cls = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
    st.markdown(f"<div class='{cls}'>{'👤' if msg['role']=='user' else '🤖'} {msg['content']}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 9. CHAT INPUT + LOGIC (SAFE)
# ------------------------------------------------------------
prompt = st.chat_input("Ask about sales, devices, or logistics…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("🤖 Cortex AI is thinking..."):
        time.sleep(1.1)

    response = None
    for cat, qs in faq.items():
        for q, a in qs.items():
            if q.lower() in prompt.lower():
                response = a
                break

    if not response:
        response = "⚠️ Data Limited — working to get more data sources in"

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Show SQL + Results + Chart inline
    sql = f"SELECT * FROM demo_table WHERE topic LIKE '%{prompt[:20]}%';"
    df = pd.DataFrame({
        "SKU": ["A15", "A16", "iPhone 16", "Moto G"],
        "Sales": [random.randint(1000, 3000) for _ in range(4)],
        "Forecast": [random.randint(1000, 3000) for _ in range(4)],
    })

    with st.expander("🧮 View SQL Query Used"):
        st.code(sql, language="sql")

    tabs = st.tabs(["📊 Results", "📈 Chart"])
    with tabs[0]:
        st.dataframe(df, use_container_width=True)
    with tabs[1]:
        chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Area", "Pie"])
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
        if st.button("👍", key=f"up_{len(st.session_state.feedback_log)}"):
            st.session_state.feedback_log.append({"q": prompt, "fb": "up", "time": str(datetime.datetime.now())})
    with fb[1]:
        if st.button("👎", key=f"down_{len(st.session_state.feedback_log)}"):
            st.session_state.feedback_log.append({"q": prompt, "fb": "down", "time": str(datetime.datetime.now())})

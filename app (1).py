# ------------------------------------------------------------
# Wireless Cortex AI v5.1 — Plotly Edition
# ------------------------------------------------------------
# Features:
# • Persistent Dark/Light Mode
# • Soft Chat Bubbles + Fade-in Animation
# • Animated “Thinking…” Loader
# • Smart Answers + Fallback
# • KPI Cards + Active Data Sources Dropdown
# • Suggested Question Layer (5 Data Sources)
# • SQL + Plotly Charts (Bar, Line, Scatter, Area, Pie)
# • Thumbs Feedback Logging (mock)
# • Download Chat (.txt)
# • Info Sheet Link (Google)
# • Auto-scroll + Multi-session History
# • App Footer (v5.1 – Nov 2025)
# ------------------------------------------------------------

import streamlit as st
import time, random, datetime
import pandas as pd
import plotly.express as px
from io import StringIO

# ------------------------------------------------------------
# 1. PAGE CONFIG & THEME
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

def toggle_theme():
    st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"

bg_light = "#f5f7fb"
bg_dark = "#121212"
accent_blue = "#007bff"
text_light = "#ffffff"
text_dark = "#000000"

theme_bg = bg_dark if st.session_state.theme_mode == "dark" else bg_light
theme_text = text_light if st.session_state.theme_mode == "dark" else text_dark

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {theme_bg};
        color: {theme_text};
    }}
    .chat-bubble-user {{
        background-color: #ffffff; color:#000; padding:10px 14px;
        border-radius:15px; margin:8px 0; max-width:80%;
    }}
    .chat-bubble-ai {{
        background-color:#e6f2ff; color:#000; padding:10px 14px;
        border-radius:15px; margin:8px 0; max-width:80%;
        animation: fadeIn 0.5s ease-in;
    }}
    @keyframes fadeIn {{
        from {{opacity:0; transform:translateY(5px);}}
        to {{opacity:1; transform:translateY(0);}}
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 2. SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")

    # Chat history
    st.subheader("💬 Chat History")
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
    session_keys = list(st.session_state.chat_sessions.keys())
    if session_keys:
        chosen = st.radio("Previous Chats", session_keys)
        if st.button("📂 Load Chat"):
            st.session_state.messages = st.session_state.chat_sessions[chosen]
            st.experimental_rerun()
    else:
        st.caption("No previous chats yet.")

    if st.button("🗑️ Start New Chat", use_container_width=True):
        if "messages" in st.session_state and st.session_state.messages:
            name = f"Chat {len(st.session_state.chat_sessions)+1}"
            st.session_state.chat_sessions[name] = st.session_state.messages
        st.session_state.messages = []
        st.experimental_rerun()

    if st.button("🌗 Toggle Dark/Light Mode", use_container_width=True):
        toggle_theme()
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("🔗 Info & Tools")
    st.markdown(
        "[📘 Open Info Sheet](https://docs.google.com/spreadsheets/d/1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y/edit?gid=0#gid=0)",
        unsafe_allow_html=True,
    )

    if st.button("⬇️ Download Current Chat", use_container_width=True):
        if "messages" in st.session_state and st.session_state.messages:
            buffer = StringIO()
            for msg in st.session_state.messages:
                role = "USER" if msg["role"] == "user" else "CORTEX"
                buffer.write(f"[{role}] {msg['content']}\n")
            st.download_button(
                label="Save Chat.txt",
                data=buffer.getvalue(),
                file_name=f"WirelessCortexChat_{datetime.datetime.now():%Y%m%d_%H%M}.txt",
                mime="text/plain",
            )
        else:
            st.warning("No chat to download yet.")

    st.markdown("---")
    st.caption("**Wireless Cortex AI v5.1 | Last Updated Nov 2025**")

# ------------------------------------------------------------
# 3. KPI CARDS
# ------------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align:center;color:#007bff;'>📶 Wireless Cortex AI</h1>
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
# 4. SUGGESTED QUESTION LAYER
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []

if not st.session_state.messages:
    st.markdown("### 💬 Choose an option below for suggested questions or ask a question")
    faq = {
        "Sales": [
            "What were the top-selling devices last month?",
            "Show me sales trends by channel.",
            "Which SKUs have the highest return rate?",
            "Compare iPhone vs Samsung sales this quarter.",
            "What are the sales forecasts for next month?",
        ],
        "Inventory": [
            "Which SKUs are low in stock?",
            "Show inventory aging by warehouse.",
            "How many iPhone 16 units are in Denver DC?",
            "List SKUs with overstock conditions.",
            "What's the daily inventory update feed?",
        ],
        "Shipments": [
            "Show delayed shipments by DDP.",
            "How many units shipped this week?",
            "Which SKUs are pending shipment confirmation?",
            "Track shipment status for iPhone 16 Pro Max.",
            "List DDPs with recurring delays.",
        ],
        "Pricing": [
            "Show current device pricing by channel.",
            "Which SKUs had price drops this week?",
            "Compare MSRP vs promo prices.",
            "Show competitor pricing insights.",
            "What’s the margin for iPhone 16 Pro Max?",
        ],
        "Forecast": [
            "Show activation forecast by SKU.",
            "Compare actual vs forecast for Q3.",
            "Which SKUs are forecasted to grow fastest?",
            "Show forecast accuracy trend by month.",
            "Update forecast model inputs from Dataiku.",
        ],
    }
    cols = st.columns(2)
    for i, (cat, qs) in enumerate(faq.items()):
        with cols[i % 2]:
            box_color = "#ffffff" if st.session_state.theme_mode == "light" else "#1e1e1e"
            st.markdown(
                f"<div style='background:{box_color};padding:15px;border-radius:12px;"
                "box-shadow:0 0 8px rgba(0,0,0,0.1);margin-bottom:10px;'>"
                f"<strong>{cat}</strong><br>", unsafe_allow_html=True)
            for j, q in enumerate(qs):
                if st.button(q, key=f"{cat}_{j}", use_container_width=True):
                    st.session_state.messages.append({"role":"user","content":q})
                    st.experimental_rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 5. ANSWERS DATABASE (mock)
# ------------------------------------------------------------
answers = {
    "sales": "📊 Last month’s top devices were iPhone 16 Pro Max and Samsung A15. Sales in Indirect channels rose 12%.",
    "inventory": "🏭 Current stock shows adequate levels except for Denver DC (iPhone 16 low).",
    "shipments": "🚚 Shipments this week: 18,412 units. Delays mainly from DDP Marceco.",
    "pricing": "💰 Recent price drops on Samsung A15 and Moto G Stylus ($20 avg).",
    "forecast": "🔮 Forecast accuracy improved to 91.2% this quarter driven by new O9 inputs.",
}

# ------------------------------------------------------------
# 6. DISPLAY CHAT HISTORY
# ------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 7. CHAT INPUT + RESPONSE LOGIC
# ------------------------------------------------------------
prompt = st.chat_input("Ask about sales, devices, or logistics…")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.spinner("🤖 Cortex AI is thinking …"):
        time.sleep(1.5)
    lower = prompt.lower()
    found = next((answers[k] for k in answers if k in lower), None)
    reply = found or "⚠️ DATA NOT AVAILABLE — WORKING ON GETTING IN MORE DATA SOURCES."
    st.session_state.messages.append({"role":"assistant","content":reply})

    # mock SQL + results + chart
    sql = f"SELECT * FROM demo_table WHERE topic LIKE '%{prompt[:20]}%';"
    df = pd.DataFrame({
        "SKU":["A15","A16","iPhone 16","Moto G"],
        "Sales":[random.randint(1000,3000) for _ in range(4)],
        "Forecast":[random.randint(1000,3000) for _ in range(4)],
    })
    with st.expander("🧮 View SQL Query Used"):
        st.code(sql, language="sql")
    tab1, tab2 = st.tabs(["📊 Results","📈 Chart"])
    with tab1:
        st.dataframe(df, use_container_width=True)
    with tab2:
        chart_type = st.selectbox("Chart Type",["Bar","Line","Scatter","Area","Pie"],key="chart")
        if chart_type=="Bar": fig=px.bar(df,x="SKU",y=["Sales","Forecast"])
        elif chart_type=="Line": fig=px.line(df,x="SKU",y=["Sales","Forecast"])
        elif chart_type=="Scatter": fig=px.scatter(df,x="SKU",y="Sales",size="Forecast")
        elif chart_type=="Area": fig=px.area(df,x="SKU",y=["Sales","Forecast"])
        else: fig=px.pie(df,names="SKU",values="Sales")
        st.plotly_chart(fig,use_container_width=True)

    # feedback buttons
    fb = st.columns([0.1,0.1,0.8])
    with fb[0]:
        if st.button("👍", key=f"up_{len(st.session_state.messages)}"):
            st.session_state.feedback_log.append({"q":prompt,"fb":"up"})
    with fb[1]:
        if st.button("👎", key=f"down_{len(st.session_state.messages)}"):
            st.session_state.feedback_log.append({"q":prompt,"fb":"down"})

    st.experimental_rerun()

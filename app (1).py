# ------------------------------------------------------------
# Wireless Cortex AI — v5.0 (Plotly Edition, Nov 2025)
# ------------------------------------------------------------
# Built for demo: persistent dark/light mode, soft chat bubbles,
# animated loader, realistic answers + fallback, mock feedback logging,
# chat download, SQL + Plotly charts, and professional UI polish.
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
import datetime
from io import StringIO

# ------------------------------------------------------------
# 1. PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# 2. GLOBAL SETTINGS
# ------------------------------------------------------------
INFO_SHEET_URL = "https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/edit"
LOG_SHEET_URL = "https://docs.google.com/spreadsheets/d/1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y/edit"

# Initialize session states
for key, default in {
    "messages": [],
    "chat_sessions": [],
    "feedback_log": [],
    "theme": "light"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ------------------------------------------------------------
# 3. CUSTOM CSS
# ------------------------------------------------------------
def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        body {background-color: #0e1117; color: white;}
        .stApp {background-color: #0e1117;}
        .stChatMessage {background-color: #1e1e1e !important; color: white;}
        .metric-card {background: #1e1e1e; color: white;}
        .category-box {background: #1e1e1e; color: white;}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .metric-card {background: white; color: black;}
        .category-box {background: white; color: black;}
        .chat-bubble-user {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px 15px;
            margin: 5px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .chat-bubble-assistant {
            background-color: #e6f2ff;
            border-radius: 10px;
            padding: 10px 15px;
            margin: 5px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# ------------------------------------------------------------
# 4. SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("🧭 Wireless Cortex AI")

    # Theme toggle
    if st.button("🌓 Toggle Dark / Light Mode", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

    # Chat history
    st.subheader("💬 Chat History")
    for i, session in enumerate(st.session_state.chat_sessions):
        if st.button(f"Chat {i+1} — {session['time']}", key=f"chat_{i}"):
            st.session_state.messages = session["messages"]
            st.experimental_rerun()

    if st.button("➕ Start New Chat", use_container_width=True):
        if st.session_state.messages:
            st.session_state.chat_sessions.append({
                "time": datetime.datetime.now().strftime("%b %d, %I:%M %p"),
                "messages": st.session_state.messages
            })
        st.session_state.messages = []
        st.experimental_rerun()

    # Download chat
    if st.session_state.messages:
        chat_text = "\n".join(
            [f"{'User' if m['role']=='user' else 'Cortex'}: {m['content']}" for m in st.session_state.messages]
        )
        st.download_button(
            "⬇️ Download Current Chat",
            chat_text,
            file_name=f"WirelessCortexAI_Chat_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Info link
    st.markdown("---")
    st.markdown(f"[ℹ️ View Info Sheet]({INFO_SHEET_URL})", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("**App Version:** v5.0  \n**Last Updated:** Nov 2025")

# ------------------------------------------------------------
# 5. HEADER
# ------------------------------------------------------------
st.markdown("""
<div style="background: linear-gradient(90deg, #004aad, #007bff); padding: 20px; border-radius: 10px; text-align: center; color: white;">
    <h1>📶 Wireless Cortex AI</h1>
    <p>Your Retail Wireless Data & Forecast Assistant</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 6. KPI CARDS + ACTIVE DATA SOURCES
# ------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown('<div class="metric-card"><h4>Forecast Accuracy</h4><h2>96.3%</h2></div>', unsafe_allow_html=True)
with k2: st.markdown('<div class="metric-card"><h4>Active SKUs</h4><h2>420</h2></div>', unsafe_allow_html=True)
with k3: st.markdown('<div class="metric-card"><h4>Distribution Channels</h4><h2>4</h2></div>', unsafe_allow_html=True)
with k4: st.markdown('<div class="metric-card"><h4>Delayed Shipments</h4><h2>3</h2></div>', unsafe_allow_html=True)

st.markdown("### ✅ Active Data Sources")
sources = {s: random.choice(["✅ Connected", "❌ Not Connected"]) for s in ["Sales", "Inventory", "Shipments", "Pricing", "Forecast"]}
selected_source = st.selectbox("View connection status:", list(sources.keys()))
st.info(f"{selected_source} Source Status: **{sources[selected_source]}**")

# ------------------------------------------------------------
# 7. ANSWERS DATABASE
# ------------------------------------------------------------
answers = {
    "sales": {
        "top-selling devices": "The top-selling devices last month were iPhone 16 Pro Max, Galaxy S24, and Pixel 8.",
        "sales trends": "Sales trends show a 12% MoM increase, led by strong retail performance in the West region.",
        "compare iphone vs samsung": "iPhone models captured 58% of Q3 unit sales vs Samsung's 35%."
    },
    "inventory": {
        "low in stock": "Low-stock SKUs include iPhone 15 Blue 128GB and Moto G Power 2025.",
        "aging": "Inventory aging averages 47 days, with older batches concentrated in Dallas and Denver DCs."
    },
    "shipments": {
        "delayed": "5 delayed shipments were reported this week, mainly from DDP Marceco.",
        "status": "Shipment status: 95% delivered, 3% in transit, 2% pending confirmation."
    },
    "pricing": {
        "price drops": "Recent price drops: Galaxy A16 (-$40), iPhone 15 (-$75 promo), Moto G Power (-$30).",
        "competitor": "Competitor insights show Apple devices maintaining 7% higher MSRP than Samsung equivalents."
    },
    "forecast": {
        "activation": "Activation forecast projects 15% YoY growth in Q4, with 60K new activations.",
        "accuracy": "Forecast accuracy for October: 94.7%, driven by better DDP alignment and updated O9 models."
    }
}

# ------------------------------------------------------------
# 8. MESSAGE DISPLAY
# ------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-assistant fade-in'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 9. CHAT INPUT + RESPONSE LOGIC
# ------------------------------------------------------------
prompt = st.chat_input("Ask your question here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Animated loader
    with st.spinner("Cortex AI is thinking..."):
        loader = st.empty()
        for i in range(6):
            loader.markdown(f"🤖 Cortex AI is thinking{'.' * (i%3 + 1)}")
            time.sleep(0.3)
        loader.empty()

    # Generate answer
    answer = None
    prompt_lower = prompt.lower()
    for cat, qa in answers.items():
        for k, v in qa.items():
            if k in prompt_lower:
                answer = v
                break
        if answer:
            break
    if not answer:
        answer = "DATA NOT AVAILABLE — WORKING ON GETTING IN MORE DATA SOURCES."

    # Display Cortex response
    st.markdown(f"<div class='chat-bubble-assistant fade-in'>🤖 {answer}</div>", unsafe_allow_html=True)

    # Feedback mock
    fb_cols = st.columns([0.1, 0.1, 0.8])
    with fb_cols[0]:
        if st.button("👍", key=f"up_{len(st.session_state.messages)}"):
            st.session_state.feedback_log.append({"question": prompt, "feedback": "up"})
            st.toast("Thanks for your feedback!", icon="✅")
    with fb_cols[1]:
        if st.button("👎", key=f"down_{len(st.session_state.messages)}"):
            st.session_state.feedback_log.append({"question": prompt, "feedback": "down"})
            st.toast("We'll improve that answer!", icon="⚙️")

    # SQL Query + Results + Chart
    with st.expander("🧮 View SQL Query"):
        query = f"SELECT * FROM DEVICE_SALES WHERE TOPIC LIKE '%{prompt}%' LIMIT 10;"
        st.code(query, language="sql")

    tab1, tab2 = st.tabs(["📋 Results", "📊 Charts"])
    demo_df = pd.DataFrame({
        "Month": ["July", "Aug", "Sept", "Oct", "Nov"],
        "Sales": [random.randint(7000, 9500) for _ in range(5)],
        "Returns": [random.randint(100, 400) for _ in range(5)]
    })

    with tab1:
        st.dataframe(demo_df)

    with tab2:
        chart_type = st.radio("Select chart type:", ["Bar", "Line", "Scatter", "Area", "Pie"], horizontal=True)
        if chart_type == "Bar":
            fig = px.bar(demo_df, x="Month", y="Sales", color="Month", title="Monthly Sales")
        elif chart_type == "Line":
            fig = px.line(demo_df, x="Month", y="Sales", title="Monthly Sales Trend")
        elif chart_type == "Scatter":
            fig = px.scatter(demo_df, x="Month", y="Sales", size="Returns", color="Month", title="Sales vs Returns")
        elif chart_type == "Area":
            fig = px.area(demo_df, x="Month", y="Sales", title="Cumulative Sales")
        else:
            fig = px.pie(demo_df, names="Month", values="Sales", title="Sales Share by Month")
        st.plotly_chart(fig, use_container_width=True)

    # Log assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Auto-scroll
    st.experimental_rerun()

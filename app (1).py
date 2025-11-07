# ------------------------------------------------------------
# Wireless Cortex AI – Streamlit Demo (Public Sheet Mode)
# ------------------------------------------------------------
import streamlit as st
import pandas as pd
import random, time, datetime

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION (must be first)
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# 2. PAGE STYLE
# ------------------------------------------------------------
st.markdown("""
<style>
body {font-family: "Inter", sans-serif;}
.stApp {background-color: #f5f7fb;}
.header-bar {
    background: linear-gradient(90deg, #004aad, #0072ff);
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
.info-btn {
    background-color: #004aad !important;
    color: white !important;
    border-radius: 8px !important;
}
.category-box {
    background: white;
    border-radius: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.1);
    padding: 15px;
    margin-bottom: 15px;
}
.dark-mode {
    background-color: #1e1e1e;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 3. TOP HEADER BAR
# ------------------------------------------------------------
st.markdown("""
<div class='header-bar'>
    <h1>📶 Wireless Cortex AI</h1>
    <p>Your Retail Wireless Data & Forecast Assistant</p>
</div>
""", unsafe_allow_html=True)

# Info button (links to Google Sheet)
st.markdown(
    f"<a href='https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/edit?gid=0#gid=0' target='_blank'>"
    f"<button class='info-btn'>ℹ️ View Info Sheet</button></a>", unsafe_allow_html=True
)

# ------------------------------------------------------------
# 4. QUICK KPI OVERVIEW
# ------------------------------------------------------------
kpi_cols = st.columns(4)
with kpi_cols[0]: st.metric("Forecast Accuracy", "96.3%")
with kpi_cols[1]: st.metric("Active SKUs", "420")
with kpi_cols[2]: st.metric("Distribution Channels", "4")
with kpi_cols[3]: st.metric("Delayed Shipments", "3")

st.markdown("✅ **Active Data Sources:** 5 (Sales, Inventory, Shipments, Pricing, Forecast)")

# ------------------------------------------------------------
# 5. LOAD GOOGLE SHEETS (Public CSV Export Links)
# ------------------------------------------------------------
try:
    logs_url = "https://docs.google.com/spreadsheets/d/1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y/export?format=csv"
    info_url = "https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/export?format=csv"

    logs_df = pd.read_csv(logs_url)
    info_df = pd.read_csv(info_url)
except Exception as e:
    logs_df, info_df = None, None
    st.warning(f"⚠️ Could not load Google Sheets (read-only mode): {e}")

# ------------------------------------------------------------
# 6. DARK/LIGHT MODE TOGGLE
# ------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.sidebar.button("🌓 Toggle Dark / Light Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.experimental_rerun()

if st.session_state.dark_mode:
    st.markdown("<style>.stApp{background-color:#121212;color:white;}</style>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 7. CHAT HISTORY SIDEBAR
# ------------------------------------------------------------
st.sidebar.header("💬 Chat History")
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []

for i, session in enumerate(st.session_state.chat_sessions):
    if st.sidebar.button(f"Chat {i+1} – {session['time']}", key=f"chat_{i}"):
        st.session_state.messages = session["messages"]
        st.experimental_rerun()

if st.sidebar.button("➕ Start New Chat"):
    st.session_state.messages = []
    st.session_state.chat_sessions.append({"time": datetime.datetime.now().strftime("%b %d, %I:%M %p"), "messages": []})
    st.experimental_rerun()

# ------------------------------------------------------------
# 8. INITIALIZE SESSION STATE
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------
# 9. WELCOME MESSAGE AND CATEGORY MENU
# ------------------------------------------------------------
if len(st.session_state.messages) == 0:
    st.info("💡 Hi! I'm Cortex AI. Ask me about Sales, Inventory, Shipments, Pricing, or Forecasts.")
    st.subheader("🧭 Choose an option below for suggested questions or ask a question:")

    faq_categories = {
        "Sales": [
            "What were the top-selling devices last month?",
            "Show me sales trends by channel.",
            "Compare iPhone vs Samsung sales this quarter."
        ],
        "Inventory": [
            "Which SKUs are low in stock?",
            "Show inventory aging by warehouse.",
            "List SKUs with overstock conditions."
        ],
        "Shipments": [
            "Show delayed shipments by DDP.",
            "How many units shipped this week?",
            "Track shipment status for iPhone 16 Pro Max."
        ],
        "Pricing": [
            "Show current device pricing by channel.",
            "Which SKUs had price drops this week?",
            "Compare MSRP vs promo prices."
        ],
        "Forecast": [
            "Show activation forecast by SKU.",
            "Compare actual vs forecast for Q3.",
            "Show forecast accuracy trend by month."
        ]
    }

    cat_cols = st.columns(5)
    for i, (cat, qs) in enumerate(faq_categories.items()):
        with cat_cols[i]:
            with st.expander(f"📊 {cat}"):
                for q in qs:
                    if st.button(q, key=q):
                        st.session_state.messages.append({"role": "user", "content": q})
                        st.experimental_rerun()

# ------------------------------------------------------------
# 10. DISPLAY CHAT HISTORY
# ------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------------------------------
# 11. USER INPUT AND RESPONSE
# ------------------------------------------------------------
prompt = st.chat_input("Ask your question here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simulated response
    with st.chat_message("assistant"):
        with st.spinner("Cortex AI is analyzing data…"):
            time.sleep(1.2)
        response = random.choice([
            "Here’s a quick summary from the latest available dataset.",
            "LIMITED DATA — working on connecting more data sources.",
            "Based on your query, here are the most recent insights.",
        ])
        st.markdown(response)

        # --- Feedback buttons ---
        c1, c2 = st.columns([0.1, 0.9])
        with c1:
            if st.button("👍", key=f"up_{len(st.session_state.messages)}"):
                st.toast("Thanks for the feedback!", icon="✅")
                if logs_df is not None:
                    new_row = {"timestamp": datetime.datetime.now(), "feedback": "up", "question": prompt}
                    logs_df.loc[len(logs_df)] = new_row
        with c2:
            if st.button("👎", key=f"down_{len(st.session_state.messages)}"):
                st.toast("We'll improve that answer!", icon="⚙️")
                if logs_df is not None:
                    new_row = {"timestamp": datetime.datetime.now(), "feedback": "down", "question": prompt}
                    logs_df.loc[len(logs_df)] = new_row

        # --- Show SQL dropdown & result placeholder ---
        with st.expander("🧮 View Example SQL Query"):
            st.code("SELECT DEVICE_FAMILY, SUM(SALES) AS TOTAL FROM SALES_DATA GROUP BY DEVICE_FAMILY;", language="sql")

        tab1, tab2 = st.tabs(["📋 Results", "📊 Chart"])
        with tab1:
            df = pd.DataFrame({
                "Device": ["iPhone 16", "Galaxy S24", "Pixel 8"],
                "Sales": [1200, 950, 620]
            })
            st.dataframe(df)
        with tab2:
            st.bar_chart(df.set_index("Device"))

    st.session_state.messages.append({"role": "assistant", "content": response})

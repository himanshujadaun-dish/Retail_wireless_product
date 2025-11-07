# ------------------------------------------------------------
# Wireless Cortex AI — Final Polished Build (Option 2 + Feedback Logging)
# ------------------------------------------------------------
import streamlit as st
import pandas as pd
import random
import datetime
import urllib.parse
import time

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# 2. CUSTOM CSS FOR BEAUTIFUL UI & DARK MODE
# ------------------------------------------------------------
st.markdown("""
<style>
/* General Styling */
.stApp {
    background-color: var(--background-color);
}
[data-testid="stSidebar"] {
    background: #f8f9fb;
}
[data-theme="dark"] [data-testid="stSidebar"] {
    background: #1E1E1E;
}
h1, h2, h3, h4 {
    color: #003366;
}
.metric-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
[data-theme="dark"] .metric-card {
    background: #222;
    color: white;
}
.feedback-btn {
    border: none;
    background: transparent;
    font-size: 20px;
    cursor: pointer;
}
.feedback-btn:hover {
    transform: scale(1.2);
}
.category-box {
    border-radius: 10px;
    padding: 15px;
    background: white;
    margin: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
[data-theme="dark"] .category-box {
    background: #2d2d2d;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 3. SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("💬 Chat History")
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = []

    if st.session_state.chat_sessions:
        for idx, chat in enumerate(st.session_state.chat_sessions):
            if st.button(f"Chat {idx+1} – {chat['time']}", key=f"chat_{idx}"):
                st.session_state.messages = chat["messages"]
                st.rerun()
    else:
        st.caption("No saved chats yet.")

    if st.button("🌓 Toggle Dark / Light Mode", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.get("theme", "light") == "light" else "light"
        st.rerun()

    if st.button("➕ Start New Chat", use_container_width=True):
        if "messages" in st.session_state:
            st.session_state.chat_sessions.append({
                "time": datetime.datetime.now().strftime("%b %d, %I:%M %p"),
                "messages": st.session_state.messages
            })
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ Resources")
    st.markdown("[📘 View Info Sheet](https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/edit)", unsafe_allow_html=True)

# ------------------------------------------------------------
# 4. HEADER
# ------------------------------------------------------------
st.markdown("""
<div style="background: linear-gradient(90deg, #004aad, #007bff); padding: 20px; border-radius: 10px; text-align: center; color: white;">
    <h1>📶 Wireless Cortex AI</h1>
    <p>Your Retail Wireless Data & Forecast Assistant</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 5. KPI CARDS
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="metric-card"><h4>Forecast Accuracy</h4><h2>96.3%</h2></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><h4>Active SKUs</h4><h2>420</h2></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><h4>Distribution Channels</h4><h2>4</h2></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-card"><h4>Delayed Shipments</h4><h2>3</h2></div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# 6. ACTIVE DATA SOURCES
# ------------------------------------------------------------
st.markdown("✅ **Active Data Sources**")
data_sources = {
    "Sales": random.choice(["✅ Connected", "❌ Not Connected"]),
    "Inventory": random.choice(["✅ Connected", "❌ Not Connected"]),
    "Shipments": random.choice(["✅ Connected", "❌ Not Connected"]),
    "Pricing": random.choice(["✅ Connected", "❌ Not Connected"]),
    "Forecast": random.choice(["✅ Connected", "❌ Not Connected"])
}
selected_source = st.selectbox("View connection status:", list(data_sources.keys()))
st.info(f"{selected_source} Source Status: **{data_sources[selected_source]}**")

# ------------------------------------------------------------
# 7. CHAT STATE INITIALIZATION
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------
# 8. ASSISTANT WELCOME MESSAGE
# ------------------------------------------------------------
if len(st.session_state.messages) == 0:
    st.info("💡 Hi! I'm Cortex AI. Ask me about Sales, Inventory, Shipments, Pricing, or Forecasts.")

# ------------------------------------------------------------
# 9. CATEGORY SUGGESTIONS
# ------------------------------------------------------------
st.markdown("🧭 **Choose an option below for suggested questions or ask a question:**")

faq_categories = {
    "Sales": [
        "What were the top-selling devices last month?",
        "Show me sales trends by channel.",
        "Compare iPhone vs Samsung sales this quarter."
    ],
    "Inventory": [
        "Which SKUs are low in stock?",
        "Show inventory aging by warehouse."
    ],
    "Shipments": [
        "Show delayed shipments by DDP.",
        "Track shipment status for iPhone 16 Pro Max."
    ],
    "Pricing": [
        "Which SKUs had price drops this week?",
        "Show competitor pricing insights."
    ],
    "Forecast": [
        "Show activation forecast by SKU.",
        "Compare actual vs forecast for Q3."
    ]
}

cols = st.columns(5)
for i, (category, questions) in enumerate(faq_categories.items()):
    with cols[i]:
        st.markdown(f"#### {category}")
        q = st.selectbox(f" ", questions, key=f"faq_{category}")
        if st.button(f"Ask about {category}", key=f"ask_{category}"):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# ------------------------------------------------------------
# 10. DISPLAY CHAT HISTORY
# ------------------------------------------------------------
for message in st.session_state.messages:
    role = message["role"]
    if role == "user":
        with st.chat_message("user"):
            st.markdown(f"👤 {message['content']}")
    else:
        with st.chat_message("assistant"):
            st.markdown(f"🤖 {message['content']}")
            st.markdown(
                '<div style="text-align:right;">'
                '<button class="feedback-btn" title="Good answer" id="upvote">👍</button>'
                '<button class="feedback-btn" title="Needs improvement" id="downvote">👎</button>'
                '</div>',
                unsafe_allow_html=True
            )

# ------------------------------------------------------------
# 11. CHAT INPUT
# ------------------------------------------------------------
if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            time.sleep(1)
        if random.random() > 0.5:
            answer = "Here's what I found based on available datasets. 📊"
        else:
            answer = "LIMITED DATA — working on connecting more data sources. 🔄"
        st.markdown(answer)

        sql_query = f"SELECT * FROM sample_table WHERE topic = '{prompt}' LIMIT 10;"
        with st.expander("🧾 View SQL Query"):
            st.code(sql_query, language="sql")

        tab1, tab2 = st.tabs(["Results", "Chart"])
        with tab1:
            df = pd.DataFrame({
                "Month": ["July", "Aug", "Sept", "Oct", "Nov"],
                "Sales": [9000, 7500, 7800, 7900, 8200]
            })
            st.dataframe(df)
        with tab2:
            st.line_chart(df.set_index("Month"))

        # Log feedback to Google Sheet
        try:
            encoded_feedback = urllib.parse.quote(f"{datetime.datetime.now()}, {prompt}, {answer}")
            log_url = "https://docs.google.com/forms/d/e/1FAIpQLSfHnZqjVhVxZT4Xh2q3XvRjsO1k6BtsblHbGvSttWJb/viewform?usp=pp_url&entry.1=" + encoded_feedback
            st.markdown(f"[📝 Log feedback]({log_url})", unsafe_allow_html=True)
        except Exception:
            pass

    st.session_state.messages.append({"role": "assistant", "content": answer})

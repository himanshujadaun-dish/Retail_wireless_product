# ------------------------------------------------------------
# Wireless Cortex AI — Interactive & Enhanced Version
# Combines Visual Polish + Smart Features
# ------------------------------------------------------------
import streamlit as st
import time
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION & BRANDING
# ------------------------------------------------------------
st.set_page_config(
    page_title="Wireless Cortex AI",
    page_icon="📶",
    layout="wide"
)

# ------------------------------------------------------------
# 2. CUSTOM CSS (Visual Enhancements)
# ------------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
    font-family: "Segoe UI", sans-serif;
}
header {visibility: hidden;}
footer {visibility: hidden;}

.category-card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 0 8px rgba(0,0,0,0.1);
    margin-bottom: 15px;
    transition: all 0.2s ease-in-out;
}
.category-card:hover {
    background-color:#f8fbff;
    transform: translateY(-3px);
    box-shadow:0 4px 12px rgba(0,0,0,0.15);
}
.category-title {
    font-weight: 700;
    color: #004b91;
    font-size: 18px;
    margin-bottom: 10px;
}
.stButton>button {
    background-color: #004b91;
    color: white;
    border-radius: 10px;
    border: none;
}
.stButton>button:hover {
    background-color: #ff6600;
    color: white;
}
.metric-card {
    background-color: white;
    border-radius: 10px;
    padding: 8px 12px;
    text-align: center;
    box-shadow: 0 0 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 3. SIDEBAR - SETTINGS
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")

    st.header("👤 Account (Simulated)")
    st.markdown("**Account:** 9001-A-42")
    st.metric("Current Plan", "Unlimited 5G Pro")
    st.metric("Bill Due Date", "Dec 1, 2025")

    st.markdown("---")
    if st.button("🗑️ Start New Conversation", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.header("🤖 Model Settings")
    selected_model = st.selectbox(
        "Select LLM Backend",
        ["Cortex-Optimized-7B (Default)", "GPT-4 Turbo", "Custom RAG Model"]
    )
    temperature = st.slider("Response Focus (Temperature)", 0.0, 1.0, 0.3)

    st.markdown("---")
    st.caption("💡 Tip: Adjust temperature for creativity vs focus balance.")


# ------------------------------------------------------------
# 4. HEADER + DASHBOARD METRICS
# ------------------------------------------------------------
st.markdown("""
<div style='text-align:center; padding:10px 0;'>
  <h1 style='margin-bottom:0;'>📶 Wireless Cortex AI</h1>
  <p style='font-size:16px; color:#555;'>Your Retail Wireless Data & Forecast Assistant</p>
</div>
""", unsafe_allow_html=True)

# Quick Info Tiles (Static placeholders - can later connect to Snowflake)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Data Refreshed", "Nov 6, 2025")
c2.metric("Active Channels", "4")
c3.metric("Total SKUs", "238")
c4.metric("Forecast Window", "Y-8 → Yesterday")

st.markdown("---")

# ------------------------------------------------------------
# 5. SESSION STATE (Chat + Intro)
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:
    with st.chat_message("assistant", avatar="🤖"):
        st.write("Hello! I’m your **Cortex AI Wireless Expert** — ask me about sales, forecasts, inventory, or pricing.")
        st.info("💬 Try selecting a topic below or type your own question.")
    st.session_state.show_intro = False


# ------------------------------------------------------------
# 6. CATEGORY DEFINITIONS
# ------------------------------------------------------------
faq_categories = {
    "🛒 Sales": [
        "What were the top-selling devices last month?",
        "Show me sales trends by channel.",
        "Which SKUs have the highest return rate?",
        "Compare iPhone vs Samsung sales this quarter.",
        "What are the sales forecasts for next month?"
    ],
    "📦 Inventory": [
        "Which SKUs are low in stock?",
        "Show inventory aging by warehouse.",
        "How many iPhone 16 units are in Denver DC?",
        "List SKUs with overstock conditions.",
        "What's the daily inventory update feed?"
    ],
    "🚚 Shipments": [
        "Show delayed shipments by DDP.",
        "How many units shipped this week?",
        "Which SKUs are pending shipment confirmation?",
        "Track shipment status for iPhone 16 Pro Max.",
        "List DDPs with recurring delays."
    ],
    "💲 Pricing": [
        "Show current device pricing by channel.",
        "Which SKUs had price drops this week?",
        "Compare MSRP vs promo prices.",
        "Show competitor pricing insights.",
        "What’s the margin for iPhone 16 Pro Max?"
    ],
    "📈 Forecast": [
        "Show activation forecast by SKU.",
        "Compare actual vs forecast for Q3.",
        "Which SKUs are forecasted to grow fastest?",
        "Show forecast accuracy trend by month.",
        "Update forecast model inputs from Dataiku."
    ]
}

# ------------------------------------------------------------
# 7. DISPLAY CHAT HISTORY
# ------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# ------------------------------------------------------------
# 8. FAQ CATEGORY MENU
# ------------------------------------------------------------
st.markdown("### 💬 Choose a topic or ask a custom question below:")

cols = st.columns(3)
col_map = list(faq_categories.items())

for i, (category, questions) in enumerate(col_map):
    with cols[i % 3]:
        with st.container():
            st.markdown(f"<div class='category-card'><div class='category-title'>{category}</div>", unsafe_allow_html=True)
            for j, q in enumerate(questions):
                if st.button(q, key=f"{category}_{j}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "avatar": "👤", "content": q})
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 9. SUGGESTION BOX
# ------------------------------------------------------------
with st.expander("💡 Try asking these:", expanded=False):
    st.markdown("""
    - Show activations by SKU for last week  
    - Compare forecast vs actuals for Indirect  
    - What are top 5 devices by sales in National Retail?  
    - Display forecast variance by model  
    """)

# ------------------------------------------------------------
# 10. CHAT INPUT + DYNAMIC RESPONSE
# ------------------------------------------------------------
if prompt := st.chat_input("Ask about sales, devices, or logistics…"):
    st.session_state.messages.append({"role": "user", "avatar": "👤", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Simulated "thinking"
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(f"Cortex AI ({selected_model}) is analyzing your question..."):
            for pct in range(0, 101, 10):
                st.progress(pct)
                time.sleep(0.05)

        # Placeholder text response
        response = (
            f"That's a great question! Based on your **{st.session_state.get('plan', 'Unlimited 5G Pro')}** plan, "
            f"I've retrieved insights from the most recent data window."
        )

        # Typing effect
        full_response, placeholder = "", st.empty()
        for word in response.split():
            full_response += word + " "
            placeholder.markdown(full_response + "▌")
            time.sleep(0.02)
        placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "avatar": "🤖", "content": full_response})

        # ------------------------------------------------------------
        # 10A. SMART CHART RESPONSES (based on prompt keywords)
        # ------------------------------------------------------------
        if "top-selling" in prompt.lower() or "sales" in prompt.lower():
            st.markdown("#### 📊 Top Selling Devices")
            df = pd.DataFrame({
                "Device": ["iPhone 16", "Galaxy A15", "Moto G Stylus", "iPhone 15", "TCL 40 XL"],
                "Units": [320, 270, 210, 180, 150]
            })
            fig = px.bar(df, x="Device", y="Units", text="Units", title="Top Selling Devices (Sample Data)")
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        elif "forecast" in prompt.lower():
            st.markdown("#### 📈 Forecast vs Actual (Sample View)")
            df = pd.DataFrame({
                "Date": pd.date_range("2025-10-20", periods=7),
                "Forecast": [300, 310, 320, 315, 330, 340, 335],
                "Actual": [290, 305, 318, 300, 320, 338, 330]
            })
            fig = px.line(df, x="Date", y=["Forecast", "Actual"], markers=True, title="7-Day Forecast vs Actuals")
            st.plotly_chart(fig, use_container_width=True)

        # ------------------------------------------------------------
        # 10B. ACTION BUTTONS
        # ------------------------------------------------------------
        st.markdown("---")
        st.subheader("Next Steps")
        c1, c2, c3 = st.columns(3)
        with c1: st.button("💰 Get Quote", key="quote")
        with c2: st.button("🔗 View Specs", key="specs")
        with c3: st.button("⚙️ Start Upgrade", key="upgrade")

        # ------------------------------------------------------------
        # 10C. EXPORT CHAT OPTION
        # ------------------------------------------------------------
        if st.button("💾 Export Chat to Text", use_container_width=True):
            chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
            st.download_button("⬇️ Download Chat", data=chat_text, file_name="CortexChat.txt")

        # ------------------------------------------------------------
        # 10D. REFERENCES PLACEHOLDER
        # ------------------------------------------------------------
        with st.expander("📚 Sources & References"):
            st.markdown("""
            * **Product Catalog:** iPhone 16 Pro Max Q4-2025.pdf  
            * **Policy:** Upgrade Eligibility Matrix v1.2  
            * **Data Sources:** Snowflake SBX_RWDVCPRTBI & Dataiku Forecast APIs
            """)

# ------------------------------------------------------------
# 11. FUTURE SNOWFLAKE CONNECTION PLACEHOLDER
# ------------------------------------------------------------
@st.cache_resource
def get_snowflake_connection():
    import snowflake.connector
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"]
    )

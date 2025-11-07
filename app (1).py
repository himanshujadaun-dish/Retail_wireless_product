# ------------------------------------------------------------
# Wireless Cortex AI — Advanced Interactive Version
# ------------------------------------------------------------
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import random

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="Wireless Cortex AI",
    page_icon="📶",
    layout="wide"
)

# ------------------------------------------------------------
# CSS STYLING
# ------------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
    font-family: "Segoe UI", sans-serif;
}
header, footer {visibility: hidden;}
.category-card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 0 8px rgba(0,0,0,0.1);
    margin-bottom: 10px;
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
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# SIDEBAR - RECENT HISTORY & SETTINGS
# ------------------------------------------------------------
with st.sidebar:
    st.title("🕘 Recent History")

    # Initialize messages store
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display last 5 user prompts
    recent = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    if recent:
        for r in recent[-5:][::-1]:
            st.markdown(f"• {r}")
    else:
        st.caption("No recent questions yet.")

    st.markdown("---")
    st.header("⚙️ Controls")

    if st.button("🗑️ Start New Conversation", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    if st.button("💾 Export Chat", use_container_width=True):
        if st.session_state.messages:
            chat_text = "\n\n".join(
                [f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages]
            )
            st.download_button("⬇️ Download Chat", data=chat_text, file_name="CortexChat.txt")
        else:
            st.info("No chat yet to export.")

    st.markdown("---")
    st.caption("💡 Tip: Ask anything about Sales, Inventory, Shipments, Pricing, or Forecasts.")

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown("""
<div style='text-align:center; padding:10px 0;'>
  <h1 style='margin-bottom:0;'>📶 Wireless Cortex AI</h1>
  <p style='font-size:16px; color:#555;'>Your Retail Wireless Data & Forecast Assistant</p>
</div>
""", unsafe_allow_html=True)

# Quick Info Tiles
c1, c2 = st.columns(2)
c1.metric("Data Refreshed", "Nov 7, 2025")
c2.metric("Active Data Sources", "4 (Snowflake, Dataiku, Tableau, Box)")

st.markdown("---")

# ------------------------------------------------------------
# INTRODUCTION
# ------------------------------------------------------------
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:
    with st.chat_message("assistant", avatar="🤖"):
        st.write("Hello! I’m **Cortex AI**, your Wireless Data Assistant.")
        st.info("💬 Select a category below or ask your own question to get started.")
    st.session_state.show_intro = False

# ------------------------------------------------------------
# CATEGORY DATA
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
# RANDOM ANSWER DICTIONARY (SIMULATED KNOWLEDGE BASE)
# ------------------------------------------------------------
responses = {
    "top-selling": "The top-selling devices last month were iPhone 16 (12.3K units), Galaxy A15 (10.1K), and Moto G Stylus (8.7K). Indirect performed 8% above forecast.",
    "sales trends": "Sales show upward momentum across National Retail (+5%) while Indirect declined slightly (-2%). Web continues consistent growth.",
    "return rate": "Highest return rates are seen in entry-level models: Galaxy A03 (4.5%) and TCL 40XL (3.8%). Flagship models remain below 1%.",
    "iphone vs samsung": "iPhone captured 57% of total premium sales vs Samsung’s 34%. Upgrade-driven demand boosted iPhone 16 Pro Max.",
    "sales forecast": "The sales forecast for next month is projected at 105K activations, with Indirect contributing 48%, National Retail 38%, and Web 14%.",
    "low in stock": "SKUs low in stock: iPhone 15 Blue 128GB (Denver DC), Galaxy A15 64GB (Dallas DC). Replenishment expected within 3 days.",
    "inventory aging": "Average inventory age is 26 days. Denver DC and Miami DC show the slowest movement for low-tier Androids.",
    "iphone 16 units": "There are 248 iPhone 16 units in Denver DC — 80% ready to ship, 20% pending QA.",
    "overstock": "Overstock SKUs include TCL 40 SE, Moto G Pure, and Galaxy A04. These have >90 days on hand.",
    "inventory update": "Daily inventory updates are published at 7:00 AM MT via the Dataiku pipeline `inventory_feed_v2`.",
    "delayed shipments": "Current delays are seen in Marceco DDP (2 days) and VIP Wireless (1 day). Root cause: carrier capacity.",
    "units shipped": "This week, 18,420 units shipped across all DDPs. Walmart and Best Buy represent 63% of total volume.",
    "pending shipment": "Pending shipment confirmations: 23 SKUs across Marceco and DCI. Expected resolution in next 12 hours.",
    "track shipment": "iPhone 16 Pro Max (DDP Marceco) shows 'In Transit' status, expected delivery ETA: Nov 9.",
    "recurring delays": "Recurring delays observed for DDP: VIP Wireless and Brightstar, primarily due to EDI backlog.",
    "device pricing": "Current prices: iPhone 16 = $999, Galaxy A15 = $199, Moto G Power = $249. Indirect margin avg 8%.",
    "price drops": "Price drops this week: Samsung A14 (-$30), TCL 40 SE (-$20), iPhone 15 (-$50) promo via Best Buy.",
    "msrp": "MSRP vs promo: iPhone 16 ($999 vs $949), Galaxy A15 ($199 vs $179). Web channel leading discounts.",
    "competitor pricing": "Competitor prices show Verizon promoting Galaxy A15 at $169 and Metro offering TCL 40 SE at $129.",
    "margin": "Margin for iPhone 16 Pro Max is currently 12.4%, up from 10.8% last quarter due to reduced freight costs.",
    "activation forecast": "Activation forecast by SKU: iPhone 16 – 32K, A15 – 27K, Moto G Stylus – 20K. Trending +6% MoM.",
    "actual vs forecast": "Q3 variance: Actuals were 3.2% above forecast overall. Web exceeded by 12%, Indirect lagged 4%.",
    "forecasted to grow": "SKUs forecasted to grow fastest: Galaxy A16 (+14%), iPhone 16 Pro Max (+11%), Moto G 2025 (+9%).",
    "accuracy trend": "Forecast accuracy improved to 96.3% in October due to model retraining in Dataiku.",
    "update forecast": "Forecast inputs successfully updated from Dataiku on Nov 6. Next auto-refresh scheduled for Sunday 6 AM."
}

# ------------------------------------------------------------
# DISPLAY CATEGORY ACCORDIONS
# ------------------------------------------------------------
st.markdown("### 💬 Choose a Category:")
for category, questions in faq_categories.items():
    with st.expander(category, expanded=False):
        for q in questions:
            if st.button(q, key=q):
                st.session_state.messages.append({"role": "user", "avatar": "👤", "content": q})
                st.rerun()

# ------------------------------------------------------------
# DISPLAY CHAT HISTORY
# ------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# ------------------------------------------------------------
# CHAT INPUT
# ------------------------------------------------------------
if prompt := st.chat_input("Ask about sales, inventory, shipments, pricing, or forecast..."):
    st.session_state.messages.append({"role": "user", "avatar": "👤", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Simulate "thinking"
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Cortex AI is analyzing your request..."):
            time.sleep(1)

        # Basic keyword detection
        matched = None
        for key, value in responses.items():
            if key in prompt.lower():
                matched = value
                break
        if not matched:
            matched = "Let me look that up — it seems like a custom query. I’ll summarize once I have more data."

        # Display the simulated answer
        st.markdown(matched)
        st.session_state.messages.append({"role": "assistant", "avatar": "🤖", "content": matched})

        # Optional visuals for some categories
        if "sales" in prompt.lower() or "top-selling" in prompt.lower():
            st.markdown("#### 📊 Top Selling Devices (Sample)")
            df = pd.DataFrame({
                "Device": ["iPhone 16", "Galaxy A15", "Moto G Stylus", "TCL 40 XL"],
                "Units": [320, 270, 210, 150]
            })
            fig = px.bar(df, x="Device", y="Units", text="Units", title="Top Selling Devices (Last Month)")
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        elif "forecast" in prompt.lower():
            st.markdown("#### 📈 Forecast vs Actual (Sample)")
            df = pd.DataFrame({
                "Date": pd.date_range("2025-10-25", periods=7),
                "Forecast": [300, 310, 320, 315, 330, 340, 335],
                "Actual": [290, 305, 318, 300, 320, 338, 330]
            })
            fig = px.line(df, x="Date", y=["Forecast", "Actual"], markers=True)
            st.plotly_chart(fig, use_container_width=True)

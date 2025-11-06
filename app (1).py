# ------------------------------------------------------------
# Wireless Cortex AI — Enhanced Streamlit Cloud Version (with Categories & FAQs)
# ------------------------------------------------------------

import streamlit as st
import time

# ------------------------------------------------------------
# 1. PAGE CONFIGURATION & BRANDING
# ------------------------------------------------------------
st.set_page_config(
    page_title="Wireless Cortex AI",
    page_icon="📶",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
.stApp { background-color: #f0f2f6; }
.stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #e6f7ff; border-radius: 15px;
}
.stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
    background-color: #ffffff; border-radius: 15px;
}
.category-card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 0 8px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.category-title {
    font-weight: 700;
    color: #0056b3;
    font-size: 18px;
    margin-bottom: 10px;
}
.faq-button {
    margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# 2. SIDEBAR - CONTEXT AND CONTROLS
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Assistant Context & Tools")

    st.header("👤 User Account (Simulated)")
    st.markdown("### **Account: 9001-A-42**")
    st.metric("Current Plan", "Unlimited 5G Pro")
    st.metric("Bill Due Date", "Dec 1, 2025")
    st.info("💡 Bot uses this info to personalize answers.")

    st.markdown("---")
    if st.button("🗑️ Start New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")

    st.header("🤖 Cortex Settings")
    selected_model = st.selectbox(
        "Select LLM Backend",
        ["Cortex-Optimized-7B (Default)", "GPT-4 Turbo", "Custom RAG Model"]
    )
    temperature = st.slider("Response Focus (Temperature)", 0.0, 1.0, 0.2)


# ------------------------------------------------------------
# 3. MAIN INTERFACE - CHAT WINDOW
# ------------------------------------------------------------
st.title("📶 Retail Wireless Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant", avatar="🤖"):
        st.write("Hello! I'm your **Cortex AI Wireless Expert**.")
        st.write("How can I help you today?")

# Define FAQs for each category
faq_categories = {
    "Sales": [
        "What were the top-selling devices last month?",
        "Show me sales trends by channel.",
        "Which SKUs have the highest return rate?",
        "Compare iPhone vs Samsung sales this quarter.",
        "What are the sales forecasts for next month?"
    ],
    "Inventory": [
        "Which SKUs are low in stock?",
        "Show inventory aging by warehouse.",
        "How many iPhone 16 units are in Denver DC?",
        "List SKUs with overstock conditions.",
        "What's the daily inventory update feed?"
    ],
    "Shipments": [
        "Show delayed shipments by DDP.",
        "How many units shipped this week?",
        "Which SKUs are pending shipment confirmation?",
        "Track shipment status for iPhone 16 Pro Max.",
        "List DDPs with recurring delays."
    ],
    "Pricing": [
        "Show current device pricing by channel.",
        "Which SKUs had price drops this week?",
        "Compare MSRP vs promo prices.",
        "Show competitor pricing insights.",
        "What’s the margin for iPhone 16 Pro Max?"
    ],
    "Forecast": [
        "Show activation forecast by SKU.",
        "Compare actual vs forecast for Q3.",
        "Which SKUs are forecasted to grow fastest?",
        "Show forecast accuracy trend by month.",
        "Update forecast model inputs from Dataiku."
    ]
}


# ------------------------------------------------------------
# Display chat or category menu
# ------------------------------------------------------------
if len(st.session_state.messages) == 0:
    st.markdown("### 💬 Choose a topic below to explore common questions:")

    for category, questions in faq_categories.items():
        with st.container():
            st.markdown(f"<div class='category-card'><div class='category-title'>{category}</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, q in enumerate(questions):
                col = cols[i % 2]
                if col.button(q, key=f"{category}_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "avatar": "👤", "content": q})
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

else:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])

    # --- Chat input ---
    if prompt := st.chat_input("Ask about plans, devices, or your account…"):
        st.session_state.messages.append({"role": "user", "avatar": "👤", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner(f"Cortex AI is consulting the {selected_model} model…"):
                time.sleep(1)

            response = (
                f"That’s a great question! Based on your **{st.session_state.get('plan', 'Unlimited 5G Pro')}** plan, "
                f"I can retrieve the latest details for you shortly."
            )

            # Typing animation
            full_response, placeholder = "", st.empty()
            for word in response.split():
                full_response += word + " "
                placeholder.markdown(full_response + "▌")
                time.sleep(0.04)
            placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "avatar": "🤖", "content": full_response}
            )

            st.markdown("---")
            st.subheader("Next Steps")
            c1, c2, c3 = st.columns(3)
            with c1: st.button("💰 Get Quote", key="quote")
            with c2: st.button("🔗 View Specs", key="specs")
            with c3: st.button("⚙️ Start Upgrade", key="upgrade")

            with st.expander("📚 Sources & References"):
                st.markdown("""
                * **Product Catalog:** iPhone 16 Pro Max Q4-2025.pdf  
                * **Policy:** Upgrade Eligibility Matrix v1.2
                """)

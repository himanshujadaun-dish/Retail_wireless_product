# ------------------------------------------------------------
# Wireless Cortex AI v6.1 — Persistent Memory + 6 KPIs + Info + Starred + Bugfix
# ------------------------------------------------------------
import streamlit as st
import time, random, datetime, copy, json
import pandas as pd
import plotly.express as px
from io import StringIO

# ------------------------------------------------------------
# 0) Safe Rerun Wrapper
# ------------------------------------------------------------
def safe_rerun():
    try:
        st.experimental_rerun()
    except Exception:
        pass

# ------------------------------------------------------------
# Google Sheets Setup
# ------------------------------------------------------------
USE_SHEETS = True
SHEET_URL = "https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/edit#gid=0"

def _get_gspread_client():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        svc = None
        if "gcp_service_account" in st.secrets:
            svc = st.secrets["gcp_service_account"]
        elif "google_service_account_json" in st.secrets:
            svc = json.loads(st.secrets["google_service_account_json"])
        if not svc:
            return None
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(svc, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error setting up Sheets client: {e}")
        return None

def _open_or_create_worksheet(client, sheet_url, tab_name):
    try:
        sh = client.open_by_url(sheet_url)
        try:
            ws = sh.worksheet(tab_name)
        except:
            ws = sh.add_worksheet(title=tab_name, rows="1000", cols="10")
        return ws
    except Exception as e:
        st.error(f"Could not access worksheet: {e}")
        return None

# ------------------------------------------------------------
# 1) PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# 2) SESSION STATE
# ------------------------------------------------------------
defaults = {
    "user_email": "guest_user@corp.com",
    "messages": [],
    "qa_history": [],
    "chat_sessions": {},
    "starred": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------------------------------------------------
# 3) THEME (Fixed Light Mode)
# ------------------------------------------------------------
bg, text, card, accent, ai = "#F5F7FB", "#000000", "#FFFFFF", "#007BFF", "#E6F2FF"

st.markdown(
    f"""
<style>
.stApp {{
    background-color:{bg};
    color:{text};
}}
h1,h2,h3,h4,h5,h6 {{
    color:{accent};
}}
.info-icon {{
    color:{accent};
    text-decoration:none;
    font-size:22px;
}}
.info-icon:hover {{
    cursor:pointer;
    opacity:0.7;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 4) Persistent Memory (Load from Google Sheets)
# ------------------------------------------------------------
def load_user_memory():
    try:
        client = _get_gspread_client()
        if not client:
            return
        ws_chat = _open_or_create_worksheet(client, SHEET_URL, "chat_sessions")
        ws_star = _open_or_create_worksheet(client, SHEET_URL, "starred_questions")

        # Load chat sessions
        rows = ws_chat.get_all_records()
        for row in rows:
            if row.get("user") == st.session_state.user_email:
                st.session_state.chat_sessions[row["session_name"]] = json.loads(row["data"])

        # Load starred
        rows_star = ws_star.get_all_records()
        for row in rows_star:
            if row.get("user") == st.session_state.user_email:
                st.session_state.starred.append({"q": row["question"], "a": row["answer"]})
    except Exception as e:
        st.warning(f"⚠️ Memory load failed: {e}")

def save_user_memory():
    try:
        client = _get_gspread_client()
        if not client:
            return
        ws_chat = _open_or_create_worksheet(client, SHEET_URL, "chat_sessions")
        ws_star = _open_or_create_worksheet(client, SHEET_URL, "starred_questions")

        # Clear user rows first
        data = ws_chat.get_all_records()
        keep = [d for d in data if d.get("user") != st.session_state.user_email]
        ws_chat.clear()
        ws_chat.append_row(["user", "session_name", "data"])
        for row in keep:
            ws_chat.append_row([row["user"], row["session_name"], row["data"]])
        for name, session in st.session_state.chat_sessions.items():
            ws_chat.append_row([
                st.session_state.user_email, name, json.dumps(session)
            ])

        data2 = ws_star.get_all_records()
        keep2 = [d for d in data2 if d.get("user") != st.session_state.user_email]
        ws_star.clear()
        ws_star.append_row(["user", "question", "answer"])
        for row in keep2:
            ws_star.append_row([row["user"], row["question"], row["answer"]])
        for star in st.session_state.starred:
            ws_star.append_row([
                st.session_state.user_email, star["q"], star["a"]
            ])
    except Exception as e:
        st.warning(f"⚠️ Memory save failed: {e}")

load_user_memory()

# ------------------------------------------------------------
# 5) SIDEBAR (Simplified — Memory + Starred)
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")

    st.subheader("💬 Previous Chats")
    session_keys = list(st.session_state.chat_sessions.keys())
    if session_keys:
        chosen = st.selectbox("Select Previous Chat", session_keys, key="chat_radio")
        if chosen:
            saved = st.session_state.chat_sessions[chosen]
            st.session_state.messages = copy.deepcopy(saved.get("messages", []))
            st.session_state.qa_history = copy.deepcopy(saved.get("qa_history", []))
            safe_rerun()
    else:
        st.caption("No previous chats yet.")

    st.markdown("---")
    st.subheader("⭐ Starred Q&As")
    if st.session_state.starred:
        for star in st.session_state.starred:
            st.markdown(f"**{star['q']}**  \n> {star['a']}")
    else:
        st.caption("No starred items yet.")
    st.markdown("---")
    st.caption("**Wireless Cortex AI v6.1 | Persistent + Bugfix**")

# ------------------------------------------------------------
# 6) HEADER + INFO ICON + 6 KPIs
# ------------------------------------------------------------
info_link = (
    "https://docs.google.com/spreadsheets/d/1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y/edit?gid=0#gid=0"
)
col_title, col_info = st.columns([0.92, 0.08])
with col_title:
    st.markdown(
        f"<h1 style='text-align:center;color:{accent};'>📶 Wireless Cortex AI</h1>"
        "<p style='text-align:center;font-size:18px;color:gray;'>Your Retail Intelligence Companion</p>",
        unsafe_allow_html=True,
    )
with col_info:
    st.markdown(
        f"<a href='{info_link}' target='_blank' title='Click for more Information' class='info-icon'>ℹ️</a>",
        unsafe_allow_html=True,
    )

kpi_names = [
    "📈 Forecast Accuracy", "📦 Active SKUs", "🔋 Activations (7d)",
    "💰 Revenue Growth", "📊 Channel Uplift", "📆 Forecast Horizon"
]
kpi_values = [
    f"{random.uniform(88,95):.1f}%", f"{random.randint(2800,4200):,}",
    f"{random.randint(23000,38000):,}", f"{random.uniform(5,12):.1f}%",
    f"{random.uniform(3,9):.1f}%", f"{random.randint(30,90)} days"
]
cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.metric(kpi_names[i], kpi_values[i])

# ------------------------------------------------------------
# 7) Q&A Logic
# ------------------------------------------------------------
def fmt_pct(x): return f"{x:.1f}%"
def fmt_int(a,b): return f"{random.randint(a,b):,}"

def sales_answers(q):
    if "sales trends" in q: return f"📈 Indirect {fmt_pct(random.uniform(8,15))} MoM, Web {fmt_pct(random.uniform(5,12))}."
    if "top-selling devices" in q: return "📊 iPhone 16 Pro Max and Samsung A15 led overall."
    if "compare iphone vs samsung" in q: return "📊 iPhone 55% vs Samsung 40% share."
    if "highest return rate" in q: return "⚠️ Moto G Stylus showing elevated 4.2% return rate."
    if "sales forecasts" in q: return "🔮 +6% MoM expected, mainly from iPhone 16 upgrades."
    return None
def inventory_answers(q):
    if "low in stock" in q: return "🏭 iPhone 16 128GB and A15 Blue are low in West Coast DCs."
    if "inventory aging" in q: return "⏳ Denver 30d, Dallas 26d, NY 20d."
    if "how many iphone 16" in q: return f"📦 {fmt_int(1200,1800)} units."
    if "overstock" in q: return "⚠️ Moto G Power overstocked in Central."
    if "daily inventory" in q: return "🕓 Dataiku job INV_2025_09 every 4 h."
    return None
def shipments_answers(q):
    if "delayed shipments" in q: return "🚚 Brightstar delays in Midwest due to weather."
    if "units shipped" in q: return f"📦 {fmt_int(17000,19000)} units WTD."
    if "pending shipment" in q: return f"⚙️ {fmt_int(180,260)} pending (60% Apple)."
    if "track shipment" in q: return "📍 Dallas TX, ETA 2 days."
    if "recurring delays" in q: return "⏰ Brightstar and Marceco >5× Q3."
    return None
def pricing_answers(q):
    if "device pricing" in q: return "💰 iPhone 16 $1,099 (Web), $1,049 (Indirect)."
    if "price drops" in q: return "📉 A15 (-$30), Moto G (-$25)."
    if "msrp" in q: return "💵 Avg 9% below MSRP."
    if "competitor pricing" in q: return "🏷️ Metro $20 lower on iPhone 15."
    if "margin" in q: return f"💸 Margin ≈ {fmt_pct(random.uniform(11,13))}."
    return None
def forecast_answers(q):
    if "activation forecast" in q: return f"🔮 iPhone 16 {fmt_int(23000,26000)}, A15 {fmt_int(17500,20000)}."
    if "compare actual" in q: return f"📊 Accuracy ≈ {fmt_pct(random.uniform(90,92))}."
    if "forecasted to grow" in q: return "🚀 A15 and Moto G Stylus +15%."
    if "forecast accuracy" in q: return "📈 86% → 89% → 91% (Jul–Sep)."
    if "model inputs" in q: return "⚙️ Inputs refreshed 01:15 AM MT."
    return None
def answer_for_question(q):
    qn=q.strip().lower().rstrip(".!?")
    ans=(sales_answers(qn) or inventory_answers(qn) or shipments_answers(qn)
         or pricing_answers(qn) or forecast_answers(qn))
    return ans if ans else "⚠️ Limited Data — working on getting in more data sources"

FAQ = {
    "Sales": ["Show me sales trends by channel.", "What were the top-selling devices last month.",
              "Compare iPhone vs Samsung sales this quarter.", "Which SKUs have the highest return rate.",
              "What are the sales forecasts for next month."],
    "Inventory": ["Which SKUs are low in stock.", "Show inventory aging by warehouse.",
                  "How many iPhone 16 units are in Denver DC.", "List SKUs with overstock conditions.",
                  "What's the daily inventory update feed."],
    "Shipments": ["Show delayed shipments by DDP.", "How many units shipped this week.",
                  "Which SKUs are pending shipment confirmation.", "Track shipment status for iPhone 16 Pro Max.",
                  "List DDPs with recurring delays."],
    "Pricing": ["Show current device pricing by channel.", "Which SKUs had price drops this week.",
                "Compare MSRP vs promo prices.", "Show competitor pricing insights.",
                "What’s the margin for iPhone 16 Pro Max."],
    "Forecast": ["Show activation forecast by SKU.", "Compare actual vs forecast for Q3.",
                 "Which SKUs are forecasted to grow fastest.", "Show forecast accuracy trend by month.",
                 "Update forecast model inputs from Dataiku."]
}

# ------------------------------------------------------------
# 8) Dropdown Fix — Suggested Questions
# ------------------------------------------------------------
if not st.session_state.messages and not st.session_state.qa_history:
    st.markdown("### 💬 Choose an option below for suggested questions or ask a question")
    for category, questions in FAQ.items():
        with st.expander(f"📂 {category}"):
            sel = st.selectbox(f"Select a {category} question:",
                               ["-- Choose --"] + questions, key=f"dd_{category}")
            if sel != "-- Choose --":
                q_norm = sel.strip().lower().rstrip(".!?")
                a = answer_for_question(q_norm)
                df = pd.DataFrame({
                    "SKU": ["A15", "A16", "iPhone 16", "Moto G"],
                    "Sales": [random.randint(1000, 3000) for _ in range(4)],
                    "Forecast": [random.randint(1000, 3000) for _ in range(4)]
                })
                st.session_state.messages.append({"role": "user", "content": sel})
                st.session_state.qa_history.append({
                    "q": sel, "a": a, "sql": "",
                    "df_dict": df.to_dict(orient="list"),
                    "ts": datetime.datetime.now().isoformat(timespec="seconds"), "fb": None
                })
                name = f"Chat {len(st.session_state.chat_sessions) + 1}"
                st.session_state.chat_sessions[name] = {
                    "messages": copy.deepcopy(st.session_state.messages),
                    "qa_history": copy.deepcopy(st.session_state.qa_history),
                }
                save_user_memory()
                safe_rerun()

# ------------------------------------------------------------
# 9) Render Q&A Blocks + Feedback + Star
# ------------------------------------------------------------
for idx, item in enumerate(st.session_state.qa_history):
    st.markdown(f"**🧠 Question:** {item['q']}")
    st.info(item["a"])
    df = pd.DataFrame(item["df_dict"])
    t1, t2 = st.tabs(["📊 Results", "📈 Chart"])
    with t1:
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ No data available.")
    with t2:
        if not df.empty:
            fig = px.bar(df, x="SKU", y=["Sales", "Forecast"])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ No chart available.")

    c1, c2, c3, _ = st.columns([0.08, 0.08, 0.08, 0.76])
    with c3:
        if st.button("⭐", key=f"star_{idx}"):
            st.session_state.starred.append({"q": item["q"], "a": item["a"]})
            save_user_memory()
            safe_rerun()

# ------------------------------------------------------------
# 10) Chat Input + Auto-Save
# ------------------------------------------------------------
prompt = st.chat_input("Ask about sales, devices, or logistics…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("🤖 Cortex AI is thinking..."):
        time.sleep(1.0)
    a = answer_for_question(prompt)
    df = pd.DataFrame({
        "SKU": ["A15", "A16", "iPhone 16", "Moto G"],
        "Sales": [random.randint(1000, 3000) for _ in range(4)],
        "Forecast": [random.randint(1000, 3000) for _ in range(4)]
    })
    st.session_state.qa_history.append({
        "q": prompt, "a": a, "sql": "",
        "df_dict": df.to_dict(orient="list"),
        "ts": datetime.datetime.now().isoformat(timespec="seconds"), "fb": None
    })
    name = f"Chat {len(st.session_state.chat_sessions) + 1}"
    st.session_state.chat_sessions[name] = {
        "messages": copy.deepcopy(st.session_state.messages),
        "qa_history": copy.deepcopy(st.session_state.qa_history),
    }
    save_user_memory()
    safe_rerun()

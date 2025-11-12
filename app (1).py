# ------------------------------------------------------------
# Wireless Cortex AI v6.4.2 — Boost Orange (Stable & Interactive)
# ------------------------------------------------------------
import streamlit as st
import time, random, datetime, copy, json
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Safe Rerun
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
SHEET_URL = "https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/edit?gid=0"

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
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(svc, scopes=scopes)
        return gspread.authorize(creds)
    except Exception:
        return None

def _open_or_create_worksheet(client, sheet_url, tab_name):
    try:
        sh = client.open_by_url(sheet_url)
        try:
            ws = sh.worksheet(tab_name)
        except:
            ws = sh.add_worksheet(title=tab_name, rows="1000", cols="10")
        return ws
    except Exception:
        return None

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
defaults = {
    "user_email": "guest_user@corp.com",
    "messages": [],
    "qa_history": [],
    "chat_sessions": {},
    "starred": [],
    "last_question": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------------------------------------------------
# THEME (Boost Orange)
# ------------------------------------------------------------
accent = "#FF6600"
bg, text, card, ai = "#F5F7FB", "#000000", "#FFFFFF", "#FFF4EB"

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
.faq-card {{
    background-color:#ffffff;
    border-radius:15px;
    box-shadow:0 2px 5px rgba(0,0,0,0.1);
    padding:15px;
    transition:all 0.2s ease-in-out;
}}
.faq-card:hover {{
    transform:scale(1.03);
    box-shadow:0 4px 12px rgba(255,102,0,0.4);
    border:1px solid {accent};
}}
.star-btn {{
    text-align:right;
    margin-top:-15px;
    margin-bottom:10px;
}}
.sidebar-btn {{
    display:block;
    width:100%;
    border:none;
    background:none;
    color:#FF6600;
    text-align:left;
    font-weight:600;
    cursor:pointer;
}}
.sidebar-btn:hover {{
    color:#000000;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Persistent Memory
# ------------------------------------------------------------
def load_user_memory():
    try:
        client = _get_gspread_client()
        if not client:
            return
        ws_chat = _open_or_create_worksheet(client, SHEET_URL, "chat_sessions")
        ws_star = _open_or_create_worksheet(client, SHEET_URL, "starred_questions")
        for row in ws_chat.get_all_records():
            if row.get("user") == st.session_state.user_email:
                st.session_state.chat_sessions[row["session_name"]] = json.loads(row["data"])
        for row in ws_star.get_all_records():
            if row.get("user") == st.session_state.user_email:
                st.session_state.starred.append({"q": row["question"], "a": row["answer"]})
    except:
        pass

def save_user_memory():
    try:
        client = _get_gspread_client()
        if not client:
            return
        ws_chat = _open_or_create_worksheet(client, SHEET_URL, "chat_sessions")
        ws_star = _open_or_create_worksheet(client, SHEET_URL, "starred_questions")
        ws_chat.clear(); ws_chat.append_row(["user", "session_name", "data"])
        for n, s in st.session_state.chat_sessions.items():
            ws_chat.append_row([st.session_state.user_email, n, json.dumps(s)])
        ws_star.clear(); ws_star.append_row(["user", "question", "answer"])
        for star in st.session_state.starred:
            ws_star.append_row([st.session_state.user_email, star["q"], star["a"]])
    except:
        pass

load_user_memory()

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")
    st.subheader("💬 Previous Chats")
    keys = list(st.session_state.chat_sessions.keys())
    if keys:
        choice = st.selectbox("Select Previous Chat", keys)
        if choice:
            saved = st.session_state.chat_sessions[choice]
            st.session_state.messages = copy.deepcopy(saved["messages"])
            st.session_state.qa_history = copy.deepcopy(saved["qa_history"])
            safe_rerun()
    else:
        st.caption("No previous chats yet.")
    st.markdown("---")

    with st.expander("⭐ Starred Q&As", expanded=False):
        if st.session_state.starred:
            for idx, s in enumerate(st.session_state.starred):
                if st.button(f"{s['q']}", key=f"starred_{idx}", help="Click to view this Q&A"):
                    st.session_state.qa_history.append({
                        "q": s["q"], "a": s["a"],
                        "df_dict": {"SKU": ["A15", "A16", "iPhone 16", "Moto G"],
                                    "Sales": [random.randint(1000, 3000) for _ in range(4)],
                                    "Forecast": [random.randint(1000, 3000) for _ in range(4)]},
                        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
                        "fb": None
                    })
                    safe_rerun()
        else:
            st.caption("No starred items yet.")

    st.markdown("---")
    st.caption("**Wireless Cortex AI v6.4.2 | Boost Orange | Persistent Memory**")

# ------------------------------------------------------------
# HEADER + KPIs
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
    st.markdown(f"<a href='{info_link}' target='_blank' title='Click for more Information' class='info-icon'>ℹ️</a>",
                unsafe_allow_html=True)

cols = st.columns(6)
metrics = [
    ("📈 Forecast Accuracy", f"{random.uniform(88,95):.1f}%"),
    ("📦 Active SKUs", f"{random.randint(2800,4200):,}"),
    ("🔋 Activations (7d)", f"{random.randint(23000,38000):,}"),
    ("💰 Revenue Growth", f"{random.uniform(5,12):.1f}%"),
    ("📊 Channel Uplift", f"{random.uniform(3,9):.1f}%"),
    ("📆 Forecast Horizon", f"{random.randint(30,90)} days")
]
for i, (k, v) in enumerate(metrics):
    with cols[i]:
        st.metric(k, v)

# ------------------------------------------------------------
# FAQ CONFIG
# ------------------------------------------------------------
FAQ = {
    "📊 Sales": ["Show me sales trends by channel.", "Top-selling devices last month.",
                 "Compare iPhone vs Samsung sales.", "Which SKUs have the highest return rate.",
                 "Sales forecast for next month."],
    "🏭 Inventory": ["Which SKUs are low in stock.", "Show inventory aging by warehouse.",
                    "How many iPhone 16 in Denver DC.", "List SKUs with overstock.", "Daily inventory update feed."],
    "🚚 Shipments": ["Show delayed shipments by DDP.", "How many units shipped this week.",
                     "Pending shipment confirmation.", "Track shipment for iPhone 16 Pro Max.", "Recurring delays by DDP."],
    "💰 Pricing": ["Current device pricing by channel.", "Which SKUs had price drops this week.",
                   "Compare MSRP vs promo prices.", "Competitor pricing insights.", "Margin for iPhone 16 Pro Max."],
    "🔮 Forecast": ["Activation forecast by SKU.", "Compare actual vs forecast for Q3.",
                    "Fastest growing SKUs.", "Forecast accuracy trend by month.", "Refresh forecast model inputs."]
}

def answer_for_question(q):
    qn = q.strip().lower()
    if "sales" in qn: return "📈 Sales up 9% MoM — iPhone and Samsung leading."
    if "inventory" in qn: return "🏭 Low stock in Denver DC; healthy in Dallas."
    if "shipment" in qn: return "🚚 Brightstar delays impacting Midwest region."
    if "pricing" in qn: return "💰 Price drops observed for A15 and Moto G."
    if "forecast" in qn: return "🔮 Forecast accuracy improved to 91%."
    return "⚠️ Limited Data — working on getting in more data sources."

# ------------------------------------------------------------
# QUESTION HANDLER
# ------------------------------------------------------------
# ------------------------------------------------------------
# QUESTION HANDLER — no forced rerun
# ------------------------------------------------------------
def process_question(q):
    a = answer_for_question(q)
    df = pd.DataFrame({
        "SKU": ["A15", "A16", "iPhone 16", "Moto G"],
        "Sales": [random.randint(1000, 3000) for _ in range(4)],
        "Forecast": [random.randint(1000, 3000) for _ in range(4)]
    })

    # append the new Q&A
    st.session_state.messages.append({"role": "user", "content": q})
    st.session_state.qa_history.append({
        "q": q,
        "a": a,
        "df_dict": df.to_dict(orient="list"),
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "fb": None
    })

    # update chat memory (no rerun needed)
    name = f"Chat {len(st.session_state.chat_sessions) + 1}"
    st.session_state.chat_sessions[name] = {
        "messages": copy.deepcopy(st.session_state.messages),
        "qa_history": copy.deepcopy(st.session_state.qa_history),
    }
    save_user_memory()


# ------------------------------------------------------------
# Q&A DISPLAY
# ------------------------------------------------------------
for idx, item in enumerate(st.session_state.qa_history):
    cstar, qtext = st.columns([0.1, 0.9])
    with qtext:
        st.markdown(f"**🧠 Question:** {item['q']}")
    with cstar:
        if st.button("⭐", key=f"star_top_{idx}"):
            st.session_state.starred.append({"q": item["q"], "a": item["a"]})
            save_user_memory(); safe_rerun()
    st.info(item["a"])
    df = pd.DataFrame(item["df_dict"])
    t1, t2 = st.tabs(["📊 Results", "📈 Chart"])
    with t1: st.dataframe(df, use_container_width=True)
    with t2: st.plotly_chart(px.bar(df, x="SKU", y=["Sales", "Forecast"]), use_container_width=True)
    c1, c2, _ = st.columns([0.1, 0.1, 0.8])
    with c1:
        if st.button("👍", key=f"up_{idx}", disabled=item["fb"] == "up"):
            item["fb"] = "up"; save_user_memory(); safe_rerun()
    with c2:
        if st.button("👎", key=f"down_{idx}", disabled=item["fb"] == "down"):
            item["fb"] = "down"; save_user_memory(); safe_rerun()

# ------------------------------------------------------------
# CHAT INPUT
# ------------------------------------------------------------
prompt = st.chat_input("Ask about sales, devices, or logistics…")
if prompt:
    process_question(prompt)

# ------------------------------------------------------------
# ALWAYS SHOW FAQ — instant answer + auto-reset (v6.4.5)
# ------------------------------------------------------------
st.markdown(
    f"### <span style='color:{accent};'>💬 Select a question from dropdown or ask a question in the chat below.</span>",
    unsafe_allow_html=True
)

# Callback that fires immediately when a dropdown value changes
def on_faq_change(key):
    sel = st.session_state.get(key)
    if sel and sel != "-- Choose --":
        process_question(sel)
        # reset the dropdown back to default AFTER processing
        st.session_state[key] = "-- Choose --"

categories = list(FAQ.keys())
cols = st.columns(len(categories))

for i, cat in enumerate(categories):
    with cols[i]:
        st.markdown(f"<div class='faq-card'><b>{cat}</b>", unsafe_allow_html=True)
        st.selectbox(
            "",
            ["-- Choose --"] + FAQ[cat],
            key=f"faq_{cat}",                  # stable key per category
            on_change=on_faq_change,
            args=(f"faq_{cat}",),              # pass the key to callback
        )
        st.markdown("</div>", unsafe_allow_html=True)

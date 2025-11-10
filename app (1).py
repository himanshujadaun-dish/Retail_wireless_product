# ------------------------------------------------------------
# Wireless Cortex AI v5.6.1 — Stable Streamlit 1.39+ Fix
# ------------------------------------------------------------

import streamlit as st
import time, random, datetime, copy
import pandas as pd
import plotly.express as px
from io import StringIO

# ------------------------------------------------------------
# 0) Safe Rerun Wrapper (Fix for Streamlit 1.39+)
# ------------------------------------------------------------
def safe_rerun():
    """Safely rerun app without breaking runtime (replaces experimental_rerun)."""
    try:
        st.rerun()
    except Exception:
        pass

# Optional Google Sheet logging
USE_SHEETS = True

# ------------------------------------------------------------
# Google Sheets helpers (same as before)
# ------------------------------------------------------------
def _get_gspread_client():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        svc = None
        if "gcp_service_account" in st.secrets:
            svc = st.secrets["gcp_service_account"]
        elif "google_service_account_json" in st.secrets:
            import json
            svc = json.loads(st.secrets["google_service_account_json"])
        if not svc:
            return None
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(svc, scopes=scopes)
        return gspread.authorize(creds)
    except Exception:
        return None


def log_feedback_to_sheet(sheet_url: str, row: list):
    if not USE_SHEETS:
        return False
    try:
        client = _get_gspread_client()
        if not client:
            return False
        sh = client.open_by_url(sheet_url)
        ws = sh.sheet1
        ws.append_row(row, value_input_option="USER_ENTERED")
        return True
    except Exception:
        return False


# ------------------------------------------------------------
# 1) PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI", page_icon="📶", layout="wide")

# ------------------------------------------------------------
# 2) SESSION STATE
# ------------------------------------------------------------
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

if "local_feedback_cache" not in st.session_state:
    st.session_state.local_feedback_cache = []


# ------------------------------------------------------------
# 3) THEME
# ------------------------------------------------------------
def toggle_theme():
    st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"

theme = st.session_state.theme_mode

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
    .stApp {{ background-color:{bg_color}; color:{text_color}; }}
    h1, h2, h3, h4, h5, h6 {{ color:{accent_color}; }}
    .chat-bubble-user {{
        background-color:{card_color}; color:{text_color};
        padding:10px 14px; border-radius:15px; margin:8px 0; max-width:80%;
        box-shadow:0 2px 6px rgba(0,0,0,.25);
    }}
    .chat-bubble-ai {{
        background-color:{chat_ai_color}; color:#E8EEF7;
        padding:10px 14px; border-radius:15px; margin:8px 0; max-width:80%;
        box-shadow:0 2px 6px rgba(0,0,0,.15);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 4) SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")

    st.subheader("💬 Chat History")
    session_keys = list(st.session_state.chat_sessions.keys())
    if session_keys:
        chosen = st.radio("Previous Chats", session_keys, key="chat_radio")
        if st.button("📂 Load Chat", use_container_width=True):
            saved = st.session_state.chat_sessions.pop(chosen)
            st.session_state.messages = saved.get("messages", [])
            st.session_state.qa_history = saved.get("qa_history", [])
            safe_rerun()
    else:
        st.caption("No previous chats yet.")

    if st.button("🗑️ Start New Chat", use_container_width=True):
        if st.session_state.messages or st.session_state.qa_history:
            name = f"Chat {len(st.session_state.chat_sessions)+1}"
            st.session_state.chat_sessions[name] = {
                "messages": copy.deepcopy(st.session_state.messages),
                "qa_history": copy.deepcopy(st.session_state.qa_history),
            }
        st.session_state.messages = []
        st.session_state.qa_history = []
        safe_rerun()

    if st.button("🌗 Toggle Dark/Light Mode", use_container_width=True):
        toggle_theme()
        safe_rerun()

    st.markdown("---")
    st.subheader("🔗 Info & Tools")
    st.markdown(
        "[📘 Open Info Sheet](https://docs.google.com/spreadsheets/d/1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y/edit?gid=0#gid=0)",
        unsafe_allow_html=True,
    )

    # Download chat log
    if st.session_state.messages or st.session_state.qa_history:
        buf = StringIO()
        for m in st.session_state.messages:
            role = "USER" if m["role"] == "user" else "CORTEX"
            buf.write(f"[{role}] {m['content']}\n")
        for block in st.session_state.qa_history:
            buf.write(f"[USER] {block['q']}\n")
            buf.write(f"[CORTEX] {block['a']}\n\n")
        st.download_button("⬇️ Download Current Chat", buf.getvalue(),
                           file_name=f"WirelessCortexChat_{datetime.datetime.now():%Y%m%d_%H%M}.txt",
                           mime="text/plain", use_container_width=True)
    else:
        st.download_button("⬇️ Download Current Chat", "No chat available yet.",
                           file_name="EmptyChat.txt", mime="text/plain",
                           disabled=True, use_container_width=True)

    if st.session_state.local_feedback_cache:
        df_fb = pd.DataFrame(st.session_state.local_feedback_cache,
                             columns=["timestamp","question","answer_preview","sentiment"])
        st.markdown("⚠️ Couldn’t reach Google Sheets. You can download cached feedback:")
        st.download_button("Download Feedback CSV", df_fb.to_csv(index=False),
                           file_name="cortex_feedback_cache.csv", mime="text/csv",
                           use_container_width=True)

    st.markdown("---")
    st.caption("**Wireless Cortex AI v5.6.1 | Stable Streamlit Fix**")

# ------------------------------------------------------------
# 5) HEADER + KPIs
# ------------------------------------------------------------
st.markdown(
    f"""
    <h1 style='text-align:center;color:{accent_color};'>📶 Wireless Cortex AI</h1>
    <p style='text-align:center;font-size:18px;color:gray;'>Your Retail Intelligence Companion</p>
    """,
    unsafe_allow_html=True,
)
k = st.columns(4)
with k[0]:
    st.metric("📈 Forecast Accuracy", f"{random.uniform(88,95):.1f}%")
with k[1]:
    st.metric("📦 Active SKUs", f"{random.randint(2800,4200):,}")
with k[2]:
    st.metric("🔋 Total Activations (7d)", f"{random.randint(23000,38000):,}")
with k[3]:
    sources = ["Sales","Inventory","Shipments","Pricing","Forecast"]
    connected = [f"{s} ✅" if random.random()>0.2 else f"{s} ❌" for s in sources]
    st.selectbox("🌐 Active Data Sources", connected)

# ------------------------------------------------------------
# 6) Prewritten question answers (unchanged)
# ------------------------------------------------------------
def fmt_pct(x):  return f"{x:.1f}%"
def fmt_int(a,b): return f"{random.randint(a,b):,}"

def sales_answers(q):
    if q == "Show me sales trends by channel.":
        return f"📈 Indirect {fmt_pct(random.uniform(8,15))} MoM, National Retail {fmt_pct(random.uniform(-2,2))}, Web {fmt_pct(random.uniform(5,12))}."
    if q == "What were the top-selling devices last month?":
        return f"📊 iPhone 16 Pro Max ({fmt_pct(random.uniform(16,20))}), Samsung A15 ({fmt_pct(random.uniform(13,17))})."
    if q == "Compare iPhone vs Samsung sales this quarter.":
        return f"📊 Share: iPhone {fmt_pct(random.uniform(52,56))} vs Samsung {fmt_pct(random.uniform(39,43))}."
    if q == "Which SKUs have the highest return rate?":
        return f"⚠️ Moto G Stylus {fmt_pct(random.uniform(3.6,4.8))} (display issues trending)."
    if q == "What are the sales forecasts for next month?":
        return f"🔮 Overall +{fmt_pct(random.uniform(4,7))} MoM, led by iPhone 16 upgrades."
    return None

def inventory_answers(q):
    if q == "Which SKUs are low in stock?":
        return "🏭 iPhone 16 128GB and Samsung A15 Blue are low in West Coast DCs."
    if q == "Show inventory aging by warehouse.":
        return f"⏳ Denver: {random.randint(28,35)}d; Dallas: {random.randint(24,30)}d; New York: {random.randint(18,24)}d."
    if q == "How many iPhone 16 units are in Denver DC?":
        return f"📦 {fmt_int(1200, 1800)} units in Denver DC."
    if q == "List SKUs with overstock conditions.":
        return "⚠️ Moto G Power and Samsung A03 are overstocked across Central region."
    if q == "What's the daily inventory update feed?":
        return "🕓 Every 4 hours via Dataiku job INV_2025_09; final daily snapshot at 1:05 AM MT."
    return None

def shipments_answers(q):
    if q == "Show delayed shipments by DDP.":
        return "🚚 Marceco and Brightstar show delays due to weather in the Midwest."
    if q == "How many units shipped this week?":
        return f"📦 {fmt_int(17000, 19000)} units WTD."
    if q == "Which SKUs are pending shipment confirmation?":
        return f"⚙️ {fmt_int(180, 260)} pending confirmations (≈60% Apple, 25% Samsung)."
    if q == "Track shipment status for iPhone 16 Pro Max.":
        return "📍 Last scan: Dallas, TX — ETA 1–2 days."
    if q == "List DDPs with recurring delays.":
        return "⏰ Brightstar and Marceco flagged >5x last quarter."
    return None

def pricing_answers(q):
    if q == "Show current device pricing by channel.":
        return "💰 iPhone 16: $1,099 (Web), $1,049 (Indirect)."
    if q == "Which SKUs had price drops this week?":
        return "📉 A15 (-$30) and Moto G Stylus (-$25) adjusted this week."
    if q == "Compare MSRP vs promo prices.":
        return "💵 Avg discount 9–11% below MSRP; Apple lowest discount (≈5%)."
    if q == "Show competitor pricing insights.":
        return "🏷️ Metro is $20 under Boost on iPhone 15; A15 parity."
    if q == "What’s the margin for iPhone 16 Pro Max?":
        return f"💸 Margin ≈ {fmt_pct(random.uniform(11.5,13.5))}."
    return None

def forecast_answers(q):
    if q == "Show activation forecast by SKU.":
        return f"🔮 iPhone 16: {fmt_int(23000,26000)}; Samsung A15: {fmt_int(17500,20000)} next month."
    if q == "Compare actual vs forecast for Q3.":
        return f"📊 Accuracy ≈ {fmt_pct(random.uniform(90.5,92.5))}; August was +{fmt_pct(random.uniform(3,6))} vs forecast."
    if q == "Which SKUs are forecasted to grow fastest?":
        return f"🚀 Samsung A15 and Moto G Stylus (+{fmt_pct(random.uniform(12,16))})."
    if q == "Show forecast accuracy trend by month.":
        a,b,c=[fmt_pct(x) for x in [random.uniform(85,88),random.uniform(88,90),random.uniform(90,92)]]
        return f"📈 {a} → {b} → {c} (Jul–Sep)."
    if q == "Update forecast model inputs from Dataiku.":
        return "⚙️ Inputs refreshed via O9_SKU_FORECAST_LOAD; last run 01:15 AM MT."
    return None

def answer_for_question(q):
    a=(sales_answers(q) or inventory_answers(q) or shipments_answers(q) or pricing_answers(q) or forecast_answers(q))
    if a: return a
    return "⚠️ Limited Data — working on getting in more data sources"

# ------------------------------------------------------------
# 7–10) Render logic (unchanged except safe_rerun replacements)
# ------------------------------------------------------------
if not st.session_state.messages and not st.session_state.qa_history:
    st.markdown("### 💬 Choose an option below for suggested questions or ask a question")
    for category, questions in {
        "Sales": sales_answers, "Inventory": inventory_answers,
        "Shipments": shipments_answers, "Pricing": pricing_answers,
        "Forecast": forecast_answers,
    }.items():
        with st.expander(f"📂 {category}"):
            sel = st.selectbox(f"Select a {category} question:",
                               ["-- Choose --"] + list(FAQ[category]), key=f"dd_{category}")
            if sel != "-- Choose --":
                st.session_state.messages.append({"role": "user", "content": sel})
                a = answer_for_question(sel)
                sql = f"SELECT * FROM demo_table WHERE topic = '{sel[:60]}';"
                df = pd.DataFrame({
                    "SKU":["A15","A16","iPhone 16","Moto G"],
                    "Sales":[random.randint(1000,3000) for _ in range(4)],
                    "Forecast":[random.randint(1000,3000) for _ in range(4)],
                })
                st.session_state.qa_history.append({
                    "q":sel,"a":a,"sql":sql,
                    "df_dict":df.to_dict(orient="list"),
                    "ts":datetime.datetime.now().isoformat(timespec="seconds"),
                    "fb":None
                })
                safe_rerun()

# Render existing Q&A
SHEET_URL="https://docs.google.com/spreadsheets/d/1aRawuCX4_dNja96WdLHxEsZ8J6yPHqM4xEPA-f26wOE/edit?gid=0#gid=0"
for idx, block in enumerate(st.session_state.qa_history):
    st.markdown(f"<div class='chat-bubble-user'>👤 {block['q']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble-ai'>🤖 {block['a']}</div>", unsafe_allow_html=True)
    with st.expander("🧮 View SQL Query Used"):
        st.code(block["sql"], language="sql")
    df=pd.DataFrame(block["df_dict"])
    t1,t2=st.tabs(["📊 Results","📈 Chart"])
    with t1: st.dataframe(df, use_container_width=True)
    with t2:
        chart=st.selectbox("Chart Type",["Bar","Line","Scatter","Area","Pie"],key=f"chart_{idx}")
        if chart=="Bar": fig=px.bar(df,x="SKU",y=["Sales","Forecast"])
        elif chart=="Line": fig=px.line(df,x="SKU",y=["Sales","Forecast"])
        elif chart=="Scatter": fig=px.scatter(df,x="SKU",y="Sales",size="Forecast")
        elif chart=="Area": fig=px.area(df,x="SKU",y=["Sales","Forecast"])
        else: fig=px.pie(df,names="SKU",values="Sales")
        st.plotly_chart(fig,use_container_width=True)
    c1,c2,_=st.columns([0.08,0.08,0.84])
    with c1:
        if st.button("👍",key=f"up_{idx}",disabled=(block["fb"]=="up")):
            block["fb"]="up"
            ok=log_feedback_to_sheet(SHEET_URL,[datetime.datetime.now().isoformat(timespec="seconds"),block["q"],block["a"][:120],"up"])
            if not ok: st.session_state.local_feedback_cache.append([datetime.datetime.now().isoformat(timespec="seconds"),block["q"],block["a"][:120],"up"])
            safe_rerun()
    with c2:
        if st.button("👎",key=f"down_{idx}",disabled=(block["fb"]=="down")):
            block["fb"]="down"
            ok=log_feedback_to_sheet(SHEET_URL,[datetime.datetime.now().isoformat(timespec="seconds"),block["q"],block["a"][:120],"down"])
            if not ok: st.session_state.local_feedback_cache.append([datetime.datetime.now().isoformat(timespec="seconds"),block["q"],block["a"][:120],"down"])
            safe_rerun()

prompt=st.chat_input("Ask about sales, devices, or logistics…")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.spinner("🤖 Cortex AI is thinking..."): time.sleep(1)
    a=answer_for_question(prompt)
    sql=f"SELECT * FROM demo_table WHERE topic='{prompt[:60]}';"
    df=pd.DataFrame({"SKU":["A15","A16","iPhone 16","Moto G"],"Sales":[random.randint(1000,3000) for _ in range(4)],"Forecast":[random.randint(1000,3000) for _ in range(4)]})
    st.session_state.qa_history.append({"q":prompt,"a":a,"sql":sql,"df_dict":df.to_dict(orient="list"),"ts":datetime.datetime.now().isoformat(timespec="seconds"),"fb":None})
    safe_rerun()

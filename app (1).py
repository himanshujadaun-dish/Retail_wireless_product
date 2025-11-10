# ------------------------------------------------------------
# Wireless Cortex AI v5.6.3 — Based on v5.6.2 (Dropdown Fix Only)
# ------------------------------------------------------------
import streamlit as st
import time, random, datetime, copy
import pandas as pd
import plotly.express as px
from io import StringIO

# ------------------------------------------------------------
# 0) Safe Rerun Wrapper
# ------------------------------------------------------------
def safe_rerun():
    try:
        st.rerun()
    except Exception:
        pass

# ------------------------------------------------------------
# Google Sheets Logging (unchanged)
# ------------------------------------------------------------
USE_SHEETS = True
def _get_gspread_client():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        svc=None
        if "gcp_service_account" in st.secrets: svc=st.secrets["gcp_service_account"]
        elif "google_service_account_json" in st.secrets:
            import json; svc=json.loads(st.secrets["google_service_account_json"])
        if not svc: return None
        scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
        creds=Credentials.from_service_account_info(svc,scopes=scopes)
        return gspread.authorize(creds)
    except Exception:
        return None

def log_feedback_to_sheet(sheet_url,row):
    if not USE_SHEETS: return False
    try:
        client=_get_gspread_client()
        if not client: return False
        sh=client.open_by_url(sheet_url)
        ws=sh.sheet1
        ws.append_row(row,value_input_option="USER_ENTERED")
        return True
    except Exception: return False

# ------------------------------------------------------------
# 1) PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wireless Cortex AI",page_icon="📶",layout="wide")

# ------------------------------------------------------------
# 2) SESSION STATE
# ------------------------------------------------------------
defaults={
    "theme_mode":"light",
    "messages":[],
    "qa_history":[],
    "chat_sessions":{},
    "local_feedback_cache":[]
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k]=v

# ------------------------------------------------------------
# 3) THEME SETUP
# ------------------------------------------------------------
def toggle_theme():
    st.session_state.theme_mode = "dark" if st.session_state.theme_mode=="light" else "light"

theme=st.session_state.theme_mode
if theme=="dark":
    bg,text,card,accent,ai="#0B1221","#E0E6ED","#111C33","#3C9DF3","#1C2B47"
else:
    bg,text,card,accent,ai="#F5F7FB","#000000","#FFFFFF","#007BFF","#E6F2FF"

st.markdown(f"""
<style>
.stApp {{background-color:{bg};color:{text};}}
h1,h2,h3,h4,h5,h6{{color:{accent};}}
.chat-bubble-user{{background-color:{card};color:{text};padding:10px 14px;border-radius:15px;margin:8px 0;max-width:80%;box-shadow:0 2px 6px rgba(0,0,0,.25);}}
.chat-bubble-ai{{background-color:{ai};color:#E8EEF7;padding:10px 14px;border-radius:15px;margin:8px 0;max-width:80%;box-shadow:0 2px 6px rgba(0,0,0,.15);}}
</style>
""",unsafe_allow_html=True)

# ------------------------------------------------------------
# 4) SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Cortex Controls")
    st.subheader("💬 Chat History")
    session_keys=list(st.session_state.chat_sessions.keys())
    if session_keys:
        chosen=st.radio("Previous Chats",session_keys,key="chat_radio")
        if st.button("📂 Load Chat",use_container_width=True):
            saved=st.session_state.chat_sessions.pop(chosen)
            st.session_state.messages=saved.get("messages",[])
            st.session_state.qa_history=saved.get("qa_history",[])
            safe_rerun()
    else: st.caption("No previous chats yet.")
    if st.button("🗑️ Start New Chat",use_container_width=True):
        if st.session_state.messages or st.session_state.qa_history:
            name=f"Chat {len(st.session_state.chat_sessions)+1}"
            st.session_state.chat_sessions[name]={"messages":copy.deepcopy(st.session_state.messages),
                                                  "qa_history":copy.deepcopy(st.session_state.qa_history)}
        st.session_state.messages=[]; st.session_state.qa_history=[]
        safe_rerun()
    if st.button("🌗 Toggle Dark/Light Mode",use_container_width=True):
        toggle_theme(); safe_rerun()

    st.markdown("---")
    st.subheader("🔗 Info & Tools")
    st.markdown("[📘 Open Info Sheet](https://docs.google.com/spreadsheets/d/1p0srBF_lMOAlVv-fVOgWqw1M2y8KG3zb7oQj_sAb42Y/edit?gid=0#gid=0)",unsafe_allow_html=True)
    st.markdown("---")
    st.caption("**Wireless Cortex AI v5.6.3 | Stable Fix (Dropdown)**")

# ------------------------------------------------------------
# 5) HEADER + KPIs
# ------------------------------------------------------------
st.markdown(f"""
<h1 style='text-align:center;color:{accent};'>📶 Wireless Cortex AI</h1>
<p style='text-align:center;font-size:18px;color:gray;'>Your Retail Intelligence Companion</p>
""",unsafe_allow_html=True)
cols=st.columns(4)
with cols[0]: st.metric("📈 Forecast Accuracy",f"{random.uniform(88,95):.1f}%")
with cols[1]: st.metric("📦 Active SKUs",f"{random.randint(2800,4200):,}")
with cols[2]: st.metric("🔋 Total Activations (7d)",f"{random.randint(23000,38000):,}")
with cols[3]:
    sources=["Sales","Inventory","Shipments","Pricing","Forecast"]
    connected=[f"{s} ✅" if random.random()>0.2 else f"{s} ❌" for s in sources]
    st.selectbox("🌐 Active Data Sources",connected)

# ------------------------------------------------------------
# 6) Prewritten Q&A setup
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
    if "daily inventory" in q: return "🕓 Dataiku job INV_2025_09 every 4h."
    return None
def shipments_answers(q):
    if "delayed shipments" in q: return "🚚 Brightstar delays in Midwest due to weather."
    if "units shipped" in q: return f"📦 {fmt_int(17000,19000)} units WTD."
    if "pending shipment" in q: return f"⚙️ {fmt_int(180,260)} pending (60% Apple)."
    if "track shipment" in q: return "📍 Dallas TX, ETA 2 days."
    if "recurring delays" in q: return "⏰ Brightstar, Marceco recurring delays >5x Q3."
    return None
def pricing_answers(q):
    if "device pricing" in q: return "💰 iPhone 16: $1,099 (Web), $1,049 (Indirect)."
    if "price drops" in q: return "📉 A15 (-$30), Moto G (-$25)."
    if "msrp" in q: return "💵 Avg 9% below MSRP."
    if "competitor pricing" in q: return "🏷️ Metro is $20 lower on iPhone 15."
    if "margin" in q: return f"💸 Margin ≈ {fmt_pct(random.uniform(11,13))}."
    return None
def forecast_answers(q):
    if "activation forecast" in q: return f"🔮 iPhone 16: {fmt_int(23000,26000)}, A15: {fmt_int(17500,20000)}."
    if "compare actual" in q: return f"📊 Accuracy ≈ {fmt_pct(random.uniform(90,92))}."
    if "forecasted to grow" in q: return "🚀 A15 and Moto G Stylus +15%."
    if "forecast accuracy" in q: return "📈 86% → 89% → 91% (Jul–Sep)."
    if "model inputs" in q: return "⚙️ Inputs refreshed 01:15 AM MT."
    return None

# ✅ FIXED: Normalized question handling to prevent blank results
def answer_for_question(q):
    qn = q.strip().lower().rstrip(".!?")  # normalize punctuation and case
    ans = (
        sales_answers(qn)
        or inventory_answers(qn)
        or shipments_answers(qn)
        or pricing_answers(qn)
        or forecast_answers(qn)
    )
    return ans if ans else "⚠️ Limited Data — working on getting in more data sources"

# ✅ FAQ dictionary unchanged
FAQ={
    "Sales":[
        "Show me sales trends by channel.",
        "What were the top-selling devices last month.",
        "Compare iPhone vs Samsung sales this quarter.",
        "Which SKUs have the highest return rate.",
        "What are the sales forecasts for next month."
    ],
    "Inventory":[
        "Which SKUs are low in stock.",
        "Show inventory aging by warehouse.",
        "How many iPhone 16 units are in Denver DC.",
        "List SKUs with overstock conditions.",
        "What's the daily inventory update feed."
    ],
    "Shipments":[
        "Show delayed shipments by DDP.",
        "How many units shipped this week.",
        "Which SKUs are pending shipment confirmation.",
        "Track shipment status for iPhone 16 Pro Max.",
        "List DDPs with recurring delays."
    ],
    "Pricing":[
        "Show current device pricing by channel.",
        "Which SKUs had price drops this week.",
        "Compare MSRP vs promo prices.",
        "Show competitor pricing insights.",
        "What’s the margin for iPhone 16 Pro Max."
    ],
    "Forecast":[
        "Show activation forecast by SKU.",
        "Compare actual vs forecast for Q3.",
        "Which SKUs are forecasted to grow fastest.",
        "Show forecast accuracy trend by month.",
        "Update forecast model inputs from Dataiku."
    ]
}

# ------------------------------------------------------------
# 7) Suggested Questions UI (Fixed Dropdown Logic)
# ------------------------------------------------------------
if not st.session_state.messages and not st.session_state.qa_history:
    st.markdown("### 💬 Choose an option below for suggested questions or ask a question")
    for category, questions in FAQ.items():
        with st.expander(f"📂 {category}"):
            sel=st.selectbox(f"Select a {category} question:",["-- Choose --"]+questions,key=f"dd_{category}")
            if sel!="-- Choose --":
                st.session_state.messages.append({"role":"user","content":sel})
                normalized_sel = sel.strip().lower().rstrip(".!?")
                a=answer_for_question(normalized_sel)
                sql=f"SELECT * FROM demo_table WHERE topic='{sel[:60]}';"
                df=pd.DataFrame({"SKU":["A15","A16","iPhone 16","Moto G"],
                                 "Sales":[random.randint(1000,3000) for _ in range(4)],
                                 "Forecast":[random.randint(1000,3000) for _ in range(4)]})
                st.session_state.qa_history.append({"q":sel,"a":a,"sql":sql,
                    "df_dict":df.to_dict(orient="list"),
                    "ts":datetime.datetime.now().isoformat(timespec="seconds"),"fb":None})
                safe_rerun()

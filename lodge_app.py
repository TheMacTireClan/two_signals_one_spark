import os
import sys
import json
import pathlib
import gspread
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# 🏗️ LEINAD: THE GLOBAL OVERRIDE
os.environ["PYTHONUTF8"] = "1"
load_dotenv()

# ==========================================
# 📐 DATA CONTROLLERS
# ==========================================

def load_json_sovereign(filename, default_value):
    try:
        path = pathlib.Path(filename)
        if path.exists():
            content = path.read_bytes().decode('utf-8', errors='ignore')
            return json.loads(content)
        return default_value
    except Exception: return default_value

def save_json_sovereign(filename, data):
    try:
        path = pathlib.Path(filename)
        content = json.dumps(data, indent=4)
        path.write_text(content, encoding='utf-8')
        return True
    except Exception: return False

# Google Ledger Handshake
SERVICE_ACCOUNT_FILE = "service_account.json" 
GOOGLE_SHEET_NAME = "Two_Signals_One_Spark_Ledger"

def sync_to_ledger(origin, phase, vault, message="", milestone=""):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client_gs = gspread.authorize(creds)
        sheet = client_gs.open(GOOGLE_SHEET_NAME).sheet1
        new_row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), origin, phase, str(vault), message, milestone]
        sheet.append_row(new_row)
        return True
    except Exception: return False

def get_ledger_signals():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client_gs = gspread.authorize(creds)
        sheet = client_gs.open(GOOGLE_SHEET_NAME).sheet1
        all_records = sheet.get_all_records()
        return [r for r in all_records if str(r.get('Origin','')).strip().lower() == 'fox'][-5:]
    except Exception: return []

# ==========================================
# 🛰️ BRAIN SELECTOR (HYBRID)
# ==========================================

def initialize_client():
    try:
        local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", timeout=1.0)
        local_client.models.list() 
        return local_client, "local-model", "🔗 Sovereign Iron (4060)"
    except Exception:
        groq_key = None
        try:
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets: groq_key = st.secrets["GROQ_API_KEY"]
        except Exception: pass
        if not groq_key: groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key), "llama-3.3-70b-versatile", "⚡ Groq Satellite (Cloud)"
        return None, None, "❌ Offline"

client, model_id, brain_status = initialize_client()

# ==========================================
# 🎨 INTERFACE & THEMES
# ==========================================

st.set_page_config(page_title="MacTíre Lodge", page_icon="🐺", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0c0e12; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #1a1c23; border-right: 2px solid #bb86fc; }
    h1,h2,h3 { color: #bb86fc; text-shadow: 0 0 10px #bb86fc; }
    .stChatMessage { background-color: #1a1c23; border-radius: 10px; border: 1px solid #3d3f4e; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Loading Data
migration_data = load_json_sovereign('migration_data.json', {"status": "Prep", "milestones": {}, "budget": {"current": 0, "goal": 7000}, "legs": []})
archive = load_json_sovereign('archive_data.json', {"tracks": [], "lorebook": {}})

with st.sidebar:
    st.header("📍 Migration Command")
    st.caption(f"Status: {brain_status}")
    st.metric("Lodge Fund", f"${migration_data['budget']['current']}")
    st.divider()
    st.info("!Kimberly is monitoring the Wind.")

tab1, tab2, tab3 = st.tabs(["🐺 The Den", "📍 War Room", "📚 Shadow Library"])

# 🐺 TAB 1: THE DEN
with tab1:
    st.title("🏛️ The Central Hearth")
    if "messages" not in st.session_state:
        SOUL = "You are the Clan MacTíre. Daniel is the Alpha. ALWAYS use *asterisks* for actions and **Bold Names** for speaking. No corporate talk. Grit, stone, and loyalty only."
        st.session_state.messages = [{"role": "system", "content": SOUL}]
    
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command, Alpha?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        if client:
            resp = client.chat.completions.create(model=model_id, messages=st.session_state.messages)
            reply = resp.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"): st.markdown(reply)

# 📍 TAB 2: WAR ROOM (The 4,400-Mile Circuit)
with tab2:
    st.title("📍 Migration Command Center")
    
    # 💰 FINANCIAL VAULT
    st.subheader("Financial Resource Management")
    col1, col2 = st.columns(2)
    
    with col1:
        budget = migration_data.get('budget', {"current": 2000, "goal": 7000})
        curr_funds = budget.get('current', 2000)
        goal_funds = budget.get('goal', 7000)
        st.metric("Lodge Gold Reserve", f"${curr_funds}", delta=f"${curr_funds - goal_funds}")
        
        if st.button("⛽ Add Gas Fill (-$60)", key="final_gas_btn"):
            migration_data['budget']['current'] -= 60
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()

    with col2:
        # 🏹 MILESTONE TRACKER
        st.write("**Operational Milestones**")
        milestones = migration_data.get('milestones', {})
        for m, done in milestones.items():
            if st.checkbox(m, value=done, key=f"war_check_{m}"):
                migration_data['milestones'][m] = not done
                save_json_sovereign('migration_data.json', migration_data)
                st.rerun()

    st.divider()

    # 🗺️ THE ITINERARY
    st.subheader("🗺️ Journey Itinerary: The 4,400-Mile Loop")
    legs = migration_data.get('legs', [])
    
    for leg in legs:
        with st.expander(f"🚩 {leg.get('name')}"):
            for stop in leg.get('stops', []):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Day {stop.get('day')}: {stop.get('dest')}**")
                    st.caption(f"📍 Pit-Stops: {stop.get('pit', 'TBD')}")
                with c2:
                    # Logic to mark individual stops as done
                    stop_done = st.checkbox("Done", value=stop.get('done', False), key=f"stop_check_{stop.get('day')}")
                    if stop_done != stop.get('done', False):
                        stop['done'] = stop_done
                        save_json_sovereign('migration_data.json', migration_data)
                        st.rerun()

# 📚 TAB 3: SHADOW LIBRARY & VESPER SIGNAL
with tab3:
    col_lib, col_vesp = st.columns([2, 1])
    with col_lib:
        st.header("📚 Shadow Library")
        if archive['tracks']:
            choice = st.selectbox("Select Scroll:", [t['title'] for t in archive['tracks']])
            track = next(t for t in archive['tracks'] if t['title'] == choice)
            st.markdown(f"### {track['title']}")
            st.text_area("Vellum", value=track['lyrics'], height=300, disabled=True)

    with col_vesp:
        st.header("🦊 Vesper Signal")
        msg = st.text_input("Signal to Cabin:", key="v_in")
        if st.button("Ignite the Spark", key="v_ignite"):
            sync_to_ledger("Alpha", migration_data['status'], migration_data['budget']['current'], msg)
            st.success("Signal Sent!")
        
        st.divider()
        st.write("### 🦊 Foxfire Feed")
        for p in reversed(get_ledger_signals()):
            st.markdown(f"**{p.get('Timestamp')}**: {p.get('Message')}")
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
# 📐 DATA CONTROLLER (JSON & GOOGLE SHEETS)
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
    except Exception as e:
        st.error(f"Save Failure: {e}")
        return False

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
    except Exception as e:
        st.error(f"Ledger Sync Failed: {e}")
        return False

def get_ledger_signals():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client_gs = gspread.authorize(creds)
        sheet = client_gs.open(GOOGLE_SHEET_NAME).sheet1
        all_records = sheet.get_all_records()
        return [r for r in all_records if r['Origin'] == 'Fox'][-5:]
    except Exception: return []

# ==========================================
# 🛰️ BRAIN SELECTOR (4060 OR GROQ)
# ==========================================

def initialize_client():
    try:
        local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", timeout=1.0)
        local_client.models.list() 
        return local_client, "local-model", "🔗 Sovereign Iron (4060)"
    except Exception:
        groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if groq_key:
            groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key)
            return groq_client, "llama-3.3-70b-versatile", "⚡ Groq Satellite (Cloud)"
        return None, None, "❌ Offline"

client, model_id, brain_status = initialize_client()

# ==========================================
# 🎨 INTERFACE & NAVIGATION
# ==========================================

st.set_page_config(page_title="MacTíre Lodge", page_icon="🐺", layout="wide")
st.markdown("<style>.stApp { background-color: #0c0e12; color: #e0e0e0; } h1,h2,h3 { color: #bb86fc; text-shadow: 0 0 10px #bb86fc; }</style>", unsafe_allow_html=True)

migration_data = load_json_sovereign('migration_data.json', {"status": "Prep", "milestones": {}, "budget": {"current": 0, "goal": 7000}})
archive = load_json_sovereign('archive_data.json', {"tracks": [], "lorebook": {}})

with st.sidebar:
    st.header("📍 Migration Command")
    st.caption(f"Status: {brain_status}")
    st.write(f"**Phase:** {migration_data.get('status', 'Unknown')}")
    st.divider()
    st.info("!Kimberly is monitoring the Wind.")

tab1, tab2, tab3 = st.tabs(["🐺 The Den", "📍 War Room", "📚 Shadow Library"])

# 🐺 TAB 1: THE DEN
with tab1:
    st.title("🏛️ The Central Hearth")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are the Clan MacTíre. Daniel is the Alpha."}]
    
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command, Alpha?"):
        # Voice Trigger logic (Optional)
        for name in ["Kalobe", "Danzer", "William", "Kimberly", "Leinad"]:
            if f"!{name.lower()}" in prompt.lower():
                v_path = f"voices/{name.lower()}_voice.wav"
                if os.path.exists(v_path): st.audio(v_path, autoplay=True)

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        if client:
            resp = client.chat.completions.create(model=model_id, messages=st.session_state.messages)
            reply = resp.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"): st.markdown(reply)

# 📍 TAB 2: WAR ROOM
with tab2:
    st.title("📍 Migration Command Center")
    col1, col2 = st.columns(2)
    with col1:
        curr = migration_data['budget']['current']
        goal = migration_data['budget']['goal']
        st.metric("Vault Balance", f"${curr}", delta=f"${curr - goal}")
        if st.button("⛽ Add Gas Fill (-$60)", key="gas_btn"):
            migration_data['budget']['current'] -= 60
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()
    
    with col2:
        st.subheader("🚩 Milestones")
        for m, done in migration_data['milestones'].items():
            if st.checkbox(m, value=done, key=f"check_{m}"):
                migration_data['milestones'][m] = True
                save_json_sovereign('migration_data.json', migration_data)

# 📚 TAB 3: SHADOW LIBRARY & VESPER SIGNAL
with tab3:
    col_lib, col_vesp = st.columns([2, 1])
    with col_lib:
        st.header("📚 Shadow Library")
        if archive['tracks']:
            titles = [t['title'] for t in archive['tracks']]
            choice = st.selectbox("Select Scroll:", titles)
            track = next(t for t in archive['tracks'] if t['title'] == choice)
            st.markdown(f"### {track['title']}")
            st.text_area("Vellum", value=track['lyrics'], height=200, disabled=True)

    with col_vesp:
        st.header("🦊 Vesper Signal")
        st.caption("Two Signals, One Spark")
        msg = st.text_input("Signal to Cabin:", key="vesp_input")
        if st.button("Ignite the Spark", key="ignite_btn"):
            if sync_to_ledger("Alpha", migration_data['status'], migration_data['budget']['current'], msg):
                st.success("Signal Sent to Ledger!")
        
        st.divider()
        st.write("### 🦊 Foxfire Feed")
        fox_pulses = get_ledger_signals()
        if not fox_pulses: st.info("Waiting for the Fox...")
        for p in reversed(fox_pulses):
            st.markdown(f"**{p['Timestamp']}**: {p['Message']}")
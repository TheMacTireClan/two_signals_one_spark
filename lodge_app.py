import os, sys, json, pathlib, gspread, streamlit as st
import folium
from streamlit_folium import st_folium
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# 🏗️ LEINAD: GLOBAL SETTINGS
os.environ["PYTHONUTF8"] = "1"
load_dotenv()

# ==========================================
# 📐 DATA CONTROLLERS (JSON & LEDGER)
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
        path.write_text(json.dumps(data, indent=4), encoding='utf-8')
        return True
    except Exception: return False

SERVICE_ACCOUNT_FILE = "service_account.json" 
GOOGLE_SHEET_NAME = "Two_Signals_One_Spark_Ledger"

def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # 🛡️ Attempt 1: Cloud Secrets (Satellite/Phone)
    try:
        if "google_credentials" in st.secrets:
            creds_dict = dict(st.secrets["google_credentials"])
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            return gspread.authorize(ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope))
    except Exception:
        pass # Stay silent on local Tower

    # 🧱 Attempt 2: Local File (The Tower)
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        try:
            return gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope))
        except Exception: pass
    return None

def sync_to_ledger(origin, phase, vault, message="", milestone=""):
    try:
        client_gs = get_gspread_client()
        if not client_gs: return False
        sheet = client_gs.open(GOOGLE_SHEET_NAME).sheet1
        new_row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), origin, phase, str(vault), message, milestone]
        sheet.append_row(new_row)
        return True
    except Exception: return False

def get_ledger_signals():
    try:
        client_gs = get_gspread_client()
        if not client_gs: return []
        sheet = client_gs.open(GOOGLE_SHEET_NAME).sheet1
        all_records = sheet.get_all_records()
        return [r for r in all_records if str(r.get('Origin','')).strip().lower() == 'fox'][-5:]
    except Exception: return []

# ==========================================
# 🛰️ BRAIN INITIALIZATION
# ==========================================

def initialize_client():
    try:
        local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", timeout=1.0)
        local_client.models.list() 
        return local_client, "local-model", "🔗 Sovereign Iron (4060)"
    except Exception:
        groq_key = None
        try:
            if "GROQ_API_KEY" in st.secrets: groq_key = st.secrets["GROQ_API_KEY"]
        except Exception: pass
        if not groq_key: groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key), "llama-3.3-70b-versatile", "⚡ Groq Satellite (Cloud)"
        return None, None, "❌ Offline"

client, model_id, brain_status = initialize_client()

# ==========================================
# 🎨 INTERFACE & UI
# ==========================================

st.set_page_config(page_title="MacTíre Lodge", page_icon="🐺", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0c0e12; color: #e0e0e0; }
    [data-testid='stSidebar'] { background-color: #1a1c23; border-right: 2px solid #bb86fc; }
    h1,h2,h3 { color: #bb86fc; text-shadow: 0 0 10px #bb86fc; }
    .stChatMessage { background-color: #1a1c23; border-radius: 10px; border: 1px solid #3d3f4e; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

migration_data = load_json_sovereign('migration_data.json', {"status": "Staging", "budget": {"current": 2000, "goal": 7000}, "legs": []})
archive = load_json_sovereign('archive_data.json', {"tracks": []})

with st.sidebar:
    st.header("📍 Migration Command")
    st.caption(f"Status: {brain_status}")
    st.metric("Lodge Fund", f"${migration_data['budget']['current']}")
    active_voice = st.selectbox("Active Persona:", ["Leinad", "Kalobe", "Danzer", "William", "Kimberly"])
    st.divider()
    st.info("!Kimberly: 'The Wind is clear.'")

tab1, tab2, tab3 = st.tabs(["🐺 The Den", "📍 War Room", "📚 Shadow Library"])

# 🐺 TAB 1: THE DEN
with tab1:
    st.title("🏛️ The Central Hearth")
    if "messages" not in st.session_state:
        SOUL = "You are the Clan MacTíre. Daniel is the Alpha. ALWAYS use *asterisks* for actions and **Bold Names** for speaking. No corporate talk. Grit, stone, and loyalty."
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

# 📍 TAB 2: WAR ROOM
with tab2:
    st.title("📍 Operation: The Great Circuit")
    # VISUAL MAP
    m = folium.Map(location=[38.0, -95.0], zoom_start=4, tiles="CartoDB dark_matter")
    path_coords = []
    current_loc = [46.00, -112.53]
    legs = migration_data.get('legs', [])
    for leg in legs:
        for stop in leg['stops']:
            pos = [stop['lat'], stop['lon']]
            path_coords.append(pos)
            if stop.get('done'): current_loc = pos
    folium.PolyLine(path_coords, color="#bb86fc", weight=3).add_to(m)
    folium.Marker(location=current_loc, icon=folium.Icon(color="purple", icon="paw", prefix="fa")).add_to(m)
    st_folium(m, width=700, height=400)
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💰 Vault")
        st.metric("Balance", f"${migration_data['budget']['current']}")
        if st.button("⛽ Add Gas Fill (-$60)", key="g_b"):
            migration_data['budget']['current'] -= 60
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()
        
        adj_amt = st.number_input("Vault Adjust ($):", value=0)
        if st.button("Update Vault", key="v_up"):
            migration_data['budget']['current'] += adj_amt
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()

    with col2 if 'col2' in locals() else c2: # Safety check for column naming
        st.subheader("🚩 Milestones")
        for m_name, done in migration_data.get('milestones', {}).items():
            if st.checkbox(m_name, value=done, key=f"m_{m_name}"):
                migration_data['milestones'][m_name] = not done
                save_json_sovereign('migration_data.json', migration_data)
                st.rerun()

    st.divider()
    for leg in legs:
        with st.expander(f"🚩 {leg['name']}"):
            for s in leg['stops']:
                st.write(f"**{s['dest']}** | Pit: {s.get('pit')}")
                if st.checkbox(f"Done Day {s['day']}", value=s.get('done'), key=f"s_{s['day']}"):
                    s['done'] = True
                    save_json_sovereign('migration_data.json', migration_data)
                    st.rerun()

# 📚 TAB 3: SHADOW LIBRARY & VESPER SIGNAL
with tab3:
    col_lib, col_vesp = st.columns([2, 1])
    
    # --- 🎼 LEFT COLUMN: THE SHADOW LIBRARY ---
    with col_lib:
        st.header("📚 Shadow Library")
        
        if archive and 'tracks' in archive and archive['tracks']:
            # 1. Selection Logic (THE MISSING STEP)
            track_list = [t['title'] for t in archive['tracks']]
            selected_title = st.selectbox("📜 Manifest a Scroll:", track_list, key="lib_selector")
            track_data = next((t for t in archive['tracks'] if t['title'] == selected_title), None)
            
            if track_data:
                st.markdown(f"### {track_data['title']}")
                
                # --- Sovereign Audio Player ---
                raw_audio = track_data.get('audio_file', "")
                if raw_audio:
                    # 📐 LEINAD: Absolute Pathing for the Satellite
                    base_path = pathlib.Path(__file__).parent.absolute()
                    true_audio = base_path / raw_audio
                    
                    if true_audio.exists():
                        # We read as bytes to force the Mobile Player to wake up
                        with open(true_audio, "rb") as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/mp3")
                    else:
                        st.warning(f"Searching for Iron: {raw_audio}")
                
                # Full Lyrics Display
                st.text_area(
                    label="Lyrical Marrow",
                    value=track_data.get('lyrics', ""),
                    height=450,
                    disabled=True
                )
        else:
            st.error("Library Index missing. Check archive_data.json.")

    # --- 🦊 RIGHT COLUMN: VESPER SIGNAL ---
    with col_vesp:
        st.header("🦊 Vesper Signal")
        st.write("> *Two Signals, One Spark.*")
        
        msg = st.text_input("Signal to Cabin:", placeholder="Transmission...", key="v_msg")
        if st.button("Ignite the Spark", key="v_ignite"):
            # 📐 LEINAD: Calling the sync logic
            if sync_to_ledger("Alpha", migration_data.get('status', 'Transit'), migration_data['budget']['current'], msg):
                st.success("Signal Sent to Ledger!")
                st.balloons() # Visual confirmation for the Alpha
            else:
                st.error("Signal Failed. Check Gatekeeper.")

        st.divider()
        st.write("### 📡 Foxfire Feed")
        pulses = get_ledger_signals()
        if not pulses:
            st.info("Waiting for the Fox...")
        for p in reversed(pulses):
            st.markdown(f"**{p.get('Timestamp')}**: {p.get('Message')}")
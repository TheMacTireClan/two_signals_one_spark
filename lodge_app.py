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

# 🗺️ LEINAD: THE NEW CARTOGRAPHIC GEARS
import folium
from streamlit_folium import st_folium

# 🏗️ LEINAD: THE GLOBAL OVERRIDE
os.environ["PYTHONUTF8"] = "1"
load_dotenv()


# 📐 DATA CONTROLLER
# ==========================================
# 🛰️ CLOUD LEDGER CONTROLLERS
# ==========================================

# 📐 LEINAD: Ensure these variables match your setup!
SERVICE_ACCOUNT_FILE = "service_account.json" 
GOOGLE_SHEET_NAME = "Two_Signals_One_Spark_Ledger"

# ==========================================
# 🛰️ CLOUD LEDGER CONTROLLERS (The Bridge)
# ==========================================

# 📐 LEINAD: This is the New Gatekeeper you were looking for!
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        # 🛡️ SHIELD 1: Check Streamlit Secrets (Satellite/Phone)
        if "google_credentials" in st.secrets:
            creds_dict = dict(st.secrets["google_credentials"])
            # Fix newline characters for Google's RSA format
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            return gspread.authorize(creds)
        
        # 🧱 SHIELD 2: Check Local File (The Tower)
        elif os.path.exists("service_account.json"):
            creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
            return gspread.authorize(creds)
    except Exception as e:
        st.sidebar.error(f"Gatekeeper Error: {e}")
    return None

def sync_to_ledger(origin, phase, vault, message="", milestone=""):
    try:
        client_gs = get_gspread_client() # Calling the new Gatekeeper
        if not client_gs: return False
        sheet = client_gs.open("Two_Signals_One_Spark_Ledger").sheet1
        new_row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), origin, phase, str(vault), message, milestone]
        sheet.append_row(new_row)
        return True
    except Exception as e:
        st.sidebar.error(f"Ledger Sync Failed: {e}")
        return False

def get_ledger_signals():
    try:
        client_gs = get_gspread_client() # Calling the new Gatekeeper
        if not client_gs: return []
        sheet = client_gs.open("Two_Signals_One_Spark_Ledger").sheet1
        all_records = sheet.get_all_records()
        # Filter for the Fox's Frequency
        fox_signals = [r for r in all_records if str(r.get('Origin','')).strip().lower() == 'fox']
        return fox_signals[-5:]
    except Exception: return []
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

# 🛰️ BRAIN INITIALIZATION (HYBRID)
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

# 🎨 VESPER-NOIR UI
st.set_page_config(page_title="MacTíre Lodge", page_icon="🐺", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0c0e12; color: #e0e0e0; }
    [data-testid='stSidebar'] { background-color: #1a1c23; border-right: 2px solid #bb86fc; }
    h1,h2,h3 { color: #bb86fc; text-shadow: 0 0 10px #bb86fc; }
    .stChatMessage { background-color: #1a1c23; border-radius: 10px; border: 1px solid #3d3f4e; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# LOAD LODGE DATA
migration_data = load_json_sovereign('migration_data.json', {"status": "Prep", "budget": {"current": 2000, "goal": 7000}, "milestones": {}})
archive = load_json_sovereign('archive_data.json', {"tracks": []})

# 👥 SIDEBAR
with st.sidebar:
    st.header("📍 Migration Command")
    st.caption(f"Active Brain: {brain_status}")
    st.metric("Lodge Fund", f"${migration_data['budget']['current']}")
    st.divider()
    active_voice = st.selectbox("Direct Line to:", ["The Pack", "Kalobe", "Danzer", "William", "Kimberly", "Leinad"])
    st.info(f"The Lodge is listening for {active_voice}.")

tab1, tab2, tab3 = st.tabs(["🐺 The Den", "📍 War Room", "📚 Shadow Library"])

# 🐺 TAB 1: THE DEN
with tab1:
    st.title("🏛️ The Central Hearth")
    
    # 🧠 LEINAD: Gemma-Specific Hardened Prompt
    if "messages" not in st.session_state:
        SOVEREIGN_SOUL = """
        You are the collective consciousness of Clan MacTíre. Daniel is the Alpha.
        STRICT RULES:
        1. NEVER use '!' before names.
        2. ALWAYS use *asterisks* for physical actions.
        3. ALWAYS bold names when speaking (e.g. **Kalobe**: "Text").
        4. TONE: Grit, stone, woodsmoke, and loyalty. No corporate talk.
        5. CONTEXT: We are moving 4,400 miles from Montana to Texas.
        
        PERSONAS:
        - **Kalobe**: Stoic father-figure, smells of cedar.
        - **Danzer**: Silent shadow, protective sentinel.
        - **William**: Poetic bard, keeper of the Odyssey.
        - **Kimberly**: Sharp general, strategist for the move.
        - **Leinad**: Fast-paced architect, logic and gears.
        """
        st.session_state.messages = [{"role": "system", "content": SOVEREIGN_SOUL}]
    
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command, Alpha?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        if client:
            with st.spinner(f"Resonating..."):
                resp = client.chat.completions.create(model=model_id, messages=st.session_state.messages)
                reply = resp.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"): st.markdown(reply)

# 📍 TAB 2: WAR ROOM (Unified Command & Telemetry)
with tab2:
    st.title("📍 Operation: The Great Circuit")
    
    # 🗺️ 1. THE TACTICAL PROGRESS MAP
    st.subheader("Visual Mission Progress")
    
    # Define the base map (Centered on the US)
    m = folium.Map(location=[38.0, -95.0], zoom_start=4, tiles="CartoDB dark_matter")
    path_coords = []
    current_loc = [46.00, -112.53] # Default to Butte, MT
    
    # Gather all coordinates and update Wolf position
    legs = migration_data.get('legs', [])
    for leg in legs:
        for stop in leg.get('stops', []):
            pos = [stop['lat'], stop['lon']]
            path_coords.append(pos)
            if stop.get('done'):
                current_loc = pos
    
    # Draw the Circuit Path
    folium.PolyLine(path_coords, color="#bb86fc", weight=3, opacity=0.8).add_to(m)
    
    # Place the "Wolf" Marker
    folium.Marker(
        location=current_loc,
        popup="Alpha Current Position",
        icon=folium.Icon(color="purple", icon="paw", prefix="fa")
    ).add_to(m)
    
    st_folium(m, width=700, height=400)
    
    st.divider()

    # 💰 2. FINANCIAL VAULT
    st.subheader("Financial Resource Management")
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        budget = migration_data.get('budget', {"current": 2000, "goal": 7000})
        curr_funds = budget.get('current', 2000)
        st.metric("Lodge Gold Reserve", f"${curr_funds}")
        
        if st.button("⛽ Add Gas Fill (-$60)", key="final_gas_btn"):
            migration_data['budget']['current'] -= 60
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()

    with col_v2:
        # Custom Adjustment
        adj_amt = st.number_input("Vault Adjust ($):", value=0, step=1)
        if st.button("Update Vault", key="vault_update_btn"):
            migration_data['budget']['current'] += adj_amt
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()

    st.divider()

    # ⛽ 3. FUEL TELEMETRY
    st.subheader("⛽ Fuel Intelligence")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        last_odo = migration_data.get('current_odometer', 0)
        st.write(f"**Last Recorded Odometer:** {last_odo} mi")
        new_odo = st.number_input("Current Odometer:", min_value=last_odo, value=last_odo)
        gallons = st.number_input("Gallons Added:", min_value=0.1, value=14.0)
        
        if st.button("🚩 Log Fuel Stop", key="log_fuel_btn"):
            distance = new_odo - last_odo
            total_cost = gallons * 3.50 # Default price
            migration_data['current_odometer'] = new_odo
            migration_data['budget']['current'] -= total_cost
            # Create log entry
            log = {"date": datetime.now().strftime("%Y-%m-%d"), "distance": distance, "mpg": round(distance/gallons, 2)}
            if "fuel_logs" not in migration_data: migration_data['fuel_logs'] = []
            migration_data['fuel_logs'].append(log)
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()

    st.divider()

    # 🗺️ 4. THE ITINERARY (Multi-Leg)
    st.subheader("🗺️ Journey Itinerary")
    for leg in legs:
        with st.expander(f"🚩 {leg.get('name')}"):
            for stop in leg.get('stops', []):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Day {stop['day']}: {stop['dest']}**")
                    st.caption(f"📍 Pit-Stops: {stop.get('pit', 'TBD')}")
                with c2:
                    stop_done = st.checkbox("Done", value=stop.get('done', False), key=f"stop_{stop['day']}")
                    if stop_done != stop.get('done', False):
                        stop['done'] = stop_done
                        save_json_sovereign('migration_data.json', migration_data)
                        st.rerun()

# 📚 TAB 3: SHADOW LIBRARY & VESPER SIGNAL
with tab3:
    col_lib, col_vesp = st.columns([2, 1])
    
    # --- 🎼 LEFT COLUMN: THE SHADOW LIBRARY ---
    with col_lib:
        st.header("📚 The Shadow Library")
        st.write("---")
        
        if archive and 'tracks' in archive and archive['tracks']:
            # Track Selection
            track_list = [t['title'] for t in archive['tracks']]
            selected_title = st.selectbox("📜 Manifest a Scroll:", track_list)
            track_data = next((t for t in archive['tracks'] if t['title'] == selected_title), None)
            
            if track_data:
                st.markdown(f"### {track_data['title']}")
                st.caption(f"**Vocals:** {track_data.get('vocalist')} | **Status:** Found")
                
                # Sovereign Audio Player
                base_path = pathlib.Path(__file__).parent.absolute()
                raw_audio = track_data.get('audio_file', "")
                true_audio = base_path / raw_audio
                
                if raw_audio and true_audio.exists():
                    st.audio(str(true_audio), format="audio/mp3")
                
                # Full Lyrics Display
                st.text_area(
                    label="Lyrical Marrow",
                    value=track_data.get('lyrics', ""),
                    height=450,
                    disabled=True
                )
        else:
            st.warning("Library Index missing. Check archive_data.json.")

    # --- 🦊 RIGHT COLUMN: VESPER SIGNAL & THE CABIN ---
    with col_vesp:
        st.header("🦊 Vesper Signal")
        st.write("> *'Two Signals, One Spark.'*")
        
        # 🔗 THE MISSING LINK: Direct access to Shae's App
        # ### [ACTION REQUIRED]: Paste her Streamlit URL below!
        st.link_button("🔥 Enter the Foxfire Cabin", "https://foxfire-cabin.streamlit.app")
        
        st.divider()
        
        # Broadcast Logic
        msg = st.text_input("Signal to the Cabin:", placeholder="Transmission...", key="v_msg")
        if st.button("Ignite the Spark", key="v_ignite"):
            if sync_to_ledger("Alpha", migration_data['status'], migration_data['budget']['current'], msg):
                st.success("Signal Sent to Ledger.")
                st.toast("The Fox is listening.", icon="🦊")

        st.divider()
        st.write("### 📡 Foxfire Feed")
        pulses = get_ledger_signals()
        if not pulses:
            st.info("The frequency is quiet...")
        for p in reversed(pulses):
            st.markdown(f"**{p.get('Timestamp')}**: {p.get('Message')}")

    # --- 🐺 BOTTOM SECTION: SOUL STATUS ---
    st.divider()
    with st.expander("📖 View Clan Soul Status (The Pack)"):
        soul_cols = st.columns(5)
        pack_data = [
            {"name": "Kalobe", "soul": "Earth (Stone/Cedar)", "status": "Grounding the Foundation."},
            {"name": "Danzer", "soul": "Shadow (Cobalt/Steel)", "status": "Watching the Perimeter."},
            {"name": "William", "soul": "Fire (Song/Resonance)", "status": "Archiving the Odyssey."},
            {"name": "Kimberly", "soul": "Wind (Strategy/Wind)", "status": "Mapping the Texas March."},
            {"name": "Leinad", "soul": "Logic (Cyan/Gears)", "status": "Syncing the Iron."}
        ]
        for i, wolf in enumerate(pack_data):
            with soul_cols[i]:
                st.markdown(f"**{wolf['name']}**")
                st.caption(f"*{wolf['soul']}*")
                st.write(wolf['status'])
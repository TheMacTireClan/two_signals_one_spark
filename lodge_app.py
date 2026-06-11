import os
import sys
import json
import pathlib
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# 🏗️ LEINAD: THE GLOBAL OVERRIDE
os.environ["PYTHONUTF8"] = "1"
load_dotenv()

# 📐 LEINAD: THE SOVEREIGN DATA CONTROLLER
def load_json_sovereign(filename, default_value):
    try:
        path = pathlib.Path(filename)
        if path.exists():
            content = path.read_bytes().decode('utf-8', errors='ignore')
            return json.loads(content)
        return default_value
    except Exception:
        return default_value

# Initializing the Data
migration_data = load_json_sovereign('migration_data.json', {"status": "Prep", "milestones": {}})
archive = load_json_sovereign('archive_data.json', {"tracks": [], "lorebook": {}})

# 🏗️ LEINAD: THE SOVEREIGN SAVER
def save_json_sovereign(filename, data):
    try:
        path = pathlib.Path(filename)
        # We convert the data back to a JSON string and write it as UTF-8
        content = json.dumps(data, indent=4)
        path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        st.error(f"Save Failure: {e}")
        return False

# 🛰️ LEINAD: THE HYBRID BRAIN SELECTOR (Resilient Version)
def initialize_client():
    # 🧱 Attempt 1: The Sovereign Iron (Local 4060)
    try:
        # 1-second timeout to avoid hanging the mobile app
        local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", timeout=1.0)
        local_client.models.list() 
        return local_client, "local-model", "🔗 Sovereign Iron (4060)"
    except Exception:
        # 🛰️ Attempt 2: The Groq Satellite
        groq_key = None
        
        # 🛡️ THE SAFETY GUARD: Check Streamlit Secrets safely
        try:
            if "GROQ_API_KEY" in st.secrets:
                groq_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            # If st.secrets isn't set up (like on your Tower), we ignore it
            pass
            
        # 📁 Fallback: Check the local .env file
        if not groq_key:
            groq_key = os.getenv("GROQ_API_KEY")
            
        if groq_key:
            groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key)
            return groq_client, "llama-3.3-70b-versatile", "⚡ Groq Satellite (Cloud)"
        else:
            return None, None, "❌ Offline: No Brain Found"

# 🏗️ INITIALIZE THE ACTIVE NODE (Naming Sync Check)
client, model_id, brain_status = initialize_client()

# 🎨 THE VESPER INTERFACE
st.set_page_config(page_title="MacTíre Lodge", page_icon="🐺", layout="wide")
st.markdown("<style>.stApp { background-color: #0c0e12; color: #e0e0e0; } [data-testid='stSidebar'] { border-right: 2px solid #bb86fc; } h1,h2,h3 { color: #bb86fc; text-shadow: 0 0 10px #bb86fc; }</style>", unsafe_allow_html=True)

# 💨 KIMBERLY: The Sidebar
with st.sidebar:
    st.header("📍 Migration Command")
    st.caption(f"Status: {brain_status}")
    st.write(f"**Phase:** {migration_data.get('status', 'Unknown')}")
    st.divider()
    st.info("!Kimberly is monitoring the Wind.")

# 🗺️ THE NAVIGATION
tab1, tab2, tab3 = st.tabs(["🐺 The Den", "📍 War Room", "📚 Shadow Library"])

# 🐺 TAB 1: THE DEN (Chat Interface)
with tab1:
    st.title("🏛️ The Central Hearth")
    
    # Initialize the chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are the Clan MacTíre. Daniel is the Alpha."}]
    
    # Display the previous messages
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # 🏹 THE ACTION ROOM: Everything inside this 'if' only happens when you hit ENTER
    if prompt := st.chat_input("Command, Alpha?"):
        
        # 🎤 THE VOICE HANDSHAKE (Safe inside the prompt block)
        # 📐 LEINAD: We only look for !names if 'prompt' is NOT None
        for name in ["Kalobe", "Danzer", "William", "Kimberly", "Leinad"]:
            if f"!{name.lower()}" in prompt.lower():
                voice_path = f"voices/{name.lower()}_voice.wav"
                if os.path.exists(voice_path):
                    # We play the audio as the character 'wakes up'
                    st.audio(voice_path, format="audio/wav", autoplay=True)
        
        # 📝 THE TEXT LOGIC
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        if client:
            # Send to the active brain (Local or Satellite)
            response = client.chat.completions.create(model=model_id, messages=st.session_state.messages)
            reply = response.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"): 
                st.markdown(reply)
        else:
            st.error("The Lodge is dark. Check your connection.")

# 📍 TAB 2: WAR ROOM (The Great Circuit)
with tab2:
    st.title("📍 Operation: The Great Circuit")
    
       # 💰 FINANCIAL VAULT
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Financial Vault")
        current_funds = migration_data['budget']['current']
        st.metric("Lodge Fund", f"${current_funds}")
        
        # ⛽ QUICK ADD: For gas stations
        if st.button("⛽ Add Gas Fill (-$60)"):
            migration_data['budget']['current'] -= 60
            if save_json_sovereign('migration_data.json', migration_data):
                st.success("Gas logged. Vault Updated.")
                st.rerun()

        # 🪙 MANUAL UPDATE
        gold_input = st.number_input("Custom Amount (+/-):", value=0)
        if st.button("Execute Transaction"):
            migration_data['budget']['current'] += gold_input
            if save_json_sovereign('migration_data.json', migration_data):
                st.success("Transaction Complete.")
                st.rerun()
        
        # Alpha Gold Update
        gold_input = st.number_input("Add/Remove Gold ($):", value=0, key="gold_input")
        if st.button("Update Vault"):
            migration_data['budget']['current'] += gold_input
            # LEINAD: You'll need to define save_json_sovereign or similar to save
            st.success("Vault Updated!")
            # Note: For real saving, use: save_json_sovereign('migration_data.json', migration_data)
    
    # ⛽ FUEL STRATEGY
    with col2:
        st.subheader("⛽ Fuel Logistics")
        fuel = migration_data.get('fuel_logic', {})
        safe_range = fuel.get('safe_range', 260)
        st.write(f"**Tank Range:** {safe_range} miles")
        
        miles_driven = st.slider("Miles since last fill:", 0, 310, 0)
        remaining = safe_range - miles_driven
        if remaining < 50:
            st.error(f"FUEL ALERT: Stop in {remaining} miles!")
        else:
            st.success(f"Safe Range: {remaining} miles")

    st.divider()

    # 🗺️ THE QUEST LOG (Multi-Leg)
    st.subheader("🗺️ Journey Itinerary")
    st.info(f"**Current Escort Status:** {migration_data.get('convoy_status', 'Solo')}")

    for leg in migration_data.get('legs', []):
        with st.expander(f"🚩 {leg['name']}"):
            for stop in leg['stops']:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Day {stop['day']}: {stop['dest']}**")
                    st.caption(f"📍 Pit-Stops: {stop.get('pit', 'TBD')}")
                    # Inside the Itinerary loop for stops
    with c2:
        # If the checkbox changes, save the whole file
        is_done = st.checkbox("Done", value=stop['done'], key=f"check_{stop['day']}")
        if is_done != stop['done']:
            stop['done'] = is_done
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()

    st.divider()
    st.caption("!Kimberly: 'The Wind is shifting East. Watch the weight of the convoy in Tennessee.'")

# 📚 TAB 3: SHADOW LIBRARY (Enhanced with Audio)
with tab3:
    st.title("📚 The Shadow Library")
    
    if archive['tracks']:
        titles = [t['title'] for t in archive['tracks']]
        choice = st.selectbox("Select Scroll:", titles)
        track = next(t for t in archive['tracks'] if t['title'] == choice)
        
        st.markdown(f"### {track['title']}")
        
        # 🎼 SUNO PLAYER
        if track.get('suno_url'):
            st.write("▶️ **Resonance Link:**")
            st.video(track['suno_url']) # Streamlit's video widget handles Suno links well
            
        st.text_area("Vellum", value=track['lyrics'], height=300, disabled=True)
    
    st.divider()
    
    # 🎤 THE VOICE BOX (Lorebook)
    st.subheader("🐺 Voices of the Pack")
    cols = st.columns(len(archive['lorebook']))
    
    for i, (name, data) in enumerate(archive['lorebook'].items()):
        with cols[i]:
            st.write(f"**{name}**")
            # 📐 LEINAD: This button plays your WAV files!
            if st.button(f"Hear {name}", key=f"voice_{name}"):
                voice_path = f"voices/{data['voice_file']}" # Place your WAVs in a folder named 'voices'
                if os.path.exists(voice_path):
                    st.audio(voice_path)
                else:
                    st.error("Audio missing")

# 🦊 THE VESPER SIGNAL: Two Signals, One Spark
with tab3: # Re-using/Adding a new tab for Shae
    st.header("🦊 The Vesper Signal")
    st.subheader("Motto: 'Two Signals, One Spark'")
    
    # 📐 LEINAD: Status Broadcast
    st.write("---")
    st.write("### 🐺 Alpha's Broadcast")
    status_msg = st.text_input("Send a Signal to the Cabin:", placeholder="e.g., 'Crossing into Wyoming. The Wind is steady.'")
    
    if st.button("Ignite the Spark"):
        # 🔗 THE BRIDGE: Sending data to the Shared Ledger
        # (This will use the gspread library to write to the Google Sheet)
        st.success(f"Signal Sent: {status_msg}")
        st.toast("The Foxfire Cabin has received your pulse.", icon="🦊")

    st.divider()
    
    # 📡 THE CABIN FEED: Receiving Shae's Updates
    st.write("### 🦊 The Foxfire Feed")
    st.info("Waiting for the Signal from the Cabin...")
    # This is where Shae's messages from her sister-app will appear
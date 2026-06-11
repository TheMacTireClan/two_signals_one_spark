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

# 🐺 TAB 1: THE DEN
with tab1:
    st.title("🏛️ The Central Hearth")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are the Clan MacTíre. Daniel is the Alpha."}]
    
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Command, Alpha?"):
        if client:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            # 📐 LEINAD: Sending the signal to the active model_id
            response = client.chat.completions.create(model=model_id, messages=st.session_state.messages)
            reply = response.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"): st.markdown(reply)
        else:
            st.error("The Lodge is dark. Check your Groq Key in Streamlit Secrets.")

# 📍 TAB 2: WAR ROOM (The Great Circuit)
with tab2:
    st.title("📍 Operation: The Great Circuit")
    
    # 💰 FINANCIAL VAULT
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Financial Vault")
        current_funds = migration_data['budget']['current']
        goal_funds = migration_data['budget']['goal']
        st.metric("Lodge Fund", f"${current_funds}", delta=f"${current_funds - goal_funds}")
        
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
                with c2:
                    st.checkbox("Done", value=stop['done'], key=f"check_{stop['day']}")

    st.divider()
    st.caption("!Kimberly: 'The Wind is shifting East. Watch the weight of the convoy in Tennessee.'")

# 📚 TAB 3: SHADOW LIBRARY
with tab3:
    st.title("📚 Shadow Library")
    if archive['tracks']:
        titles = [t['title'] for t in archive['tracks']]
        choice = st.selectbox("Select Scroll:", titles)
        track = next(t for t in archive['tracks'] if t['title'] == choice)
        st.markdown(f"### {track['title']}")
        st.text_area("Vellum", value=track['lyrics'], height=300, disabled=True)
    
    st.divider()
    with st.expander("📖 Explore the Lorebook"):
        for key, value in archive.get('lorebook', {}).items():
            st.write(f"**{key}:** {value}")
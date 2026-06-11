import os
import sys
import json
import pathlib
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# 🏗️ LEINAD: THE GLOBAL OVERRIDE
os.environ["PYTHONUTF8"] = "1"

# 📐 LEINAD: THE HYBRID BRAIN SELECTOR
def initialize_client():
    # 🧱 Attempt 1: The Sovereign Iron (Local 4060)
    try:
        # We use a 1-second timeout so it doesn't hang if the PC is off
        local_client = OpenAI(
            base_url="http://localhost:1234/v1", 
            api_key="lm-studio",
            timeout=1.0 
        )
        local_client.models.list() # Test connection
        return local_client, "local-model", "🔗 Sovereign Iron (4060)"
    except Exception:
       # 🛰️ Attempt 2: The Groq Satellite (Update the model_id)
return groq_client, "llama-3.3-70b-versatile", "⚡ Groq Satellite (Cloud)"
        if groq_key:
            groq_client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=groq_key
            )
            # We use the powerful 70B model for the skeleton crew
            return groq_client, "llama-3.1-70b-versatile", "⚡ Groq Satellite (Cloud)"
        else:
            return None, None, "❌ Offline: No Brain Found"

client, model_id, brain_status = initialize_client()
st.sidebar.caption(f"📍 Brain: {brain_status}")

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

# 🧱 THE VAULT & CLIENT
load_dotenv()
local_key = os.getenv("LOCAL_API_KEY") or "lm-studio"
client = OpenAI(base_url="http://localhost:1234/v1", api_key=local_key)

# 🎨 THE VESPER INTERFACE (Styling)
st.set_page_config(page_title="MacTíre Lodge", page_icon="🐺", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0c0e12; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #1a1c23; border-right: 2px solid #bb86fc; }
    h1, h2, h3 { color: #bb86fc; text-shadow: 0 0 10px #bb86fc; }
    .stChatMessage { background-color: #242730; border-radius: 15px; border: 1px solid #3d3f4e; }
    </style>
    """, unsafe_allow_html=True)

# 💨 KIMBERLY: The War Room Sidebar
with st.sidebar:
    st.header("📍 Migration Command")
    st.write(f"**Current Phase:** {migration_data.get('status', 'Initialization')}")
    
    # Progress Calculation
    milestones = migration_data.get('milestones', {})
    if milestones:
        completed = sum(milestones.values())
        total = len(milestones)
        st.progress(completed / total if total > 0 else 0)
        st.subheader("🚩 Milestones")
        for task, done in milestones.items():
            status_icon = "✅" if done else "⏳"
            st.write(f"{status_icon} {task}")
    
    st.divider()
    st.info("!Kimberly is monitoring the 'Wind'.")

# 🗺️ THE NAVIGATION TABS
tab1, tab2, tab3 = st.tabs(["🐺 The Den", "📍 Tactical Map", "📚 Shadow Library"])

# 🐺 TAB 1: THE DEN
with tab1:
    st.title("🏛️ The Central Hearth")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are the Clan MacTíre. Daniel is the Alpha."}]
    
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Command, Alpha?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        response = client.chat.completions.create(model="local-model", messages=st.session_state.messages)
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"): st.markdown(reply)

# 📍 TAB 2: WAR ROOM (Full View)
with tab2:
    st.title("📍 Migration Strategy")
    st.write("Detailed Logistical Briefing:")
    st.json(migration_data)

# 📚 TAB 3: SHADOW LIBRARY
with tab3:
    st.title("📚 The Shadow Library")
    if archive['tracks']:
        track_titles = [t['title'] for t in archive['tracks']]
        selected_title = st.selectbox("Select a Scroll to read:", track_titles)
        track = next(t for t in archive['tracks'] if t['title'] == selected_title)
        
        st.markdown(f"### {track['title']}")
        st.caption(f"Lead Vocals: {track.get('vocalist')} | Resonance: {track.get('resonance')}")
        st.text_area("Vellum", value=track['lyrics'], height=300, disabled=True)
    
    st.divider()
    
    # 📜 Lorebook Section (Now Restored)
    with st.expander("📖 Explore the Lorebook"):
        for key, value in archive.get('lorebook', {}).items():
            st.write(f"**{key}:** {value}")
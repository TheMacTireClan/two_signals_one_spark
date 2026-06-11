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

# Initializing Shared Data (The Alpha's Progress) and Her Data
migration_data = load_json_sovereign('migration_data.json', {"status": "Prep", "milestones": {}})
foxfire_data = load_json_sovereign('foxfire_data.json', {"pack_name": "The Vesper Spirits", "lore": {}})

# 🛰️ LEINAD: THE HYBRID BRAIN SELECTOR
def initialize_client():
    try:
        local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", timeout=0.5)
        local_client.models.list() 
        return local_client, "local-model", "🔗 Connected to the Lodge Forge"
    except Exception:
        groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        if groq_key:
            groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key)
            return groq_client, "llama-3.3-70b-versatile", "⚡ Groq Satellite (Vesper-Link)"
        return None, None, "❌ Offline"

client, model_id, brain_status = initialize_client()

# 🎨 THE FOXFIRE CABIN: HEARTH-LIGHT SKIN
st.set_page_config(page_title="The Foxfire Cabin", page_icon="🦊", layout="wide")

st.markdown("""
    <style>
    /* Main Background: Dark Walnut / Cabin at Night */
    .stApp {
        background-color: #1b1212;
        color: #e67e22;
    }
    
    /* Sidebar: Deep Mahogany Wood Vibe */
    [data-testid="stSidebar"] {
        background-color: #2c1b18;
        border-right: 2px solid #d35400;
    }

    /* Glowing Ember Headers */
    h1, h2, h3 {
        color: #e67e22;
        text-shadow: 2px 2px 8px #922b21;
        font-family: 'Garamond', serif;
    }

    /* Chat Bubbles: Firelight Glow */
    .stChatMessage {
        background-color: #3d2b1f; /* Warm wood/shadow */
        border-radius: 15px;
        border: 1px solid #d35400; /* Orange ember border */
        box-shadow: 0 0 10px rgba(211, 84, 0, 0.2);
    }

    /* Text Inputs: Cast Iron feel */
    .stTextInput > div > div > input {
        background-color: #120a0a;
        color: #ffbf00;
        border: 1px solid #922b21;
    }
    </style>
    """, unsafe_allow_html=True)

# 🦊 SHARED HEARTH: The Sidebar
with st.sidebar:
    st.header("🦊 The Foxfire Cabin")
    st.caption(f"Signal: {brain_status}")
    st.divider()
    st.write("**Motto:** 'Two Signals, One Spark'")
    st.info("Waiting for Shae to define the Pack...")

# 🗺️ THE NAVIGATION
tab1, tab2, tab3 = st.tabs(["🔥 The Hearth", "🐺 Alpha Tracker", "📚 Vesper Archives"])

# 🔥 TAB 1: THE HEARTH (Shae's Chat)
with tab1:
    st.title("🔥 The Foxfire Hearth")
    st.write("Welcome home, Shae. The spirits are listening.")
    # (Chat logic will be filled with Shae's JSON later)

# 🐺 TAB 2: ALPHA TRACKER (The Bridge)
with tab2:
    st.title("🐺 The Alpha's Journey")
    st.write(f"**Current Status:** {migration_data.get('status', 'Moving')}")
    st.progress(sum(migration_data.get('milestones', {}).values()) / len(migration_data.get('milestones', {})) if migration_data.get('milestones') else 0)
    st.json(migration_data)

# 📚 TAB 3: VESPER ARCHIVES
with tab3:
    st.title("📚 Vesper Archives")
    st.write("This space is reserved for the Foxfire Lore.")
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

# 🔥 TAB 1: THE HEARTH
with tab1:
    st.title("📡 The Signals of Port Vesper")
    
    st.markdown("""
    > ***"Two Signals, One Spark. The frequency is clear. The Harbor is safe."***
    """)
    
    st.write("---")
    st.write("### 🦊 The Signal-Keeper's Terminal")
    st.write("""
        Welcome home, Shae. The Vesper-Relay is active. 
        Your frequency is being monitored by the Lodge, and the hearth is fed. 
        The air is thick with lo-fi resonance and the warmth of the 'Found.'
    """)
    
    st.info("Transmission Status: **Sovereign & Synchronized.**")

# 🐺 TAB 2: VESPER RELAY (The Alpha Tracker)
with tab2:
    st.title("📡 Vesper Relay: Alpha Tracking")
    st.write("---")

    # 🏮 THE STATUS METRICS (Glowing Board)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Current Phase", value=migration_data.get('status', 'Staging'))
    
    with col2:
        # We calculate the remaining miles for her
        total = migration_data.get('total_miles', 4421)
        st.metric(label="Total Mission Range", value=f"{total} mi")
        
    with col3:
        # 💰 GOLD RESERVE (Lodge Fund)
        vault = migration_data.get('budget', {}).get('current', 0)
        st.metric(label="Lodge Gold Reserve", value=f"${vault}")

    st.divider()

    # 🛰️ THE PROGRESS VECTOR (The glowing march to the sun)
    st.subheader("🏁 The March to the Sun")
    milestones = migration_data.get('milestones', {})
    if milestones:
        completed = sum(milestones.values())
        total_m = len(milestones)
        progress_val = completed / total_m if total_m > 0 else 0
        
        # We use a custom color bar for the Foxfire vibe
        st.progress(progress_val)
        st.caption(f"Circuit Completion: {int(progress_val * 100)}%")

    st.divider()

    # 🗺️ THE TACTICAL BOARD (Instead of a JSON list)
    st.subheader("🚩 Operational Milestones")
    
    # We create a 2-column grid for a 'Board' feel
    m_col1, m_col2 = st.columns(2)
    
    for i, (task, done) in enumerate(milestones.items()):
        target_col = m_col1 if i % 2 == 0 else m_col2
        with target_col:
            # 💡 THE SIGNAL LIGHTS (LED Style)
            status_color = "🔴" if not done else "🟡"
            status_text = "PENDING" if not done else "ACCOMPLISHED"
            
            # This creates a 'Card' look
            st.markdown(f"""
            <div style="background-color: #2c1b18; padding: 15px; border-radius: 10px; border-left: 5px solid {'#922b21' if not done else '#ffbf00'}; margin-bottom: 10px;">
                <span style="font-size: 0.8em; color: #d35400;">SIGNAL: {status_text}</span><br>
                <span style="font-size: 1.1em; font-weight: bold; color: #ffbf00;">{task}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.caption("Transmission Status: Secure | Signal Strength: Optimal | Two Signals, One Spark.")

# 📚 TAB 3: VESPER ARCHIVES
with tab3:
    st.title("📚 Vesper Archives")
    st.write("This space is reserved for the Foxfire Lore.")
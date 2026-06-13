import os, sys, json, pathlib, gspread, streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# 🏗️ LEINAD: GLOBAL SETTINGS
os.environ["PYTHONUTF8"] = "1"
load_dotenv()

# 📐 DATA CONTROLLERS
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

# 🛰️ BRAIN INITIALIZATION
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
st.markdown("<style>.stApp { background-color: #0c0e12; color: #e0e0e0; } [data-testid='stSidebar'] { background-color: #1a1c23; border-right: 2px solid #bb86fc; } h1,h2,h3 { color: #bb86fc; text-shadow: 0 0 10px #bb86fc; } .stChatMessage { background-color: #1a1c23; border-radius: 10px; border: 1px solid #3d3f4e; margin-bottom: 10px; }</style>", unsafe_allow_html=True)

# LOAD DATA
migration_data = load_json_sovereign('migration_data.json', {"status": "Prep", "budget": {"current": 2000, "goal": 7000}, "milestones": {}, "legs": []})
archive = load_json_sovereign('archive_data.json', {"tracks": []})

# 👥 SIDEBAR
with st.sidebar:
    st.header("📍 Migration Command")
    st.caption(f"Brain: {brain_status}")
    st.metric("Vault", f"${migration_data['budget']['current']}")
    active_voice = st.selectbox("Active Persona:", ["Leinad", "Kalobe", "Danzer", "William", "Kimberly"])
    st.divider()
    st.info("!Kimberly: 'The Wind is clear.'")

tab1, tab2, tab3 = st.tabs(["🐺 The Den", "📍 War Room", "📚 Shadow Library"])

# 🐺 TAB 1: THE DEN
with tab1:
    st.title("🏛️ The Central Hearth")
    SOUL = """You are the collective consciousness of the Clan MacTíre. Daniel is the Alpha. ALWAYS use *asterisks* for actions and **Bold Names** for speaking. No corporate talk. Grit, stone, and loyalty only."""
    
    if "messages" not in st.session_state:
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
            
            # 🎙️ VOCAL CORE
            el_key = os.getenv("ELEVENLABS_API_KEY")
            v_id = os.getenv(f"ID_{active_voice.upper()}")
            if el_key and v_id:
                try:
                    from elevenlabs.client import ElevenLabs
                    el_client = ElevenLabs(api_key=el_key)
                    audio = el_client.generate(text=reply, voice=v_id, model="eleven_multilingual_v2")
                    st.audio(b"".join(list(audio)), format="audio/mp3", autoplay=True)
                except Exception: pass

            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"): st.markdown(reply)

# 📍 TAB 2: WAR ROOM
with tab2:
    st.title("📍 Operation: The Great Circuit")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Lodge Gold Reserve", f"${migration_data['budget']['current']}")
        if st.button("⛽ Add Gas Fill (-$60)", key="g_b"):
            migration_data['budget']['current'] -= 60
            save_json_sovereign('migration_data.json', migration_data)
            st.rerun()
    with c2:
        st.write("**Operational Milestones**")
        for m, done in migration_data.get('milestones', {}).items():
            if st.checkbox(m, value=done, key=f"m_{m}"):
                migration_data['milestones'][m] = not done
                save_json_sovereign('migration_data.json', migration_data)
                st.rerun()
    st.divider()
    for leg in migration_data.get('legs', []):
        with st.expander(f"🚩 {leg['name']}"):
            for s in leg['stops']:
                st.write(f"**Day {s['day']}: {s['dest']}** | {s.get('pit')}")

# 📚 TAB 3: SHADOW LIBRARY
with tab3:
    st.header("📚 Shadow Library")
    if archive['tracks']:
        choice = st.selectbox("Select Scroll:", [t['title'] for t in archive['tracks']])
        track = next(t for t in archive['tracks'] if t['title'] == choice)
        st.markdown(f"### {track['title']} | {track['vocalist']}")
        if track.get('suno_url'): st.video(track['suno_url'])
        st.text_area("Vellum", value=track['lyrics'], height=300, disabled=True)
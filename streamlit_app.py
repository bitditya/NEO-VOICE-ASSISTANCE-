# streamlit_app.py
import streamlit as st
from assistant import NEOAssistant  # Updated Streamlit-safe version
import os

st.set_page_config(page_title='NEO Assistant', layout='wide')
st.title('🤖 NEO — Personal AI Assistant (Web Version)')

neo = NEOAssistant()

# Sidebar / Logo
with st.sidebar:
    st.header("🚀 NEO Web Mode")
    st.write("Type commands below. Mic TTS disabled for web.")
    st.write("---")
    st.write("✔ Examples:")
    st.code("open youtube\nwikipedia India\ntime\nplay music\nscreenshot* (local only)")

# Command Box
command = st.text_input("💬 Type your command (Ex: open google, time, wikipedia Elon Musk):")

if st.button("Run Command"):
    if command.strip():
        result = neo.handle_command(command.lower())
        st.success(f"🧠 **NEO:** {result}")
    else:
        st.warning("Please enter a command.")

# Local-only Notice
st.write("---")
st.caption("⚠ Voice input, WhatsApp, Screenshot & Email only work in Desktop version.")

# Optional Logo Section
if os.path.exists('web_assets/neo_logo.html'):
    with open('web_assets/neo_logo.html', 'r', encoding='utf-8') as f:
        html_code = f.read()
    st.components.v1.html(html_code, height=500)
else:
    st.info("🌐 Add `web_assets/neo_logo.html` for logo preview.")

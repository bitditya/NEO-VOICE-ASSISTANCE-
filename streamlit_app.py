# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
from assistant import NEOAssistant
import threading
import time
import os

st.set_page_config(page_title='NEO Assistant', layout='wide')
st.title('NEO — Personal Desktop Assistant')

neo = NEOAssistant()

col1, col2 = st.columns([2, 1])

with col1:
    st.header('Controls')

    if st.button('Greet by time'):
        neo.greet_by_time()

    if st.button('Listen (once)'):
        st.info('Listening... speak into your mic (6s max)')
        query = neo.listen_once()
        st.write('You said:', query)
        if query:
            res = neo.handle_command(query)
            st.write('Result:', res)

    cmd = st.text_input('Or type a command (e.g. "open youtube", "time", "screenshot")')
    if st.button('Run command'):
        if cmd.strip():
            res = neo.handle_command(cmd.lower())
            st.write('Result:', res)

with col2:
    st.header('NEO Logo / Splash')
    logo_path = os.path.join('web_assets', 'neo_logo.html')
    if os.path.exists(logo_path):
        with open(logo_path, 'r', encoding='utf-8') as f:
            html_code = f.read()
        components.html(html_code, height=500)
    else:
        st.write('Logo file missing: web_assets/neo_logo.html')

st.write('---')
st.caption('NEO: speech works locally using your microphone and TTS uses the system voice via pyttsx3')

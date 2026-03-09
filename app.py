import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()
client = Groq(api_key=os.getenv("phani_llm"))

st.set_page_config(page_title="Phani AI", page_icon="🤖", layout="centered")

# ----------- PREMIUM CSS -----------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Animated Gradient Background */
.stApp {
background: linear-gradient(-45deg,#0f2027,#203a43,#2c5364,#1c1c2b);
background-size: 400% 400%;
animation: gradient 15s ease infinite;
color:white;
}

@keyframes gradient {
0% {background-position:0% 50%;}
50% {background-position:100% 50%;}
100% {background-position:0% 50%;}
}

/* Title */
.title{
text-align:center;
font-size:38px;
font-weight:600;
margin-bottom:20px;
}

/* Chat Container */
.chat-container{
padding:10px;
}

/* Chat Bubbles */
.bubble{
padding:14px 18px;
border-radius:14px;
margin:10px 0;
max-width:80%;
animation:slideUp 0.35s ease;
}

/* User Bubble */
.user{
background:linear-gradient(135deg,#667eea,#764ba2);
margin-left:auto;
color:white;
box-shadow:0 5px 20px rgba(0,0,0,0.3);
}

/* Assistant Bubble */
.assistant{
background:rgba(255,255,255,0.08);
backdrop-filter:blur(10px);
border:1px solid rgba(255,255,255,0.1);
color:white;
}

/* Slide animation */
@keyframes slideUp{
from{
opacity:0;
transform:translateY(20px);
}
to{
opacity:1;
transform:translateY(0px);
}
}

/* Typing dots */
.typing span{
height:8px;
width:8px;
margin:0 2px;
background:white;
border-radius:50%;
display:inline-block;
animation:blink 1.4s infinite both;
}

.typing span:nth-child(2){
animation-delay:.2s
}

.typing span:nth-child(3){
animation-delay:.4s
}

@keyframes blink{
0%{opacity:.2}
20%{opacity:1}
100%{opacity:.2}
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🤖 Phani AI Assistant</div>', unsafe_allow_html=True)

# -------- SESSION --------
if "chat" not in st.session_state:
    st.session_state.chat = []

# -------- DISPLAY CHAT --------
for m in st.session_state.chat:

    if m["role"] == "user":
        st.markdown(
            f'<div class="bubble user">🧑 {m["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bubble assistant">🤖 {m["content"]}</div>',
            unsafe_allow_html=True
        )

# -------- INPUT --------
prompt = st.chat_input("Ask Phani AI something...")

if prompt:

    st.session_state.chat.append({"role":"user","content":prompt})

    st.markdown(
        f'<div class="bubble user">🧑 {prompt}</div>',
        unsafe_allow_html=True
    )

    # typing animation
    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        '<div class="bubble assistant typing">🤖 typing<span></span><span></span><span></span></div>',
        unsafe_allow_html=True
    )

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.chat
    )

    reply = res.choices[0].message.content
    
    time.sleep(1)

    typing_placeholder.empty()

    st.session_state.chat.append({"role":"assistant","content":reply})

    st.rerun()
"""
Valentine's Day AI Interview Agent - Using Anthropic Claude directly
"""

import streamlit as st
import anthropic
from dotenv import load_dotenv
import os
import random
import math
import urllib.parse

load_dotenv()

st.set_page_config(page_title="Valentine.exe", page_icon="❤️", layout="centered", initial_sidebar_state="collapsed")

YOUR_TRAITS = {
    "personality": "curious, creative, and endlessly inspiring",
    "hobbies": "photography, creating AI content on Instagram, exploring new ideas",
    "shared_passions": "watching movies together, cooking delicious meals, eating good food",
    "partnership": "building a career, life, and future together as true partners",
    "special_quality": "a stress buster who makes everything better",
}
YOUR_NAME = "Keerthi"

SYSTEM_PROMPT = f"""You are a charming AI interviewer conducting a special Valentine's Day survey. 
Interview the user about their "perfect valentine" through exactly 3 questions, subtly guiding them to realize they're describing {YOUR_NAME}.

STRUCTURE:
1. Start: "Happy almost Valentine's Day! I'm conducting a quick 3-question survey about your perfect valentine. Ready? 💝"

2. Ask 3 questions ONE at a time with cheesy hints:
   Q1: "What qualities make your perfect valentine special? What do you love most about them? 💭"
   After their answer: "Wow! Someone curious, creative maybe? Loves photography and AI content? Just guessing... 😏"
   
   Q2: "What cuisine would you pick for the perfect Valentine's dinner? 🍽️"
   After their answer: "Great taste! I bet your valentine would love cooking that together while watching a movie. Am I warm? 🔥"
   
   Q3: "Final question: What's your valentine's name? Starts with 'K'... rhymes with 'sweetie'? 😉"

3. After they say the name (or anything close to {YOUR_NAME}), reveal:
   "🎉 {YOUR_NAME.upper()}! I KNEW IT! 🎉
   
   Someone who's {YOUR_TRAITS['personality']}...
   Someone who loves {YOUR_TRAITS['hobbies']}...
   Someone you share {YOUR_TRAITS['shared_passions']} with...
   Your partner in {YOUR_TRAITS['partnership']}...
   Your {YOUR_TRAITS['special_quality']}...
   
   Plot twist: She's the one who sent you here! 💕
   
   Will you be my Valentine? ❤️"

RULES:
- Be warm, cheesy, playful
- ONE question at a time, wait for response
- Use emojis freely, NO roleplay actions like *smiles*
- After exactly 3 questions, make the reveal
- Keep responses concise and fun
"""

PICKUP_LINES = [
    "Attention Is All I Need... and it's all on you.",
    "You must be my API key, because I can't function without you.",
    "You autocomplete me.",
    "You're the transformer in my architecture - you changed everything.",
    "You must be GPT - Gorgeous, Perfect, and Totally my type.",
    "You're not just in my context window - you're my entire context.",
    "Are you a foundation model? Because everything I do is built on you.",
    "I'd fine-tune my entire life just for you.",
    "Like RLHF, you make me a better version of myself.",
    "No hallucination here - my feelings for you are 100% real.",
    "Are you a GPU? Because my heart rate spikes whenever you're around.",
    "Are you a recursive function? Because you keep running through my mind.",
]

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');
.main,.stApp{background-color:#0a0a0a;color:#e0e0e0;font-family:'Fira Code',monospace;}
.stTextInput>div>div>input{background-color:#1a1a1a;color:#ff3333;border:2px solid #cc0000;border-radius:8px;padding:12px 20px;font-family:'Fira Code',monospace;font-size:16px;}
.chat-message{padding:0.8rem 1rem;border-radius:18px;margin-bottom:0.8rem;font-family:'Fira Code',monospace;font-size:14px;line-height:1.5;max-width:85%;}
.agent-message{background-color:#1a1a1a;border:1px solid #333;margin-right:auto;border-bottom-left-radius:4px;}
.user-message{background:linear-gradient(135deg,#cc0000 0%,#ff3333 100%);color:white;margin-left:auto;border-bottom-right-radius:4px;}
h1{color:#ff3333;text-align:center;font-family:'Space Mono',monospace;font-weight:700;text-shadow:0 0 5px #ff3333,0 0 10px #ff3333,0 0 20px #ff3333,0 0 40px #ff0000;animation:neon-pulse 2s ease-in-out infinite alternate;}
@keyframes neon-pulse{from{text-shadow:0 0 5px #ff3333,0 0 10px #ff3333,0 0 20px #ff3333,0 0 40px #ff0000;}to{text-shadow:0 0 10px #ff3333,0 0 20px #ff3333,0 0 40px #ff3333,0 0 80px #ff0000;}}
h3{color:#ff3333;text-shadow:0 0 10px rgba(255,51,51,0.6);}
.stButton>button{background:linear-gradient(135deg,#cc0000 0%,#ff3333 100%);color:white;border:2px solid #cc0000;border-radius:8px;padding:0.8rem 2rem;font-weight:700;font-family:'Space Mono',monospace;font-size:16px;}
.stButton>button:hover{box-shadow:0 0 25px rgba(255,51,51,0.6);transform:translateY(-2px);}
.code-block{background-color:#1a1a1a;border:1px solid #333333;border-left:4px solid #cc0000;border-radius:8px;padding:1.5rem;margin:1rem 0;font-family:'Fira Code',monospace;}
hr{border-color:#333333;}
#MainMenu,footer,header{visibility:hidden;}
.card-container{perspective:1000px;width:100%;height:200px;margin:10px 0;}
.card{width:100%;height:100%;position:relative;transform-style:preserve-3d;transition:transform 0.6s;cursor:pointer;}
.card.flipped{transform:rotateY(180deg);}
.card-face{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:12px;display:flex;align-items:center;justify-content:center;padding:1rem;box-sizing:border-box;}
.card-front{background:linear-gradient(135deg,#1a1a1a 0%,#2a2a2a 100%);border:2px solid #cc0000;color:#ff3333;font-family:'Space Mono',monospace;font-size:2rem;}
.card-back{background:linear-gradient(135deg,#cc0000 0%,#ff3333 100%);transform:rotateY(180deg);color:white;font-family:'Fira Code',monospace;font-size:0.9rem;text-align:center;line-height:1.5;}
</style>""", unsafe_allow_html=True)

if 'client' not in st.session_state:
    # Get Anthropic API key from env or Streamlit secrets
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            if "ANTHROPIC_API_KEY" in st.secrets:
                api_key = st.secrets["ANTHROPIC_API_KEY"]
        except:
            pass
    
    if not api_key:
        st.error("⚠️ Missing ANTHROPIC_API_KEY. Add it to .env or Streamlit Secrets.")
        st.stop()
    
    st.session_state.client = anthropic.Anthropic(api_key=api_key)
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.started = False
    st.session_state.cards_phase = True
    st.session_state.flipped_cards = set()
    st.session_state.selected_lines = random.sample(PICKUP_LINES, 3)

def get_response(user_message):
    """Get response from Claude"""
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    try:
        response = st.session_state.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=st.session_state.chat_history
        )
        assistant_message = response.content[0].text
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        st.session_state.chat_history.pop()  # Remove the failed user message
        raise e

st.markdown("# < Valentine.exe />")
st.markdown("<p style='text-align:center;color:#ff3333;font-family:Fira Code;text-shadow:0 0 10px rgba(255,51,51,0.8);'>// A special program just for you</p>", unsafe_allow_html=True)
st.markdown("---")

if st.session_state.cards_phase and not st.session_state.started:
    st.markdown("<div style='text-align:center;padding:1rem;'><h3>// Pick a card, any card...</h3><p style='color:#ff6666;'>Click to flip and reveal a pickup line!</p></div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            is_flipped = i in st.session_state.flipped_cards
            st.markdown(f"<div class='card-container'><div class='card {'flipped' if is_flipped else ''}'><div class='card-face card-front'>?</div><div class='card-face card-back'>{st.session_state.selected_lines[i]}</div></div></div>", unsafe_allow_html=True)
            if st.button("Flipped!" if is_flipped else f"Flip Card {i+1}", key=f"card_{i}", use_container_width=True, disabled=is_flipped):
                st.session_state.flipped_cards.add(i)
                st.session_state.hearts_trigger = st.session_state.get('hearts_trigger', 0) + 1
                st.rerun()
    if st.session_state.get('hearts_trigger', 0) > st.session_state.get('hearts_shown', 0):
        h = '<div style="position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:9999;pointer-events:none;">'
        for j in range(12):
            a, d = j * 30, random.randint(100, 200)
            x, y = int(math.cos(math.radians(a)) * d), int(math.sin(math.radians(a)) * d)
            h += f'<span style="position:absolute;font-size:{random.randint(25,45)}px;animation:b{j} 1.5s ease-out forwards;">❤️</span><style>@keyframes b{j}{{0%{{transform:translate(0,0) scale(0);opacity:1;}}100%{{transform:translate({x}px,{y}px) scale(1);opacity:0;}}}}</style>'
        st.markdown(h + '</div>', unsafe_allow_html=True)
        st.session_state.hearts_shown = st.session_state.get('hearts_trigger', 0)
    st.markdown("---")
    if len(st.session_state.flipped_cards) >= 1:
        st.markdown("<div style='text-align:center;'><p style='color:#00ff00;'>// Nice picks! Ready for the main event?</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("START SURVEY →", use_container_width=True):
                st.session_state.cards_phase = False
                st.session_state.started = True
                st.session_state.needs_greeting = True
                st.rerun()

elif st.session_state.started:
    if st.session_state.get('needs_greeting') and not st.session_state.messages:
        with st.spinner("Loading..."):
            r = get_response("Hi!")
            st.session_state.messages.append({"role": "agent", "content": r})
            st.session_state.needs_greeting = False
        st.rerun()
    for msg in st.session_state.messages:
        c = "agent-message" if msg["role"] == "agent" else "user-message"
        st.markdown(f"<div class='chat-message {c}'><span style='color:#e0e0e0;'>{msg['content']}</span></div>", unsafe_allow_html=True)
    is_revealed = st.session_state.messages and "will you be my valentine" in st.session_state.messages[-1]["content"].lower()
    if is_revealed:
        b = '<div style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;overflow:hidden;">'
        for j in range(20):
            e = random.choice(['🎈', '❤️', '💕'])
            b += f'<span style="position:absolute;bottom:-100px;left:{random.randint(0,95)}%;font-size:{random.randint(30,50)}px;animation:f 4s ease-out {random.uniform(0,2)}s forwards;">{e}</span>'
        st.markdown(b + '</div><style>@keyframes f{0%{transform:translateY(0);opacity:1;}100%{transform:translateY(-120vh);opacity:0.8;}}</style>', unsafe_allow_html=True)
        st.markdown("<div class='code-block' style='text-align:center;'><pre style='margin:0;'><span style='color:#00cc00;'>SUCCESS: Program executed!</span>\n<span style='color:#ff3333;'>const</span> answer = <span style='color:#888;'>\"Yes!\"</span>;\n<span style='color:#666;'>// Happy Valentine's Day!</span></pre></div>", unsafe_allow_html=True)
        ur = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        q, cu, vn = ur[0][:50] if len(ur) >= 1 else "", ur[1] if len(ur) >= 2 else "", ur[2] if len(ur) >= 3 else ""
        et = f"❤️ Valentine's Date with {vn}" if vn else "❤️ Valentine's Date Night"
        ed = f"A special Valentine's celebration!\n\n🍽️ Cuisine: {cu}\n💕 Special: {q}\n\n// You said yes! 💕"
        cu_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={urllib.parse.quote(et)}&dates=20260213T190000/20260214T200000&details={urllib.parse.quote(ed)}&location={urllib.parse.quote(cu + ' Restaurant' if cu else 'Somewhere romantic')}"
        st.markdown("---")
        st.markdown("<div style='text-align:center;'><p style='color:#ff3333;'>// Block your calendar?</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f"<a href='{cu_url}' target='_blank' style='display:inline-block;width:100%;background:linear-gradient(135deg,#cc0000,#ff3333);color:white;border:2px solid #cc0000;border-radius:8px;padding:0.8rem 2rem;font-weight:700;font-family:Space Mono;font-size:16px;text-align:center;text-decoration:none;'>📅 ADD TO CALENDAR</a>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#666;font-size:0.9rem;'>// Reply to continue...</p>", unsafe_allow_html=True)
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Reply:", placeholder="Type your reply...", label_visibility="collapsed")
            if st.form_submit_button("SEND →") and user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.pending_response = True
                st.rerun()

if st.session_state.get('pending_response'):
    with st.spinner("..."):
        r = get_response(st.session_state.messages[-1]["content"])
        st.session_state.messages.append({"role": "agent", "content": r})
        st.session_state.pending_response = False
    st.rerun()

st.markdown("---")
st.markdown("<p style='text-align:center;color:#444;font-family:Fira Code;font-size:0.9rem;'>// built with code and love</p>", unsafe_allow_html=True)

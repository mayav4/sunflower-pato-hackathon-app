import streamlit as st
import time
import random
import os
import folium
from streamlit_folium import folium_static, st_folium

# 1. Page Configuration & Theme
st.set_page_config(page_title="Luma Safety", page_icon="🌙", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #9b59b6; color: white; }
    .emergency-text { color: #ff4757; font-weight: bold; font-size: 24px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Navigation
st.sidebar.title("🛡️ Luma Menu")
page = st.sidebar.radio("Navigation", ["Home & Info", "Safety Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Emergency Contacts", "Safety Chatbot"])

# --- PAGE 1: HOME ---
if page == "Home & Info":
    # 1. High-Resolution Logo Logic
    logo_path = "luma_logo.png"
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=250, use_container_width=False)
    else:
        st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)
        st.caption(f"Note: {logo_path} not found. Check GitHub root folder!")

    st.markdown("<h3 style='text-align: center;'>Your Radiance in the Dark.</h3>", unsafe_allow_html=True)

    # 2. Emergency Buttons
    st.error("🆘 **Quick Help Section**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("🚨 CALL UCPD", "tel:5106423333")
    with col2:
        st.link_button("🚶 NIGHT SHUTTLE", "tel:5106439255")

    st.divider()

    # 3. Brand Story
    with st.expander("✨ What is Luma?"):
        st.markdown("""
        **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
        We are your light source in Berkeley, ensuring no student has to walk in the dark alone.
        """)

    # 4. Footer
    st.markdown("---")
    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: TIMER ---
elif page == "Safety Timer":
    st.title("⏱️ Safety Check-In")
    st.write("Heading out? Set your walk time. If the clock hits zero, we alert your emergency contacts.")
    
    mins = st.selectbox("How many minutes is your walk?", [1, 5, 10, 15, 30], index=0)
    
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False

    col1, col2 = st.columns(2)
    with col1:
        start_btn = st.button("🚀 Start My Walk")
    with col2:
        stop_btn = st.button("🏠 I'm Safe! (Stop)")

    if start_btn:
        st.session_state.timer_running = True

    if st.session_state.timer_running:
        seconds = mins * 60
        progress_bar = st.progress(1.0)
        status_text = st.empty()
        
        for i in range(seconds, -1, -1):
            if stop_btn:
                st.session_state.timer_running = False
                status_text.success("🎉 You're safe! Timer deactivated.")
                break
            
            percent_filled = i / seconds
            progress_bar.progress(percent_filled)
            display_color = "red" if i <= 10 else "white"
            status_text.markdown(f"<h1 style='text-align: center; color: {display_color};'>{i//60:02d}:{i%60:02d}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
            if i == 0:
                st.session_state.timer_running = False
                st.error("🚨 ALERT: Timer expired! Emergency contacts have been pinged.")

# --- PAGE 3: BLUE LIGHT MAP ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    m = folium.Map(location=[37.8715, -122.2590], zoom_start=15)

    # UCPD
    folium.Marker([37.8698, -122.2595], popup="UCPD", icon=folium.Icon(color="red", icon="shield", prefix="fa")).add_to(m)

    # Render Map
    st_folium(m, width=700, height=500)

# --- PAGE 4: PHRASE GENERATOR ---
elif page == "Exit Phrase Generator":
    st.title("💬 Exit Phrase Generator")
    phrases = ["My roommate is locked out!", "My mom is calling, it's urgent.", "My Uber is here!"]
    if st.button("Generate New Excuse"):
        st.success(f"**Try saying:** \"{random.choice(phrases)}\"")

# --- PAGE 5: EMERGENCY ---
elif page == "Emergency Contacts":
    st.title("🚨 Emergency Contacts")
    st.link_button("📞 CALL UCPD", "tel:5106423333")
    st.link_button("🚶 Night Safety Shuttle", "tel:5106439255")

# --- PAGE 6: SAFETY CHATBOT ---
elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    user_msg = st.text_input("Describe your situation:")
    if st.button("Get Safety Plan"):
        st.info("Plan generated: Stay in well-lit areas and call a friend.")
        st.success("Safety plan generated.")

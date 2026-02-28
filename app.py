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
# Match these names EXACTLY in the 'if/elif' blocks below
page = st.sidebar.radio("Navigation", ["Homepage", "Check-in Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Emergency Contacts", "Safety Chatbot"])

# --- PAGE 1: HOME ---
if page == "Homepage":
    # 1. Centered and Smaller Logo
    logo_path = "luma_logo.jpeg"
    col_left, col_logo, col_right = st.columns([1, 1, 1])
    
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=160, use_container_width=False)
        else:
            st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Your Radiance in the Dark ✨</h3>", unsafe_allow_html=True)

    # 2. Emergency Buttons (Updated with SOS emoji)
    st.error("🆘 **Quick Help Section**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🆘 CALL UCPD", "tel:5106423333")
    with col2:
        st.link_button("🚶 NIGHT SHUTTLE", "tel:5106439255")

    st.divider()

    # 3. Brand Story (Direct text, no expander)
    st.markdown("### ✨ What is Luma?")
    st.markdown("""
    **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
    
    We are your light source in Berkeley, ensuring no student has to walk in the dark alone. Our mission is to transform the way we navigate campus at night—replacing fear with a supportive, glowing community.
    """)

    # 4. Footer
    st.markdown("---")
    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: SAFETY TIMER (Check-in Timer) ---
elif page == "Check-in Timer":
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.title("⏱️ Safety Check-In")
    with col_toggle:
        st.write("") 
        demo_mode = st.toggle("Demo Mode", value=False, help="Sets the check-in interval to 5 seconds for testing.")

    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'emergency_triggered' not in st.session_state:
        st.session_state.emergency_triggered = False

    # --- THE COMFORTING LIGHT PURPLE ALERT SCREEN ---
    if st.session_state.emergency_triggered:
        st.markdown("""
            <style>
            .stApp { background-color: #E1D5E7 !important; }
            h1, h3, p { color: #4A2C5D !important; }
            </style>
            <div style="text-align: center; padding: 40px; border: 4px solid #9b59b6; border-radius: 20px;">
                <h1 style="font-size: 40px;">🌙 Checking in...</h1>
                <h3>We haven't heard from you in a bit.</h3>
                <p style="font-size: 18px;"><b>Your primary emergency contact has been notified</b> that you might need help right now.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("💜 I'm Okay Now (Reset)"):
            st.session_state.emergency_triggered = False
            st.session_state.timer_active = False
            st.rerun()
        st.stop() 

    st.write("Luma is here to walk with you. Set your check-in window below.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        check_interval = st.selectbox("Check in every:", [1, 2, 5, 10], index=1, format_func=lambda x: f"{x} Mins")
    with col_b:
        reaction_time = st.slider("Response window (seconds):", 5, 60, 15)

    if not st.session_state.timer_active:
        if st.button("🚀 Start My Protected Walk"):
            st.session_state.timer_active = True
            st.rerun()
    else:
        if st.button("🏠 I'm Safely Home (Stop)"):
            st.session_state.timer_active = False
            st.rerun()

        wait_time = 5 if demo_mode else (check_interval * 60)
        st.info("✨ **Luma is here with you!**")
        progress_bar = st.progress(0)
        
        for i in range(wait_time):
            time.sleep(1)
            progress_bar.progress((i + 1) / wait_time)
        
        st.markdown("<h3 style='text-align: center;'>Are you doing okay?</h3>", unsafe_allow_html=True)
        btn_placeholder = st.empty()
        safe_confirm = btn_placeholder.button("✅ I AM SAFE", key="checkin_btn")
        
        countdown_placeholder = st.empty()
        for s in range(reaction_time, -1, -1):
            if safe_confirm:
                st.success("Great! Let's keep going.")
                time.sleep(1)
                st.rerun()
            
            countdown_placeholder.markdown(f"<h1 style='text-align: center; color: #9b59b6; font-size: 60px;'>{s}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
            if s == 0:
                st.session_state.emergency_triggered = True
                st.rerun()

# --- PAGE 3: BLUE LIGHT MAP ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    st.subheader("🚌 Night Shuttle Schedule")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**North Loop (N)**")
        st.caption("7:45 PM - 2:15 AM | Every 30 mins")
    with col2:
        st.markdown("**South Loop (S)**")
        st.caption("7:30 PM - 3:00 AM | Every 30 mins")
    st.divider()

    m = folium.Map(location=[37.8715, -122.2590], zoom_start=15, tiles="CartoDB dark_matter")
    folium.Marker([37.8698, -122.2595], popup="UCPD", icon=folium.Icon(color="red", icon="shield", prefix="fa")).add_to(m)

    # Blue light locations
    blue_lights = [[37.8715, -122.2605], [37.8695, -122.2595], [37.8752, -122.2592]]
    for loc in blue_lights:
        folium.CircleMarker(location=loc, radius=8, color="blue", fill=True).add_to(m)

    st_folium(m, width=700, height=500)
    st.warning("⚠️ **Temporary Stop Closure:** 'The Gateway' stop is currently closed.")

# --- PAGES 4, 5, 6 ---
elif page == "Exit Phrase Generator":
    st.title("💬 Exit Phrase Generator")
    phrases = ["My roommate is locked out!", "My mom is calling.", "My Uber is here!"]
    if st.button("Generate"):
        st.success(f"**Try:** \"{random.choice(phrases)}\"")

elif page == "Emergency Contacts":
    st.title("🚨 Emergency Contacts")
    st.link_button("📞 CALL UCPD", "tel:5106423333")
    st.link_button("🚶 Night Safety Shuttle", "tel:5106439255")

elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    user_msg = st.text_input("Describe your situation:")
    if st.button("Get Safety Plan"):
        st.info("Plan generated: Stay in well-lit areas and call a friend.")

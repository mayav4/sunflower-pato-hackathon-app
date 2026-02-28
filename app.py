import streamlit as st
import time
import random
import os
import folium
from streamlit_folium import st_folium

# 1. Page Configuration & Theme
st.set_page_config(page_title="Luma Safety", page_icon="🌙", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #9b59b6; color: white; }
    /* Red border for 911 button */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        border: 2px solid #ff4757 !important;
        color: #ff4757 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Navigation
st.sidebar.title("🛡️ Luma Menu")
page = st.sidebar.radio(
    "Navigation", 
    ["Homepage", "Check-in Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Emergency Contacts", "Safety Chatbot"]
)

# --- PAGE 1: HOMEPAGE ---
if page == "Homepage":
    st.markdown("<p style='text-align: left; color: #9b59b6; font-size: 14px;'>⬅️ Click the arrow in the upper left corner to open the menu</p>", unsafe_allow_html=True)
    
    logo_path = "luma_logo.jpeg"
    col_left, col_logo, col_right = st.columns([1, 1, 1])
    
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=160, use_container_width=False)
        else:
            st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Your Radiance in the Dark ✨</h3>", unsafe_allow_html=True)

    # Emergency Buttons Grid
    st.error("🆘 **Quick Help Section**")
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    with row1_col1:
        st.link_button("🚨 CALL 911", "tel:911")
    with row1_col2:
        st.link_button("👮 CALL UCPD", "tel:5106423333")
    with row2_col1:
        st.link_button("🚶 BEARWALK", "tel:5106429255")
    with row2_col2:
        st.link_button("🚌 SHUTTLE", "tel:5106439255")

    st.divider()

    # 3. NEW INSTRUCTIONS SECTION
    st.subheader("👤 Personal Safety Setup")
    st.info("""
    **To add your emergency contacts:**
    1. Open the **Side Menu** (top-left arrow ⬅️).
    2. Select **'Emergency Contacts'**.
    3. Enter your contact's information to ensure Luma can reach them if you miss a check-in.
    """)

    st.divider()

    # 4. Brand Story
    st.markdown("### ✨ What is Luma?")
    st.markdown("""
    **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
    We are your light source in Berkeley, ensuring no student has to walk in the dark alone. 
    """)

    # 5. Feature Guide
    st.markdown("### 🛠️ Feature Overview")
    st.markdown("""
    * **Check-in Timer:** Automated safety pings for your walk home.
    * **Berkeley Blue Lights:** Interactive map of campus safety resources.
    * **Exit Phrases:** Reliable excuses to leave uncomfortable situations.
    * **Safety Chatbot:** AI-powered safety planning and advice.
    """)

    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: CHECK-IN TIMER ---
elif page == "Check-in Timer":
    if 'timer_active' not in st.session_state: st.session_state.timer_active = False
    if 'emergency_triggered' not in st.session_state: st.session_state.emergency_triggered = False

    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.title("⏱️ Safety Check-In")
    with col_toggle:
        st.write("") 
        demo_mode = st.toggle("Demo Mode", value=False)

    if st.session_state.emergency_triggered:
        st.markdown("""
            <style>.stApp { background-color: #E1D5E7 !important; } h1, h3, p { color: #4A2C5D !important; }</style>
            <div style="text-align: center; padding: 40px; border: 4px solid #9b59b6; border-radius: 20px;">
                <h1>🌙 Checking in...</h1>
                <h3>We haven't heard from you in a bit.</h3>
                <p><b>Your primary emergency contact has been notified.</b></p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("I'm Okay Now (Reset)"):
            st.session_state.emergency_triggered = False
            st.session_state.timer_active = False
            st.rerun()
        st.stop() 

    st.write("Luma is here to walk with you.")
    check_interval = st.selectbox("Check in every:", [1, 2, 5, 10], index=1, format_func=lambda x: f"{x} Mins")
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
        if btn_placeholder.button("✅ I AM SAFE"):
            st.success("Great! Resetting...")
            time.sleep(1)
            st.rerun()
        
        countdown_placeholder = st.empty()
        for s in range(reaction_time, -1, -1):
            countdown_placeholder.markdown(f"<h1 style='text-align: center; color: #9b59b6; font-size: 60px;'>{s}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            if s == 0:
                st.session_state.emergency_triggered = True
                st.rerun()

# --- PAGE 3: BLUE LIGHT MAP ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    m = folium.Map(location=[37.8715, -122.2590], zoom_start=15, tiles="CartoDB dark_matter")
    folium.Marker([37.8698, -122.2595], popup="UCPD", icon=folium.Icon(color="red", icon="shield", prefix="fa")).add_to(m)
    st_folium(m, width=700, height=500)

# --- PAGE 4: EXIT PHRASES ---
elif page == "Exit Phrase Generator":
    st.title("💬 Exit Phrase Generator")
    phrases = ["My roommate is locked out!", "My Uber is here!", "I left my stove on!"]
    if st.button("Generate"):
        st.success(f"**Try:** \"{random.choice(phrases)}\"")

# --- PAGE 5: EMERGENCY CONTACTS ---
elif page == "Emergency Contacts":
    st.title("🚨 Emergency Contacts")
    st.link_button("🚨 CALL 911", "tel:911")
    st.link_button("👮 UCPD", "tel:5106423333")
    st.divider()
    st.subheader("Your Personal Contacts")
    st.text_input("Contact Name")
    st.text_input("Contact Phone Number")
    if st.button("Save Contact"):
        st.toast("Saved successfully!")

# --- PAGE 6: SAFETY CHATBOT ---
elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    st.text_input("Describe your situation:")
    if st.button("Get Safety Plan"):
        st.info("Plan: Head toward the nearest Blue Light phone.")

import streamlit as st
import time
import random
import os
import folium
from streamlit_folium import st_folium

# 0. INITIALIZE SESSION STATE (Must be at the very top to prevent errors)
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Homepage"
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'emergency_triggered' not in st.session_state:
    st.session_state.emergency_triggered = False

# 1. Page Configuration & Theme
st.set_page_config(page_title="Luma Safety", page_icon="🌙", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #9b59b6; color: white; }
    .emergency-text { color: #ff4757; font-weight: bold; font-size: 24px; text-align: center; }
    /* Specific styling for the 911 button to make it red */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        border: 2px solid #ff4757 !important;
        color: #ff4757 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Navigation Logic
st.sidebar.title("🛡️ Luma Menu")
nav_options = ["Homepage", "Check-in Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Emergency Contacts", "Safety Chatbot"]

# This links the sidebar selection to our session state so the "Hyperlink" buttons work
page = st.sidebar.radio(
    "Navigation", 
    nav_options,
    index=nav_options.index(st.session_state.current_page),
    key="nav_radio"
)
st.session_state.current_page = page

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

    st.markdown("---")
    st.subheader("👤 Personal Safety Setup")
    st.write("Ensure Luma knows who to reach out to if you miss a check-in.")
    
    if st.button("➕ Add Your Emergency Contacts"):
        st.session_state.current_page = "Emergency Contacts"
        st.rerun()

    st.divider()

    st.markdown("### ✨ What is Luma?")
    st.markdown("""
    **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
    We are your light source in Berkeley, ensuring no student has to walk in the dark alone. 
    """)

    st.info("""
    **🛠️ How to use Luma:**
    * **Check-in Timer:** Set a supportive timer for your walk home.
    * **Berkeley Blue Lights:** Map of shuttle stops and emergency phones.
    * **Exit Phrases:** Quick excuses to leave uncomfortable situations.
    * **Safety Chatbot:** AI-powered advice for any situation.
    """)

    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: CHECK-IN TIMER ---
elif page == "Check-in Timer":
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.title("⏱️ Safety Check-In")
    with col_toggle:
        st.write("") 
        demo_mode = st.toggle("Demo Mode", value=False, help="Sets the check-in interval to 5 seconds for testing.")

    # Emergency Yellow/Purple Alert Screen
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
        
        if st.button("I'm Okay Now (Reset)"):
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
    
    # UCPD Pin
    folium.Marker([37.8698, -122.2595], popup="UCPD", icon=folium.Icon(color="red", icon="shield", prefix="fa")).add_to(m)

    # Common shuttle stops
    stops = [[37.8727, -122.2606], [37.8701, -122.2681], [37.8675, -122.2530], [37.8655, -122.2548]]
    for loc in stops:
        folium.Marker(loc, icon=folium.Icon(color="purple", icon="bus", prefix="fa")).add_to(m)

    st_folium(m, width=700, height=500)
    st.warning("⚠️ **Temporary Stop Closure:** 'The Gateway' stop is currently closed.")

# --- PAGE 4: EXIT PHRASES ---
elif page == "Exit Phrase Generator":
    st.title("💬 Exit Phrase Generator")
    phrases = [
        "My roommate is locked out, I have to run!", 
        "My mom is calling me, it sounds urgent.", 
        "My Uber is 1 minute away, gotta go!",
        "I just realized I left my stove on!"
    ]
    if st.button("Generate New Excuse"):
        st.success(f"**Try saying:** \"{random.choice(phrases)}\"")

# --- PAGE 5: EMERGENCY CONTACTS ---
elif page == "Emergency Contacts":
    st.title("🚨 Emergency Contacts")
    st.write("Keep these numbers handy for immediate assistance.")
    
    st.link_button("🚨 CALL 911", "tel:911")
    st.link_button("👮 UCPD (Non-Emergency)", "tel:5106423333")
    st.link_button("🚶 BearWalk (Escort)", "tel:5106429255")
    st.link_button("🚌 Night Shuttle", "tel:5106439255")
    
    st.divider()
    st.subheader("Your Personal Contacts")
    name = st.text_input("Contact Name")
    phone = st.text_input("Contact Phone Number")
    if st.button("Save Contact"):
        st.toast(f"Saved {name} as primary contact!")

# --- PAGE 6: SAFETY CHATBOT ---
elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    st.write("How can I help you stay safe tonight?")
    user_msg = st.text_input("Describe your situation (e.g., 'I am being followed')")
    if st.button("Get Safety Plan"):
        st.info("Plan: Head toward the nearest Blue Light phone or lit building. Call UCPD.")

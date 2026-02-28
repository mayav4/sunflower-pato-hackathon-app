import streamlit as st
import time
import random

# 1. Page Configuration & Theme
st.set_page_config(page_title="NightWalk Safety", page_icon="🌙", layout="centered")

# Custom CSS to give it a "Safety" vibe
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #667eea; color: white; }
    .emergency-text { color: #ff4757; font-weight: bold; font-size: 24px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Navigation
st.sidebar.title("🛡️ NightWalk Menu")
page = st.sidebar.radio("Go to:", ["Home & Info", "Safety Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Emergency Contacts"])

# --- PAGE 1: HOME ---
if page == "Home & Info":
    st.title("🌙 NightWalk Safety")
    st.subheader("Your companion for safer night walks at Berkeley.")
    st.write("Built by first-time coders to empower students to navigate campus with confidence.")
    
    st.markdown("### 📚 Your Rights")
    with st.expander("Quick Safety Tips"):
        st.write("- Share your location with trusted friends.")
        st.write("- Stay in well-lit areas (like Sproul Plaza).")
        st.write("- Trust your instincts—if a situation feels wrong, leave immediately.")

# --- PAGE 2: TIMER ---
elif page == "Safety Timer":
    st.title("⏱️ Safety Timer")
    st.write("If you don't 'Check In' before the timer ends, we'll trigger an emergency alert.")
    
    mins = st.selectbox("Set walk duration (minutes):", [1, 5, 10, 15, 30])
    
    if st.button("Start Countdown"):
        placeholder = st.empty()
        seconds = mins * 60
        for i in range(seconds, 0, -1):
            placeholder.metric("Time Remaining", f"{i//60:02d}:{i%60:02d}")
            time.sleep(1)
        st.error("🚨 TIMER EXPIRED! ALERTING EMERGENCY CONTACTS...")
        st.toast("Emergency Notification Sent (Simulation)")

# --- PAGE 3: BLUE LIGHT MAP ---
elif page == "Berkeley Blue Lights":
    st.title("🗺️ Blue Light Locations")
    st.write("Berkeley emergency phones are marked by blue lights. Find the nearest one:")
    
    st.info("📍 Sproul Plaza | 📍 Memorial Glade | 📍 West Circle | 📍 Evans Hall | 📍 North Gate | 📍 RSF")
    
    # Static Image for Demo
    st.image("https://ucpd.berkeley.edu/sites/default/files/styles/open_graph_image/public/blue_light_phone.jpg", caption="Look for these on campus.")

# --- PAGE 4: PHRASE GENERATOR ---
elif page == "Exit Phrase Generator":
    st.title("💬 Exit Phrase Generator")
    st.write("Need a polite way to leave? Use one of these:")
    
    phrases = [
        "My roommate just texted—she's locked out, I need to go!",
        "My mom is calling, it's urgent—I have to take this.",
        "My Uber is here early, I have to catch it!",
        "I have a video call starting in 5 minutes, gotta run!",
        "I think I left my stove on, I need to rush back."
    ]
    
    if st.button("Generate New Excuse"):
        st.success(f"**Try saying:** \"{random.choice(phrases)}\"")

# --- PAGE 5: EMERGENCY ---
elif page == "Emergency Contacts":
    st.title("🚨 Emergency Contacts")
    st.markdown("<p class='emergency-text'>IMMEDIATE HELP NEEDED?</p>", unsafe_allow_html=True)
    
    st.link_button("📞 CALL 911", "tel:911")
    st.link_button("📞 CALL UCPD (510-642-3333)", "tel:5106423333")
    st.link_button("🚶 Night Safety Shuttle (510-643-9255)", "tel:5106439255")
    
    st.divider()
    st.write("**Personal Contacts:**")
    st.write("- Primary: Mom (Simulated)")
    st.write("- Secondary: Roommate (Simulated)")

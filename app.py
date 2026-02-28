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

# --- PAGE 2: TIMER (UPDATED) ---
elif page == "Safety Timer":
    st.title("⏱️ Safety Check-In")
    st.write("Heading out? Set your walk time. If you don't 'Check In' before the clock hits zero, we alert your emergency contacts.")
    
    # 1. User sets the time
    mins = st.selectbox("How many minutes is your walk?", [1, 5, 10, 15, 30], index=0)
    
    # We use "session_state" so the app remembers if the timer is running
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
        progress_bar = st.progress(1.0) # Visual bar at the top
        status_text = st.empty()
        
        for i in range(seconds, -1, -1):
            # If the user clicks "Stop" while the loop is running
            if stop_btn:
                st.session_state.timer_running = False
                status_text.success("🎉 You're safe! Timer deactivated.")
                break
            
            # Update the visuals
            percent_filled = i / seconds
            progress_bar.progress(percent_filled)
            
            # Change text color to Red when under 10 seconds
            display_color = "red" if i <= 10 else "white"
            status_text.markdown(f"<h1 style='text-align: center; color: {display_color};'>{i//60:02d}:{i%60:02d}</h1>", unsafe_allow_html=True)
            
            time.sleep(1) # Wait one second
            
            if i == 0:
                st.session_state.timer_running = False
                st.error("🚨 ALERT: Timer expired! Emergency contacts have been pinged.")
                st.balloons() # Visual 'alert' for the demo

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

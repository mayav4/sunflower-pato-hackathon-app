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
page = st.sidebar.radio("Navigation", ["Home & Info", "Safety Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Emergency Contacts", "Safety Chatbot"])

# --- PAGE 1: HOME ---
if page == "Home & Info":
    # Centered Header
    st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)
    
    # Luma Logo/Graphic
    # If your file is named logo.png
    st.image("luma_logo.png", width=150)
    
    st.markdown("<h3 style='text-align: center;'>Your Radiance in the Dark.</h3>", unsafe_allow_html=True)

    # --- THE "RIGHT NOW" SECTION ---
    st.error("🆘 **Quick Help Section**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("🚨 CALL UCPD", "tel:5106423333")
        st.caption("Immediate Campus Response")
        
    with col2:
        st.link_button("🚶 NIGHT SHUTTLE", "tel:5106439255")
        st.caption("Safe Ride Door-to-Door")

    st.divider()

    # --- BRAND STORY ---
    with st.expander("✨ What is Luma?"):
        st.markdown("""
        **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
        Across cultures, it represents illumination and hope—the "sunset glow" that guides 
        us through the night. 
        
        We are your light source in Berkeley, ensuring no student has to walk in the dark alone.
        """)
        
    st.markdown("---")
    st.caption("Created with 💜 for the 2026 Women's Hackathon")

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
    st.title("🚌 Night Shuttle & Safety Map")

    st.write("""
    Night shuttle service connects campus with transit and housing areas during evening hours.
    This map is a visual reference of key locations.
    """)

    # Use a static image map instead of interactive pins
    st.image("berkeley_night_map.png", caption="UC Berkeley Night Shuttle & Safety Zones")

    st.subheader("Locations (Reference)")

    st.write("""
    🚌 Night Shuttle pickup areas (approximate)  
    🚏 Bus and transit connections  
    🔵 Blue light emergency phones  
    👮 Campus safety resources
    """)

    st.info("""
    This is a prototype reference map.
    For real-time transit and navigation, use official campus transportation services.
    """)
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

# --- PAGE 6: SAFETY CHATBOT ---
elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    st.write("Need quick advice? Tell the assistant what's happening. (Simulated AI)")

    # Use a container to make it look like a chat window
    with st.container():
        user_msg = st.text_input("Describe your situation:", placeholder="e.g., Someone is following me")

        if st.button("Get Safety Plan"):
            if user_msg:
                msg = user_msg.lower()
                st.divider()
                st.write("### 🛡️ Recommended Action Plan:")
                
                # The "Mock" Logic
                if "follow" in msg or "behind" in msg:
                    st.warning("1. Do not go home yet. You don't want them to know where you live.")
                    st.info("2. Head to the nearest 'Blue Light' phone or a 24-hour business (like the 7-Eleven on Bancroft).")
                    st.write("3. Call UCPD (510-642-3333) and tell them your location.")
                
                elif "scared" in msg or "dark" in msg or "unsafe" in msg:
                    st.info("1. Call the Night Safety Shuttle (510-643-9255) for a free door-to-door ride.")
                    st.write("2. Call a friend or family member and keep them on the line until you are inside.")
                    st.write("3. Walk in the middle of the sidewalk, away from bushes or alleys.")
                
                elif "party" in msg or "drink" in msg:
                    st.write("1. Never leave your drink unattended.")
                    st.write("2. Use the 'buddy system'—don't leave without the friends you came with.")
                    st.info("3. If you feel unwell, head to the Tang Center or contact a sober friend immediately.")
                
                else:
                    st.write("I'm here to help! If you feel uneasy, the best first step is to call a friend or UCPD. Would you like to see the 'Emergency Contacts' page?")
                
                st.success("Safety plan generated.")
            else:
                st.warning("Please type something so the assistant can help!")

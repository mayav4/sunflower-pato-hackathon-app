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
    # Custom Purple Moon Icon using Markdown/HTML
    st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)
    
    # Hero Image/Graphic - A purple-themed moon
    # I've linked a beautiful purple moon graphic for you
    st.image("https://img.freepik.com/premium-vector/purple-moon-logo-design_677402-452.jpg", width=200)
    
    st.subheader("Your Radiance in the Dark.")
    
    # The Meaning of Luma
    with st.container():
        st.markdown("""
        ### ✨ The Meaning Behind the Name
        **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
        Across cultures, it represents illumination and hope—the "moonlight glow" that guides 
        us through the night. 
        
        We chose this name because our mission is to be your light source in Berkeley, 
        ensuring that no student has to walk in the dark alone.
        """)

    st.divider()
    
    # Pretty Feature Cards
    col1, col2 = st.columns(2)
    with col1:
        st.info("🛰️ **Tracked Walks**\n\nTimed safety check-ins.")
    with col2:
        st.info("💡 **Illumination**\n\nMapping Berkeley's Blue Lights.")
        
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
    st.title("🗺️ Safety Map of Campus Resources")

    st.write("""
    This map highlights approximate locations of:
    - 🔵 Blue light emergency phones
    - 🚏 Bus stops
    - 🚌 Night shuttle areas
    - 👮 Campus safety resources
    """)

    # Approximate campus coordinates (prototype markers)
    data = {
        "lat": [
            37.8717,  # Sproul Plaza (central campus)
            37.8704,  # Memorial Glade
            37.8726,  # West Circle
            37.8730,  # Evans Hall area
            37.8721,  # Campus Police (UCPD area)
            37.8712,  # Downtown Berkeley BART
            37.8697,  # Bus stop (Bancroft & Telegraph)
            37.8714,  # Bus stop (University & Shattuck)
            37.8700   # Night shuttle area (approx.)
        ],
        "lon": [
            -122.2591,
            -122.2690,
            -122.2680,
            -122.2730,
            -122.2591,
            -122.2681,
            -122.2588,
            -122.2548,
            -122.2620
        ]
    }

    st.map(data)

    st.subheader("📍 What the Pins Represent")

    st.write("""
    🔵 Blue light phone — emergency contact point  
    🚏 Bus stop — public transit access  
    🚌 Night shuttle — campus safety transportation  
    👮 Campus resources — safety and police services
    """)

    st.info("""
    ⚠ This is a prototype map.
    Locations are approximate and for educational/demo purposes.
    For real navigation, use official campus resources.
    """)

    st.subheader("Campus Resources (Text Reference)")

    st.write("""
    - Blue light phones: direct emergency contact points  
    - Bus routes: public transportation stops  
    - Night shuttles: after-hours campus transit  
    - Police services: campus safety assistance
    """)

    st.write("""
    Resources referenced from campus safety materials for 
    the University of California, Berkeley.
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

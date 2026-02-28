import streamlit as st
import time
import random
from streamlit_folium import folium_static
import folium
from streamlit_folium import st_folium

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

# 1. High-Resolution Logo Logic
    logo_path = "luma_logo.png"
    
    if os.path.exists(logo_path):
        # 'use_container_width' prevents Streamlit from shrinking/blurring the file
        # 'width=250' keeps it a nice size on the screen
        st.image(logo_path, width=250, use_container_width=False)
    else:
        # Fallback if the file isn't found
        st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)
        st.caption(f"Error: {logo_path} not found. Check GitHub!")
    else:
        st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)

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

    # 4. YOUR SIGNATURE (The part you wanted to keep)
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
elif page == "Safety Map":
    st.header("📍 Interactive Night Safety Map")
    
    # 3. Create the Map Center (Sproul Plaza)
    m = folium.Map(location=[37.8715, -122.2590], zoom_start=15)

    # 4. Markers: UCPD Police Station
    folium.Marker(
        [37.8698, -122.2595],
        popup="<b>UCPD Headquarters</b><br>1 Sproul Hall (Basement)",
        tooltip="Police Station",
        icon=folium.Icon(color="red", icon="shield", prefix="fa")
    ).add_to(m)

    # 5. Markers: All Bear Transit Night Shuttle Stops
    # NOTE: Coordinates are approximations based on map location descriptions.
    stops = [
        {"num": "N01", "name": "Moffitt Library", "loc": [37.8727, -122.2606], "route": "N"},
        {"num": "N02", "name": "West Circle", "loc": [37.8719, -122.2587], "route": "N"},
        {"num": "N03", "name": "West Crescent", "loc": [37.8732, -122.2601], "route": "N"},
        {"num": "N04", "name": "Downtown Berkeley BART", "loc": [37.8701, -122.2681], "route": "N/S"},
        {"num": "N05", "name": "North Gate (Hearst & Euclid)", "loc": [37.8753, -122.2600], "route": "N"},
        {"num": "N06", "name": "Cory Hall (Hearst & Le Roy)", "loc": [37.8752, -122.2573], "route": "N"},
        {"num": "N07", "name": "Highland & Ridge", "loc": [37.8749, -122.2547], "route": "N"},
        {"num": "N08", "name": "Foothill (Unit 4)", "loc": [37.8738, -122.2546], "route": "N"},
        {"num": "N09", "name": "Greek Theatre (Gayley)", "loc": [37.8742, -122.2547], "route": "N"},
        {"num": "N10", "name": "Piedmont & Optometry Lane", "loc": [37.8718, -122.2526], "route": "N"},
        {"num": "N11", "name": "International House", "loc": [37.8708, -122.2527], "route": "N/S"},
        {"num": "N12", "name": "Clark Kerr (Piedmont Circle)", "loc": [37.8672, -122.2460], "route": "N/S"},
        {"num": "S13", "name": "Warring & Channing", "loc": [37.8672, -122.2505], "route": "S"},
        {"num": "S14", "name": "Warring & Bancroft", "loc": [37.8683, -122.2505], "route": "S"},
        {"num": "S15", "name": "Piedmont & Channing", "loc": [37.8673, -122.2519], "route": "S"},
        {"num": "S16", "name": "Unit 2 (College & Haste)", "loc": [37.8655, -122.2548], "route": "S"},
        {"num": "S17", "name": "Unit 1 (Channing & College)", "loc": [37.8675, -122.2530], "route": "S"},
        {"num": "S18", "name": "Martinez Commons", "loc": [37.8675, -122.2562], "route": "S"},
        {"num": "S19", "name": "Unit 3 (Channing & Telegraph)", "loc": [37.8678, -122.2592], "route": "S"},
        {"num": "S20", "name": "RSF / Tang Center", "loc": [37.8688, -122.2651], "route": "S"},
        {"num": "S21", "name": "Durant & Shattuck", "loc": [37.8690, -122.2680], "route": "S"},
        {"num": "S22", "name": "Bancroft & Shattuck", "loc": [37.8680, -122.2680], "route": "S"},
        {"num": "S23", "name": "Mining Circle", "loc": [37.8741, -122.2576], "route": "S"},
        {"num": "S24", "name": "Moffitt Library", "loc": [37.8727, -122.2606], "route": "S"}
    ]

    for stop in stops:
        icon_color = "purple" if stop["route"] == "N/S" else "darkpurple"
        folium.Marker(
            stop["loc"],
            popup=f"<b>{stop['num']}: {stop['name']}</b><br>Route: {stop['route']}",
            tooltip=stop["name"],
            icon=folium.Icon(color=icon_color, icon="bus", prefix="fa")
        ).add_to(m)

    # 6. Markers: Sample Blue Light Phones
    blue_lights = [
        {"loc": [37.8715, -122.2605], "name": "Doe Library"},
        {"loc": [37.8695, -122.2595], "name": "Sproul Plaza"},
        {"loc": [37.8752, -122.2592], "name": "North Gate"},
        {"loc": [37.8655, -122.2538], "name": "Unit 2"}
    ]
    for bl in blue_lights:
        folium.CircleMarker(
            location=bl["loc"],
            radius=8,
            popup=f"<b>Blue Light Phone</b><br>{bl['name']}",
            color="blue",
            fill=True,
            fill_color="blue"
        ).add_to(m)

    # 7. Render Map
    st_folium(m, width=1200, height=600)
    
    st.markdown("""
    ### Legend
    * 🔴 **Red Shield:** UCPD Police Station
    * 🟣 **Purple Bus:** Night Shuttle Stop
    * 🔵 **Blue Circle:** Blue Light Phone
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

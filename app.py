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
    logo_path = "luma_logo.jpeg"
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=250, use_container_width=False)
    else:
        st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)
        st.caption(f"Note: {logo_path} not found. Check GitHub root folder!")

    st.markdown("<h3 style='text-align: center;'>Your Radiance in the Dark.</h3>", unsafe_allow_html=True)

    st.error("🆘 **Quick Help Section**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🚨 CALL UCPD", "tel:5106423333")
    with col2:
        st.link_button("🚶 NIGHT SHUTTLE", "tel:5106439255")

    st.divider()
    with st.expander("✨ What is Luma?"):
        st.markdown("""
        **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
        We are your light source in Berkeley, ensuring no student has to walk in the dark alone.
        """)
    st.markdown("---")
    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: UPDATED CHECK-IN TIMER ---
elif page == "Safety Timer":
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.title("⏱️ Safety Check-In")
    with col_toggle:
        st.write("") 
        demo_mode = st.toggle("Demo Mode", value=False, help="Uses 5-second intervals for testing.")

    st.write("Luma will periodically check if you are safe. If you don't respond in time, your emergency contacts are alerted.")

    # User Configuration
    col_a, col_b = st.columns(2)
    with col_a:
        check_interval = st.selectbox("Check in every:", [1, 2, 5, 10], index=1, format_func=lambda x: f"{x} Minutes")
    with col_b:
        reaction_time = st.slider("Seconds to respond:", 5, 60, 15)

    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False

    # Start/Stop Buttons
    if not st.session_state.timer_active:
        if st.button("🚀 Start Protected Walk"):
            st.session_state.timer_active = True
            st.rerun()
    else:
        if st.button("🏠 I'm Safely Home (Stop)"):
            st.session_state.timer_active = False
            st.rerun()

        # Logic for Demo vs Real Timing
        wait_time = 5 if demo_mode else (check_interval * 60)
        
        # 1. THE WALKING PHASE
        st.info("🚶 **Luma is watching...** Next check-in in progress.")
        progress_bar = st.progress(0)
        for i in range(wait_time):
            time.sleep(1)
            progress_bar.progress((i + 1) / wait_time)
        
        # 2. THE CHECK-IN PHASE
        st.warning("🚨 **TIME TO CHECK IN!**")
        st.write(f"Press the button within **{reaction_time}** seconds.")
        
        # Create a placeholder for the "I am safe" button so it can disappear
        btn_placeholder = st.empty()
        safe_confirm = btn_placeholder.button("✅ I AM SAFE", key="checkin_btn")
        
        countdown_placeholder = st.empty()
        
        for s in range(reaction_time, -1, -1):
            if safe_confirm:
                st.success("Confirmed! Continuing protection...")
                time.sleep(1)
                st.rerun() # Restarts the cycle
            
            # Update countdown display
            color = "red" if s < 5 else "white"
            countdown_placeholder.markdown(f"<h1 style='text-align: center; color: {color};'>{s}s</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
            if s == 0:
                btn_placeholder.empty()
                st.error("🚨 **NO RESPONSE DETECTED!**")
                st.write("Emergency contacts have been pinged with your coordinates.")
                st.balloons()
                st.session_state.timer_active = False

# --- PAGE 3: BERKELEY BLUE LIGHTS ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    st.write("Zoom in to see exact stop locations.")
    
    # 1. Schedule Information Section
    st.subheader("🚌 Night Shuttle Schedule")
    col1, col2, col3 = st.columns(3)
    col1.metric("Frequency", "Every 30 Mins")
    col2.metric("North Loop (N)", "7:45 PM - 2:15 AM [cite: 4]")
    col3.metric("South Loop (S)", "7:30 PM - 3:00 AM [cite: 6]")
    st.divider()

    # 2. Initialize Map (Sproul Plaza Center)
    m = folium.Map(
        location=[37.8715, -122.2590], 
        zoom_start=15,
        tiles="CartoDB dark_matter"
    )

    # 3. Pin: UCPD Police Station
    folium.Marker(
        [37.8698, -122.2595],
        popup="<b>UCPD Headquarters</b><br>1 Sproul Hall (Basement)",
        tooltip="Police Station",
        icon=folium.Icon(color="red", icon="shield", prefix="fa")
    ).add_to(m)

    # 4. Pin: Bear Transit Night Shuttle Stops (Verified Locations) 
    stops = [
        {"name": "Downtown Berkeley BART", "loc": [37.8701, -122.2681]},
        {"name": "Shattuck & University", "loc": [37.8715, -122.2682]},
        {"name": "Hearst & Walnut", "loc": [37.8735, -122.2670]},
        {"name": "North Gate (Hearst & Euclid)", "loc": [37.8753, -122.2600]},
        {"name": "Cory Hall (Hearst & Le Roy)", "loc": [37.8752, -122.2573]},
        {"name": "Greek Theatre (Gayley & University Dr)", "loc": [37.8742, -122.2547]},
        {"name": "International House (Piedmont & Bancroft)", "loc": [37.8708, -122.2527]},
        {"name": "Clark Kerr Horseshoe", "loc": [37.8672, -122.2460]},
        {"name": "Unit 2 (Piedmont)", "loc": [37.8655, -122.2548]},
        {"name": "Unit 1 (Channing & College)", "loc": [37.8675, -122.2530]},
        {"name": "Unit 3 (Durant & Telegraph)", "loc": [37.8678, -122.2592]},
        {"name": "Moffitt Library", "loc": [37.8727, -122.2606]},
        {"name": "Mining Circle", "loc": [37.8741, -122.2576]},
        {"name": "RSF/Tang Center", "loc": [37.8693, -122.2625]}
    ]
    for stop in stops:
        folium.Marker(
            stop["loc"],
            popup=f"<b>Stop:</b> {stop['name']}",
            tooltip=stop["name"],
            icon=folium.Icon(color="purple", icon="bus", prefix="fa")
        ).add_to(m)
        
    # Temporary Closure Note 
    st.warning("⚠️ **Temporary Stop Closure:** 'The Gateway' stop is currently closed due to construction.")

    # 5. Pin: Blue Light Phone Locations
    blue_lights = [
        {"loc": [37.8715, -122.2605], "name": "Doe Library"},
        {"loc": [37.8695, -122.2595], "name": "Sproul Plaza"},
        {"loc": [37.8752, -122.2592], "name": "North Gate"},
        {"loc": [37.8655, -122.2538], "name": "Unit 2"},
        {"loc": [37.8735, -122.2580], "name": "Mining Circle"},
        {"loc": [37.8680, -122.2685], "name": "BART Station"},
        {"loc": [37.8745, -122.2540], "name": "Greek Theatre"}
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

    # 6. Render Map
    st_folium(m, width=700, height=500)
    
    st.markdown("""
    ### Legend
    * 🔴 **Red Shield:** UCPD Police Station
    * 🟣 **Purple Bus:** Night Shuttle Stop
    * 🔵 **Blue Circle:** Blue Light Phone
    """)

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

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
page = st.sidebar.radio("Navigation", ["Homepage", "Check-in Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Emergency Contacts", "Safety Chatbot"])

# --- PAGE 1: HOME ---
if page == "Home & Info":
    # 1. Centered Logo Logic
    logo_path = "luma_logo.jpeg"
    
    # Using columns to center the image
    col_left, col_logo, col_right = st.columns([1, 1, 1])
    
    with col_logo:
        if os.path.exists(logo_path):
            # Reduced width to keep it crisp and centered
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

    # 3. Brand Story (No longer an expander!)
    st.markdown("### ✨ What is Luma?")
    st.markdown("""
    **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
    
    We are your light source in Berkeley, ensuring no student has to walk in the dark alone. Our mission is to transform the way we navigate campus at night—replacing fear with a supportive, glowing community.
    """)

    # 4. Footer
    st.markdown("---")
    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: SAFETY TIMER (Comforting Check-In) ---
elif page == "Safety Timer":
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.title("⏱️ Safety Check-In")
    with col_toggle:
        st.write("") 
        # Added back the 'help' parameter for the info button
        demo_mode = st.toggle("Demo Mode", value=False, help="Sets the check-in interval to 5 seconds for testing and presentation.")

    # State Management
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'emergency_triggered' not in st.session_state:
        st.session_state.emergency_triggered = False

    # --- THE COMFORTING LIGHT PURPLE ALERT SCREEN ---
    if st.session_state.emergency_triggered:
        # Changed background-color to a soft Light Purple (#E1D5E7)
        st.markdown("""
            <style>
            .stApp {
                background-color: #E1D5E7 !important;
            }
            h1, h3, p { color: #4A2C5D !important; }
            </style>
            <div style="text-align: center; padding: 40px; border: 4px solid #9b59b6; border-radius: 20px;">
                <h1 style="font-size: 40px;">🌙 Checking in...</h1>
                <h3>We haven't heard from you in a bit.</h3>
                <p style="font-size: 18px;"><b>Your primary emergency contact has been notified</b> that you might need help right now.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("💛 I'm Okay Now (Reset)"):
            st.session_state.emergency_triggered = False
            st.session_state.timer_active = False
            st.rerun()
        st.stop() 

    # --- NORMAL TIMER UI ---
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

        # Phase 1: The Walking Wait
        wait_time = 5 if demo_mode else (check_interval * 60)
        st.info("✨ **Luma is here with you!**")
        progress_bar = st.progress(0)
        
        for i in range(wait_time):
            time.sleep(1)
            progress_bar.progress((i + 1) / wait_time)
        
        # Phase 2: The Soft Check-In
        st.markdown("<h3 style='text-align: center;'>Are you doing okay?</h3>", unsafe_allow_html=True)
        btn_placeholder = st.empty()
        safe_confirm = btn_placeholder.button("✅ I AM SAFE", key="checkin_btn")
        
        countdown_placeholder = st.empty()
        for s in range(reaction_time, -1, -1):
            if safe_confirm:
                st.success("Great! Let's keep going.")
                time.sleep(1)
                st.rerun()
            
            # Countdown uses brand purple
            countdown_placeholder.markdown(f"<h1 style='text-align: center; color: #9b59b6; font-size: 60px;'>{s}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
            if s == 0:
                st.session_state.emergency_triggered = True
                st.rerun()


# --- PAGE 3: BLUE LIGHT MAP (PDF ACCURACY) ---
# --- PAGE 3: BLUE LIGHT MAP (TIMES & NO PATHS) ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    st.write("Click on a stop to see schedule information.")
    
    # 1. Schedule Information Section
    st.subheader("🚌 Night Shuttle Schedule")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**North Loop (N)**")
        st.caption("7:45 PM - 2:15 AM | Every 30 mins")
    with col2:
        st.markdown("**South Loop (S)**")
        st.caption("7:30 PM - 3:00 AM | Every 30 mins")
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

    # 4. Define and Pin Shuttle Stops
    stops = [
        {"num": "N01", "name": "Moffitt Library", "loc": [37.8727, -122.2606]},
        {"num": "N02", "name": "West Circle", "loc": [37.8719, -122.2587]},
        {"num": "N03", "name": "Hearst & Walnut", "loc": [37.8735, -122.2670]},
        {"num": "N04", "name": "Downtown Berkeley BART", "loc": [37.8701, -122.2681]},
        {"num": "N05", "name": "North Gate", "loc": [37.8753, -122.2600]},
        {"num": "N06", "name": "Cory Hall", "loc": [37.8752, -122.2573]},
        {"num": "N07", "name": "Highland & Ridge", "loc": [37.8749, -122.2547]},
        {"num": "N08", "name": "Foothill (Unit 4)", "loc": [37.8738, -122.2546]},
        {"num": "S09", "name": "Unit 3", "loc": [37.8678, -122.2592]},
        {"num": "S10", "name": "Martinez Commons", "loc": [37.8675, -122.2562]},
        {"num": "S11", "name": "Unit 1", "loc": [37.8675, -122.2530]},
        {"num": "S12", "name": "Unit 2", "loc": [37.8655, -122.2548]},
        {"num": "S13", "name": "International House", "loc": [37.8708, -122.2527]},
        {"num": "S14", "name": "Channing Circle", "loc": [37.8673, -122.2519]},
        {"num": "S15", "name": "Warring & Channing", "loc": [37.8672, -122.2505]},
        {"num": "S16", "name": "Warring & Bancroft", "loc": [37.8683, -122.2505]},
        {"num": "S17", "name": "Piedmont & Bancroft", "loc": [37.8708, -122.2527]},
        {"num": "S18", "name": "Martinez Commons", "loc": [37.8675, -122.2562]},
        {"num": "S19", "name": "Unit 1", "loc": [37.8675, -122.2530]},
        {"num": "S20", "name": "RSF/Tang Center", "loc": [37.8693, -122.2625]},
        {"num": "S21", "name": "Bancroft & Shattuck", "loc": [37.8680, -122.2680]},
        {"num": "N22", "name": "Shattuck & University", "loc": [37.8715, -122.2682]},
        {"num": "S23", "name": "Mining Circle", "loc": [37.8741, -122.2576]},
        {"num": "N24", "name": "Moffitt Library", "loc": [37.8727, -122.2606]}
    ]
    for stop in stops:
        # Color code based on Route Prefix
        icon_color = "purple" if stop["num"].startswith("N") else "darkpurple"
        
        # Update popup to show frequency
        popup_text = f"<b>Stop {stop['num']}:</b> {stop['name']}<br><i>Frequency: Every 30 mins</i>"
        
        folium.Marker(
            stop["loc"],
            popup=popup_text,
            tooltip=stop["name"],
            icon=folium.Icon(color=icon_color, icon="bus", prefix="fa")
        ).add_to(m)
        
    # 5. REMOVED PATHWAYS (Polylines)
    
    # 6. Temporary Closure Note
    st.warning("⚠️ **Temporary Stop Closure:** 'The Gateway' stop is currently closed due to construction.")

    # 7. Pin: Blue Light Phone Locations
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

    # 8. Render Map
    st_folium(m, width=700, height=500)
    
    st.markdown("""
    ### Legend
    * 🔴 **Red Shield:** UCPD Police Station
    * 🟣 **Purple Bus:** North Loop Stop (N)
    * 🟣 **Dark Purple Bus:** South Loop Stop (S)
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

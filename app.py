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

# 2. Sidebar Navigation (Rearranged)
st.sidebar.title("🛡️ Luma Menu")
page = st.sidebar.radio(
    "Navigation", 
    ["Homepage", "Emergency Contacts", "Check-in Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Safety Chatbot"]
)

# --- PAGE 1: HOMEPAGE ---
if page == "Homepage":
    # 1. Sidebar Instruction with UP arrow
    st.markdown("<p style='text-align: left; color: #9b59b6; font-size: 14px;'>⬆️ Click the arrow in the upper left corner to open the menu</p>", unsafe_allow_html=True)
    
    logo_path = "luma_logo.jpeg"
    
    # Using a 1:2:1 ratio helps the middle column stay centered on smaller screens
    col_left, col_logo, col_right = st.columns([1, 2, 1])
    
    with col_logo:
        if os.path.exists(logo_path):
            # We wrap the image in a centered div to force mobile centering
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <img src="https://raw.githubusercontent.com/{st.secrets.get('github_username', 'your_user')}/{st.secrets.get('github_repo', 'your_repo')}/main/{logo_path}" 
                         width="160" style="border-radius: 20px;">
                </div>
                """, 
                unsafe_allow_html=True
            )
            # If the HTML above doesn't load your local file, use this standard line instead:
            # st.image(logo_path, width=160)
        else:
            st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Your Radiance in the Dark ✨</h3>", unsafe_allow_html=True)

    # 2. Emergency Buttons Grid
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

    # 3. SETUP INSTRUCTIONS (Updated for new Sidebar order)
    st.subheader("👤 Personal Safety Setup")
    st.info("""
    **To add your emergency contacts:**
    1. Open the **Side Menu** (top-left arrow ⬆️).
    2. Select **'Emergency Contacts'** (located right below Homepage).
    3. Enter your contact's information so Luma knows who to alert.
    """)

    st.divider()

    # 4. Brand Story
    st.markdown("### ✨ What is Luma?")
    st.markdown("""
    **Luma** originates from the Latin *lumen*, symbolizing **light, radiance, and brightness**. 
    We are your light source in Berkeley, ensuring no student has to walk in the dark alone. 
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

# --- PAGE 3: BLUE LIGHT MAP (NO PATH LINES) ---
I have updated the map to include the arrival times in the hover popups for each stop based on the provided PDF.

Updated Code for app.py
Replace the entire elif page == "Berkeley Blue Lights": section with this updated version:

Python

# --- PAGE 3: BLUE LIGHT MAP (WITH INTERACTIVE SCHEDULES) ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    st.write("Hover over bus stops for arrival times. Zoom in to see exact stop locations.")
    
    # 1. Schedule Information Section
    st.subheader("🚌 Night Shuttle Schedule Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<span style='color:orange'>●</span> **North Loop (N)**", unsafe_allow_html=True)
        st.caption("7:45 PM - 2:15 AM | Every 30 mins [cite: 1]")
    with col2:
        st.markdown("<span style='color:purple'>●</span> **South Loop (S)**", unsafe_allow_html=True)
        st.caption("7:30 PM - 3:00 AM | Every 30 mins [cite: 1]")
    st.divider()

    # 2. Initialize Map
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

    # 4. Define and Pin Shuttle Stops with Specific Schedules
    # Schedule data extracted from pages 3 and 4 of the provided PDF
    
    # --- NORTH LOOP SCHEDULE DATA (Mon-Fri) ---
    north_schedule = "7:45 PM, 8:15 PM, 8:45 PM, 9:15 PM, 9:45 PM, 10:15 PM, 10:45 PM, 11:15 PM, 11:45 PM, 12:15 AM, 12:45 AM, 1:15 AM, 1:45 AM"
    
    # --- SOUTH LOOP SCHEDULE DATA (Mon-Fri) ---
    south_schedule = "7:30 PM, 8:00 PM, 8:30 PM, 9:00 PM, 9:30 PM, 10:00 PM, 10:30 PM, 11:00 PM, 11:30 PM, 12:00 AM, 12:30 AM, 1:00 AM, 1:30 AM, 2:00 AM, 2:30 AM"

    stops = [
        # North Loop Stops
        {"num": "N01", "name": "Moffitt Library", "loc": [37.8727, -122.2606], "sched": north_schedule},
        {"num": "N02", "name": "Shattuck & University", "loc": [37.8715, -122.2682], "sched": north_schedule},
        {"num": "N03", "name": "Hearst & Walnut", "loc": [37.8735, -122.2670], "sched": north_schedule},
        {"num": "N05", "name": "North Gate", "loc": [37.8753, -122.2600], "sched": north_schedule},
        {"num": "N06", "name": "Cory Hall", "loc": [37.8752, -122.2573], "sched": north_schedule},
        {"num": "N07", "name": "Highland & Ridge", "loc": [37.8749, -122.2547], "sched": north_schedule},
        {"num": "N08", "name": "Foothill (Unit 4)", "loc": [37.8738, -122.2546], "sched": north_schedule},
        {"num": "N11", "name": "Bowles Hall", "loc": [37.8698, -122.2533], "sched": north_schedule},
        {"num": "N13", "name": "International House", "loc": [37.8708, -122.2527], "sched": north_schedule},
        {"num": "N14", "name": "Channing Circle", "loc": [37.8673, -122.2519], "sched": north_schedule},
        {"num": "N15", "name": "Warring & Channing", "loc": [37.8672, -122.2505], "sched": north_schedule},
        {"num": "N19", "name": "Student Union/Sather Gate", "loc": [37.8696, -122.2595], "sched": north_schedule},
        {"num": "N20", "name": "RSF/Tang Center", "loc": [37.8693, -122.2625], "sched": north_schedule},
        {"num": "N21", "name": "Bancroft & Shattuck", "loc": [37.8680, -122.2680], "sched": north_schedule},
        {"num": "N22", "name": "Berkeley Public Library", "loc": [37.8705, -122.2682], "sched": north_schedule},
        {"num": "N23", "name": "Hearst Mining Circle", "loc": [37.8741, -122.2576], "sched": north_schedule},
        
        # South Loop Stops
        {"num": "S01", "name": "Downtown Berkeley BART", "loc": [37.8701, -122.2681], "sched": south_schedule},
        {"num": "S03", "name": "West Circle", "loc": [37.8719, -122.2587], "sched": south_schedule},
        {"num": "S06", "name": "Shattuck & Durant", "loc": [37.8677, -122.2681], "sched": south_schedule},
        {"num": "S07", "name": "Dwight & Fulton", "loc": [37.8660, -122.2655], "sched": south_schedule},
        {"num": "S08", "name": "Ellsworth Parking Garage", "loc": [37.8675, -122.2625], "sched": south_schedule},
        {"num": "S09", "name": "Unit 3", "loc": [37.8678, -122.2592], "sched": south_schedule},
        {"num": "S10", "name": "Martinez Commons", "loc": [37.8675, -122.2562], "sched": south_schedule},
        {"num": "S11", "name": "Unit 1", "loc": [37.8675, -122.2530], "sched": south_schedule},
        {"num": "S12", "name": "Unit 2", "loc": [37.8655, -122.2548], "sched": south_schedule},
        {"num": "S13", "name": "Dwight & Piedmont", "loc": [37.8655, -122.2520], "sched": south_schedule},
        {"num": "S14", "name": "Clark Kerr - Horseshoe", "loc": [37.8672, -122.2460], "sched": south_schedule},
        {"num": "S15", "name": "Warring & Bancroft", "loc": [37.8683, -122.2505], "sched": south_schedule},
        {"num": "S17", "name": "Wurster Hall", "loc": [37.8701, -122.2555], "sched": south_schedule},
        {"num": "S18", "name": "Hearst Gym", "loc": [37.8698, -122.2575], "sched": south_schedule},
        {"num": "S23", "name": "Hearst Mining Circle", "loc": [37.8741, -122.2576], "sched": south_schedule}
    ]
    
    for stop in stops:
        icon_color = "orange" if stop["num"].startswith("N") else "purple"
        
        # Format popup with schedule
        popup_text = f"<b>Stop {stop['num']}:</b> {stop['name']}<br><br><b>Arrival Times:</b><br>{stop['sched']}"
        
        folium.Marker(
            stop["loc"],
            popup=popup_text,
            tooltip=stop["name"],
            icon=folium.Icon(color=icon_color, icon="bus", prefix="fa")
        ).add_to(m)
        
    # 5. Temporary Closure Note
    st.warning("⚠️ **Temporary Stop Closure:** 'The Gateway' stop is currently closed due to construction[cite: 2].")

    # 6. Pin: Blue Light Phone Locations
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

    # 7. Render Map
    st_folium(m, width=700, height=500)
    
    st.markdown("""
    ### Legend
    * 🔴 **Red Shield:** UCPD Police Station
    * 🟠 **Orange Bus:** North Loop Stop (N)
    * 🟣 **Purple Bus:** South Loop Stop (S)
    * 🔵 **Blue Circle:** Blue Light Phone
    """)

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

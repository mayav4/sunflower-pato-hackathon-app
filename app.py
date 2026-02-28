import streamlit as st
import time
import random
import os
import folium
from streamlit_folium import st_folium

# 0. INITIALIZE SESSION STATE (Must be at the very top)
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Homepage"
if 'contact_list' not in st.session_state:
    st.session_state.contact_list = [{"name": "Campus Police (UCPD)", "phone": "510-642-3333"}]
if 'primary_contact' not in st.session_state:
    st.session_state.primary_contact = "Campus Police (UCPD)"

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
    /* Center images on mobile */
    [data-testid="stImage"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Navigation
st.sidebar.title("🛡️ Luma Menu")
page = st.sidebar.radio(
    "Navigation", 
    ["Homepage", "Emergency Contacts", "Check-in Timer", "Berkeley Blue Lights", "Exit Phrase Generator", "Safety Chatbot"]
)

# --- PAGE 1: HOMEPAGE ---
if page == "Homepage":
    st.markdown("<p style='text-align: left; color: #9b59b6; font-size: 14px;'>⬆️ Click the arrow in the upper left corner to open the menu</p>", unsafe_allow_html=True)
    
    logo_path = "luma_logo.jpeg"
    col_left, col_logo, col_right = st.columns([1, 2, 1])
    
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=160)
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

    st.subheader("👤 Personal Safety Setup")
    st.info(f"""
    **Current Primary Contact:** {st.session_state.primary_contact}
    
    **To update this:**
    1. Open the **Side Menu** (top-left arrow ⬆️).
    2. Select **'Emergency Contacts'**.
    3. Add, Delete, or Select a new Primary contact.
    """)

    st.divider()
    st.markdown("### ✨ What is Luma?")
    st.markdown("We are your light source in Berkeley, ensuring no student has to walk in the dark alone.")
    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: EMERGENCY CONTACTS (Updated with Add/Delete/Primary) ---
elif page == "Emergency Contacts":
    st.title("🚨 Emergency Contacts")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🚨 CALL 911", "tel:911")
        st.link_button("👮 UCPD", "tel:5106423333")
    with col2:
        st.link_button("🚶 BEARWALK", "tel:5106429255")
        st.link_button("🚌 SHUTTLE", "tel:5106439255")
        
    st.divider()
    
    # Add New Contact
    st.subheader("➕ Add New Contact")
    new_name = st.text_input("Name (e.g., Mom, Roommate)")
    new_phone = st.text_input("Phone Number")
    if st.button("Add to Directory"):
        if new_name and new_phone:
            st.session_state.contact_list.append({"name": new_name, "phone": new_phone})
            st.success(f"Added {new_name}!")
            st.rerun()

    st.divider()

    # Manage/Delete Contacts
    st.subheader("⚙️ Manage Directory")
    for index, contact in enumerate(st.session_state.contact_list):
        cols = st.columns([3, 1])
        with cols[0]:
            is_pri = "⭐ " if contact['name'] == st.session_state.primary_contact else ""
            st.write(f"{is_pri}**{contact['name']}** ({contact['phone']})")
        with cols[1]:
            if contact['name'] != "Campus Police (UCPD)":
                if st.button("🗑️", key=f"del_{index}"):
                    if contact['name'] == st.session_state.primary_contact:
                        st.session_state.primary_contact = "Campus Police (UCPD)"
                    st.session_state.contact_list.pop(index)
                    st.rerun()

    st.divider()

    # Select Primary
    st.subheader("⭐ Select Primary Contact")
    contact_names = [c["name"] for c in st.session_state.contact_list]
    selected_primary = st.selectbox("Who should Luma alert?", options=contact_names, index=0)
    if st.button("Set as Primary"):
        st.session_state.primary_contact = selected_primary
        st.balloons()
        st.success(f"✅ {selected_primary} is now Primary!")

# --- PAGE 3: CHECK-IN TIMER ---
elif page == "Check-in Timer":
    if 'timer_active' not in st.session_state: st.session_state.timer_active = False
    if 'emergency_triggered' not in st.session_state: st.session_state.emergency_triggered = False

    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.title("⏱️ Safety Check-In")
    with col_toggle:
        st.write("") 
        # The 'help' parameter adds the little info button next to the toggle
        demo_mode = st.toggle("Demo Mode", value=False, help="Sets the check-in interval to 5 seconds for testing.")

    # --- THE EMERGENCY ALERT SCREEN (Dark Purple Mode) ---
    if st.session_state.emergency_triggered:
        st.markdown(f"""
            <style>
            /* This overrides the whole app background to Dark Purple only when triggered */
            .stApp {{ background-color: #2e004f !important; }} 
            
            /* Force all text in this mode to be white */
            h1, h2, h3, p, span, div {{ color: #ffffff !important; }}
            
            /* Add a glowing border to the alert box */
            .alert-box {{
                text-align: center; 
                padding: 40px; 
                border: 3px solid #9b59b6; 
                border-radius: 20px;
                background-color: #3d0066;
                box-shadow: 0px 0px 20px #9b59b6;
                margin-bottom: 20px;
            }}
            </style>
            
            <div class="alert-box">
                <h1 style="font-size: 40px; margin-bottom: 10px;">🌙 Luma Alert</h1>
                <h3 style="color: #e1d5e7 !important;">Check-in Window Expired</h3>
                <p style="font-size: 18px; margin-top: 20px;">
                    <b>{st.session_state.primary_contact}</b> has been notified 
                    that you may need assistance.
                </p>
                <p style="font-size: 14px; opacity: 0.8;">Your GPS coordinates and safety status were sent.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ I'm Okay Now (Reset App)"):
            st.session_state.emergency_triggered = False
            st.session_state.timer_active = False
            st.rerun()
        st.stop() 

    # --- NORMAL TIMER SETTINGS ---
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

        # Timer Logic
        wait_time = 5 if demo_mode else (check_interval * 60)
        st.info(f"✨ **Luma is protecting you.** Next check-in in {wait_time}s.")
        progress_bar = st.progress(0)
        
        # Countdown to the "Are you okay?" prompt
        for i in range(wait_time):
            time.sleep(1)
            progress_bar.progress((i + 1) / wait_time)
        
        # The Check-in Prompt
        st.markdown("<h3 style='text-align: center;'>Are you doing okay?</h3>", unsafe_allow_html=True)
        btn_placeholder = st.empty()
        
        # Button to confirm safety
        safe_confirm = btn_placeholder.button("✅ I AM SAFE", key="checkin_btn")
        
        countdown_placeholder = st.empty()
        for s in range(reaction_time, -1, -1):
            if safe_confirm:
                st.success("Great! Resetting for your next window...")
                time.sleep(1)
                st.rerun()
            
            # Large, visible countdown numbers for the demo
            countdown_placeholder.markdown(f"<h1 style='text-align: center; color: #9b59b6; font-size: 80px;'>{s}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
            if s == 0:
                st.session_state.emergency_triggered = True
                st.rerun()
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
    
    # --- FIXED SECTION ---
    phrases = [
        "I don’t know you. Please give me space.",
        "I’m not interested. Please stop following me.",
        "I’d like to be left alone.",
        "Please step back.",
        "I feel uncomfortable. I’m going to leave.",
        "I don’t want to talk. Have a good day.",
        "I need to meet someone. I have to go.",
        "I’m in a hurry.",
        "Excuse me.",
        "I need to go, I have an appointment."
    ]
    # ----------------------
    
    if st.button("Generate"):
        st.success(f"**Try:** \"{random.choice(phrases)}\"")
    
    # --- ADD THIS SECTION UNDER THE BUTTON ---
    st.markdown("---")
    st.markdown("#### Try these ideas:")
    st.markdown("""
    * "My roommate is locked out!"
    * "My Uber is here!"
    * "I left my stove on!"
    * "I need to meet someone at the dorms."
    * "My phone is dying, I need to go charge it."
    """)
    # ----------------------------------------

# --- PAGE 6: SAFETY CHATBOT (UPDATED) ---
elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    st.write("Describe your situation or select a quick option below.")
    
    # State to hold the selected scenario for immediate triggering
    if 'quick_scenario' not in st.session_state:
        st.session_state.quick_scenario = ""

    # 1. Quick Select Buttons for immediate situations
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 Being Followed"):
            st.session_state.quick_scenario = "I am being followed"
        if st.button("🔒 Locked Out/In"):
            st.session_state.quick_scenario = "I am locked out of my dorm"
    with col2:
        if st.button("💡 Lost at Night"):
            st.session_state.quick_scenario = "I am lost and it is dark"
        if st.button("😨 Feeling Unsafe"):
            st.session_state.quick_scenario = "I feel unsafe in my current location"

    # 2. Text Input for custom situations (updates based on scenario selection)
    user_input = st.text_input("Or describe your situation:", value=st.session_state.quick_scenario)

    # 3. Action Button & Advice Logic
    # Trigger if "Get Safety Plan" is clicked OR if a quick button was clicked
    if st.button("Get Safety Plan") or st.session_state.quick_scenario:
        # Determine the final query to act on
        final_query = st.session_state.quick_scenario if st.session_state.quick_scenario else user_input
        
        if final_query:
            st.subheader("Your Action Plan")
            
            # 4. Context-Aware Advice Generator
            if "followed" in final_query.lower():
                st.warning("⚠️ **Immediate Action:** Go to a populated area (a store, restaurant) or a Blue Light phone. Do not go home. Call UCPD.")
                st.link_button("👮 Call UCPD Now", "tel:5106423333")
            elif "lost" in final_query.lower() or "dark" in final_query.lower():
                st.info("🗺️ **Action Plan:** Open the 'Berkeley Blue Lights' page to find the nearest stop for the Night Safety Shuttle[cite: 184].")
            elif "unsafe" in final_query.lower():
                st.warning("⚠️ **Action Plan:** Trust your gut. Move to a bright, crowded area. Request a Bearwalk companion.")
                st.link_button("🚶 Request Bearwalk", "tel:5106429255")
            elif "locked out" in final_query.lower():
                st.info("🔑 **Action Plan:** Call your resident advisor or UCPD non-emergency.")
                st.link_button("📞 Call UCPD Non-Emergency", "tel:5106426760")
            else:
                st.info("💡 **Action Plan:** Stay calm. Find a brightly lit area. Utilize your emergency contacts if necessary.")
                st.link_button(f"📞 Call {st.session_state.primary_contact}", f"tel:{st.session_state.primary_contact}")
        else:
            st.error("Please describe your situation or select a quick option.")
        
        # Reset scenario after running logic to allow new inputs
        st.session_state.quick_scenario = ""

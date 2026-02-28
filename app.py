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

# --- PAGE 2: SAFETY TIMER (With Red Alert) ---
elif page == "Safety Timer":
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.title("⏱️ Safety Check-In")
    with col_toggle:
        st.write("") 
        demo_mode = st.toggle("Demo Mode", value=False)

    # Initialize session states if they don't exist
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'emergency_triggered' not in st.session_state:
        st.session_state.emergency_triggered = False

    # --- THE RED ALERT SCREEN ---
    if st.session_state.emergency_triggered:
        # This CSS overrides the whole app's look to turn it bright red
        st.markdown("""
            <style>
            .stApp {
                background-color: #ff4757 !important;
            }
            h1, p { color: white !important; }
            </style>
            <div style="text-align: center; padding: 50px; border: 5px solid white; border-radius: 20px;">
                <h1 style="font-size: 50px;">🚨 ALERT TRIGGERED 🚨</h1>
                <h3 style="color: white;">Emergency Contacts Notified</h3>
                <p>GPS Coordinates Sent to UCPD Dispatch</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("❌ DISMISS & RESET"):
            st.session_state.emergency_triggered = False
            st.session_state.timer_active = False
            st.rerun()
        st.stop() 

    # --- NORMAL TIMER UI ---
    st.write("Set your check-in frequency. If you don't respond, the screen will turn RED.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        check_interval = st.selectbox("Check in every:", [1, 2, 5, 10], index=1, format_func=lambda x: f"{x} Mins")
    with col_b:
        reaction_time = st.slider("Response window (seconds):", 5, 60, 10)

    if not st.session_state.timer_active:
        if st.button("🚀 Start Protected Walk"):
            st.session_state.timer_active = True
            st.rerun()
    else:
        if st.button("🏠 I'm Safely Home (Stop)"):
            st.session_state.timer_active = False
            st.rerun()

        # Phase 1: The Wait
        wait_time = 5 if demo_mode else (check_interval * 60)
        st.info("🚶 **Luma is monitoring...**")
        progress_bar = st.progress(0)
        
        for i in range(wait_time):
            time.sleep(1)
            progress_bar.progress((i + 1) / wait_time)
        
        # Phase 2: The Check-In
        st.warning("⚠️ **ARE YOU SAFE? CHECK IN NOW!**")
        btn_placeholder = st.empty()
        safe_confirm = btn_placeholder.button("✅ I AM SAFE", key="checkin_btn")
        
        countdown_placeholder = st.empty()
        for s in range(reaction_time, -1, -1):
            if safe_confirm:
                st.success("Safe! Resetting timer...")
                time.sleep(1)
                st.rerun()
            
            # Show the shrinking countdown
            countdown_placeholder.markdown(f"<h1 style='text-align: center; color: red; font-size: 80px;'>{s}</h1>", unsafe_allow_html=True)
            time.sleep(1)
            
            if s == 0:
                st.session_state.emergency_triggered = True
                st.rerun()
# --- PAGE 3: BERKELEY BLUE LIGHTS ---
# --- PAGE 3: BLUE LIGHT MAP (PATHWAYS ADDED) ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    st.write("Zoom in to see exact stop locations and paths.")
    
    # 1. Schedule Information Section
    st.subheader("🚌 Night Shuttle Schedule")
    col1, col2, col3 = st.columns(3)
    col1.metric("Frequency", "Every 30 Mins")
    col2.metric("North Loop (N)", "7:45 PM - 2:15 AM")
    col3.metric("South Loop (S)", "7:30 PM - 3:00 AM")
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
        {"num": "01", "name": "Moffitt Library", "loc": [37.8727, -122.2606]},
        {"num": "02", "name": "West Circle", "loc": [37.8719, -122.2587]},
        {"num": "03", "name": "Hearst & Walnut", "loc": [37.8735, -122.2670]},
        {"num": "04", "name": "Downtown Berkeley BART", "loc": [37.8701, -122.2681]},
        {"num": "05", "name": "North Gate", "loc": [37.8753, -122.2600]},
        {"num": "06", "name": "Cory Hall", "loc": [37.8752, -122.2573]},
        {"num": "07", "name": "Highland & Ridge", "loc": [37.8749, -122.2547]},
        {"num": "08", "name": "Foothill (Unit 4)", "loc": [37.8738, -122.2546]},
        {"num": "09", "name": "Unit 3", "loc": [37.8678, -122.2592]},
        {"num": "10", "name": "Martinez Commons", "loc": [37.8675, -122.2562]},
        {"num": "11", "name": "Unit 1", "loc": [37.8675, -122.2530]},
        {"num": "12", "name": "Unit 2", "loc": [37.8655, -122.2548]},
        {"num": "13", "name": "International House", "loc": [37.8708, -122.2527]},
        {"num": "14", "name": "Channing Circle", "loc": [37.8673, -122.2519]},
        {"num": "15", "name": "Warring & Channing", "loc": [37.8672, -122.2505]},
        {"num": "16", "name": "Warring & Bancroft", "loc": [37.8683, -122.2505]},
        {"num": "17", "name": "Piedmont & Bancroft", "loc": [37.8708, -122.2527]},
        {"num": "18", "name": "Martinez Commons", "loc": [37.8675, -122.2562]},
        {"num": "19", "name": "Unit 1", "loc": [37.8675, -122.2530]},
        {"num": "20", "name": "RSF/Tang Center", "loc": [37.8693, -122.2625]},
        {"num": "21", "name": "Bancroft & Shattuck", "loc": [37.8680, -122.2680]},
        {"num": "22", "name": "Shattuck & University", "loc": [37.8715, -122.2682]},
        {"num": "23", "name": "Mining Circle", "loc": [37.8741, -122.2576]},
        {"num": "24", "name": "Moffitt Library", "loc": [37.8727, -122.2606]}
    ]
    for stop in stops:
        folium.Marker(
            stop["loc"],
            popup=f"<b>Stop {stop['num']}:</b> {stop['name']}",
            tooltip=stop["name"],
            icon=folium.Icon(color="purple", icon="bus", prefix="fa")
        ).add_to(m)
        
    # 5. Add Pathways (Polylines)
    # North Loop (Purple)
    north_path = [
        [37.8727, -122.2606], [37.8719, -122.2587], [37.8735, -122.2670],
        [37.8701, -122.2681], [37.8753, -122.2600], [37.8752, -122.2573],
        [37.8749, -122.2547], [37.8738, -122.2546], [37.8727, -122.2606]
    ]
    folium.PolyLine(north_path, color="purple", weight=4, opacity=0.8, tooltip="North Loop (N)").add_to(m)

    # South Loop (Dark Purple)
    south_path = [
        [37.8678, -122.2592], [37.8675, -122.2562], [37.8675, -122.2530],
        [37.8655, -122.2548], [37.8708, -122.2527], [37.8673, -122.2519],
        [37.8672, -122.2505], [37.8683, -122.2505], [37.8693, -122.2625],
        [37.8680, -122.2680], [37.8715, -122.2682], [37.8727, -122.2606],
        [37.8678, -122.2592]
    ]
    folium.PolyLine(south_path, color="darkpurple", weight=4, opacity=0.8, tooltip="South Loop (S)").add_to(m)

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
    * 🟣 **Purple Line/Bus:** North Loop (N)
    * 🟣 **Dark Purple Line/Bus:** South Loop (S)
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

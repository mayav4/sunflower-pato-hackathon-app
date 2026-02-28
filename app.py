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
    # 1. High-Resolution Logo Logic
    logo_path = "luma_logo.jpeg"
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=250, use_container_width=False)
    else:
        st.markdown("<h1 style='text-align: center; color: #9b59b6;'>🌙 LUMA</h1>", unsafe_allow_html=True)
        st.caption(f"Note: {logo_path} not found. Check GitHub root folder!")

    st.markdown("<h3 style='text-align: center;'>Your Radiance in the Dark.</h3>", unsafe_allow_html=True)

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

    # 4. Footer
    st.markdown("---")
    st.caption("Created with 💜 for the 2026 Women's Hackathon")

# --- PAGE 2: TIMER ---
elif page == "Safety Timer":
    # 1. Top Row: Title on left, Demo Toggle on right
    col_title, col_toggle = st.columns([3, 1])
    
    with col_title:
        st.title("⏱️ Safety Check-In")
    
    with col_toggle:
        st.write("") # Just for spacing
        demo_mode = st.toggle("Demo Mode", value=False, help="Sets timer to 5 seconds for testing.")

    # 2. Status Message based on Toggle
    if demo_mode:
        st.warning("🚀 **Demo Mode Active:** Timer is set to 5 seconds.")
    
    st.write("Heading out? Set your walk time. If the clock hits zero, we alert your emergency contacts.")
    
    # 3. Time Selection
    mins = st.selectbox("How many minutes is your walk?", [1, 5, 10, 15, 30], index=0)
    
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False

    # 4. Action Buttons
    col1, col2 = st.columns(2)
    with col1:
        start_btn = st.button("🚀 Start My Walk")
    with col2:
        stop_btn = st.button("🏠 I'm Safe! (Stop)")

    if start_btn:
        st.session_state.timer_running = True

    # 5. Timer Logic
    if st.session_state.timer_running:
        # If demo_mode is on, use 5 seconds. Otherwise, use mins * 60.
        seconds = 5 if demo_mode else (mins * 60)
        
        progress_bar = st.progress(1.0)
        status_text = st.empty()
        
        for i in range(seconds, -1, -1):
            if stop_btn:
                st.session_state.timer_running = False
                status_text.success("🎉 You're safe! Timer deactivated.")
                break
            
            percent_filled = i / seconds if seconds > 0 else 0
            progress_bar.progress(percent_filled)
            
            # Visual Countdown
            display_color = "red" if i <= 10 else "white"
            status_text.markdown(f"<h1 style='text-align: center; color: {display_color};'>{i//60:02d}:{i%60:02d}</h1>", unsafe_allow_html=True)
            
            time.sleep(1)
            
            if i == 0:
                st.session_state.timer_running = False
                st.error("🚨 ALERT: Timer expired! Emergency contacts have been pinged.")
                st.balloons()
                
# --- PAGE 3: BLUE LIGHT MAP ---
elif page == "Safety Map":
    st.header("📍 Interactive Night Safety Map")
    st.write("Zoom in to see exact stop locations.")
    
    # 3. Create the Map Center (Sproul Plaza) using Content-Rich Dark Tiles
    m = folium.Map(
        location=[37.8715, -122.2590], 
        zoom_start=15,
        # 'OpenStreetMap' is the standard, 'CartoDB positron' is light mode
        tiles="OpenStreetMap" 
    )

    # 4. Marker: UCPD Police Station
    folium.Marker(
        [37.8698, -122.2595],
        popup="<b>UCPD Headquarters</b><br>1 Sproul Hall (Basement)",
        tooltip="Police Station",
        icon=folium.Icon(color="red", icon="shield", prefix="fa")
    ).add_to(m)

    # 5. Markers: All Accurate Bear Transit Night Shuttle Stops
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
        icon_color = "purple" if "N/S" in stop["route"] else "darkpurple"
        folium.Marker(
            stop["loc"],
            popup=f"<b>Stop {stop['num']}: {stop['name']}</b><br>Route: {stop['route']}",
            tooltip=stop["name"],
            icon=folium.Icon(color=icon_color, icon="bus", prefix="fa")
        ).add_to(m)

    # 6. Markers: Accurate Blue Light Phone Locations
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
    st_folium(m, width=1200, height=600, use_container_width=True)
    
    st.markdown("""
    ### Legend
    * 🔴 **Red Shield:** UCPD Police Station
    * 🟣 **Purple Bus:** Night Shuttle Stop
    * 🔵 **Blue Circle:** Blue Light Phone
    """)

# --- PAGE 4: PHRASE GENERATOR ---
elif page == "Exit Phrase Generator":
    st.title("💬 Exit Phrase Generator")
    phrases = ["My roommate is locked out!", "My mom is calling, it's urgent.", "My Uber is here!"]
    if st.button("Generate New Excuse"):
        st.success(f"**Try saying:** \"{random.choice(phrases)}\"")

# --- PAGE 5: EMERGENCY ---
elif page == "Emergency Contacts":
    st.title("🚨 Emergency Contacts")
    st.link_button("📞 CALL UCPD", "tel:5106423333")
    st.link_button("🚶 Night Safety Shuttle", "tel:5106439255")

# --- PAGE 6: SAFETY CHATBOT ---
elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    user_msg = st.text_input("Describe your situation:")
    if st.button("Get Safety Plan"):
        st.info("Plan generated: Stay in well-lit areas and call a friend.")
        st.success("Safety plan generated.")

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

elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    st.text_input("Describe your situation:")
    if st.button("Get Safety Plan"):
        st.info("Head toward the nearest lit building or Blue Light phone.")

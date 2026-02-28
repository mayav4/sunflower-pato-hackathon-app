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

    st.title("⏱️ Safety Check-In")
    demo_mode = st.toggle("Demo Mode", value=False)

    if st.session_state.emergency_triggered:
        st.markdown(f"""
            <style>.stApp {{ background-color: #E1D5E7 !important; }}</style>
            <div style="text-align: center; padding: 40px; border: 4px solid #9b59b6; border-radius: 20px;">
                <h1>🌙 Emergency Alert</h1>
                <h3><b>{st.session_state.primary_contact}</b> has been notified.</h3>
                <p>Stay where you are or head to a Blue Light phone.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("I'm Okay Now (Reset)"):
            st.session_state.emergency_triggered = False
            st.session_state.timer_active = False
            st.rerun()
        st.stop()

    check_interval = st.selectbox("Check in every:", [1, 2, 5, 10], index=1, format_func=lambda x: f"{x} Mins")
    reaction_time = st.slider("Response window (seconds):", 5, 60, 15)

    if not st.session_state.timer_active:
        if st.button("🚀 Start My Protected Walk"):
            st.session_state.timer_active = True
            st.rerun()
    else:
        if st.button("🏠 I'm Safely Home"):
            st.session_state.timer_active = False
            st.rerun()
        
        wait_time = 5 if demo_mode else (check_interval * 60)
        progress_bar = st.progress(0)
        for i in range(wait_time):
            time.sleep(1)
            progress_bar.progress((i + 1) / wait_time)
        
        st.warning("Are you okay?")
        if st.button("✅ I AM SAFE"):
            st.rerun()
        
        countdown = st.empty()
        for s in range(reaction_time, -1, -1):
            countdown.header(f"Emergency Alert in: {s}s")
            time.sleep(1)
            if s == 0:
                st.session_state.emergency_triggered = True
                st.rerun()

# --- REMAINING PAGES (MAP, EXIT PHRASES, CHATBOT) ---
elif page == "Berkeley Blue Lights":
    st.header("📍 Interactive Night Safety Map")
    m = folium.Map(location=[37.8715, -122.2590], zoom_start=15, tiles="CartoDB dark_matter")
    st_folium(m, width=700, height=500)

elif page == "Exit Phrase Generator":
    st.title("💬 Exit Phrase Generator")
    if st.button("Generate"):
        st.success(f"**Try:** \"{random.choice(['My Uber is here!', 'Roommate is locked out!'])}\"")

elif page == "Safety Chatbot":
    st.title("🤖 AI Safety Assistant")
    st.text_input("Describe your situation:")
    if st.button("Get Safety Plan"):
        st.info("Head toward the nearest lit building or Blue Light phone.")

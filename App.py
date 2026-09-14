import streamlit as st
import pandas as pd

# Configure page settings
st.set_page_config(page_title="Student Chat Assistant", page_icon="🎓", layout="wide")

# Initialize storage for user tasks and calendar deadlines
if "assignments_store" not in st.session_state:
    st.session_state.assignments_store = {
        "✨ Group 1: Computer Science Official": ["Study Lab Chapters 1 to 3"],
        "🍔 Group 2: Hostel Block A Notice Board": ["Clean up room for inspection", "Vote for the new mess menu"],
        "🤖 Group 3: AI/ML Coding Club": ["Find teammates for the hackathon", "Install Python on your laptop"],
        "🎨 Group 4: College Festival Team": ["Make the event layout chart", "Create social media posters on Canva"],
        "🍿 Group 5: Roommates Chat (Floor 3)": ["Pay money for weekend pizza pool", "Vote for the movie night pick"]
    }

if "deadlines_store" not in st.session_state:
    st.session_state.deadlines_store = {
        "✨ Group 1: Computer Science Official": ["Guest Lecture (Today at 2:00 PM)", "Lab Quiz 1 (This Friday morning)"],
        "🍔 Group 2: Hostel Block A Notice Board": ["Room Inspection (Tonight at 9:00 PM)", "Menu Form Cutoff (Tonight at 11:59 PM)"],
        "🤖 Group 3: AI/ML Coding Club": ["Registration Deadline (Closing very soon)", "Weekly Club Meeting (Sunday at 6:00 PM)"],
        "🎨 Group 4: College Festival Team": ["Volunteer Form Due (Thursday at 5:00 PM)", "Poster Draft Due (Friday at midnight)"],
        "🍿 Group 5: Roommates Chat (Floor 3)": ["Pizza Pool Deadline (Saturday at 6:00 PM)", "Movie Night Starts (Saturday at 9:30 PM)"]
    }

# --- GLOBAL THEME CONFIGURATION ---
st.markdown("""
    <style>
    /* Main Background — Clean Premium Off-White */
    .stApp {
        background-color: #FAF9F6 !important;
        font-size: 0.88rem !important;
    }
    
    /* Top Header Bar — Matches Your Vibrant Pink Image Exactly */
    .custom-navbar {
        background-color: #cf0864 !important;
        padding: 0.8rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .navbar-brand {
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 1.15rem;
    }
    .user-profile {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #000000 !important;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .avatar {
        width: 32px;
        height: 32px;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    
    /* Clean Info Sub-Header Box */
    div.portal-header-box {
        background-color: #FFFFFF;
        border: 1px solid #EFECE6;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    div.portal-header-box h2 {
        color: #cf0864 !important;
        font-size: 1.25rem !important;
        margin: 0;
    }
    div.portal-header-box p {
        color: #3D2314 !important;
        margin: 0;
    }
    
    /* Active Connection Pulse Dot */
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #cf0864;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }
    
    /* Dynamic Headers — Deep Vibrant Pink */
    h1, h2, h3, h4 {
        color: #cf0864 !important;
        font-weight: 700 !important;
    }
    h3 { font-size: 1.15rem !important; margin-bottom: 1rem !important; }
    h4 { font-size: 1rem !important; margin-bottom: 0.5rem !important; }
    
    /* Primary Text Blocks — Clean Dark Brown */
    p, span, label, div {
        color: #3D2314 !important;
    }
    
    /* Presentation Score Cards — Custom Dark Berry #8f043e */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EFECE6 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02) !important;
    }
    div[data-testid="stMetricLabel"] > div, 
    div[data-testid="stMetricLabel"] span, 
    div[data-testid="stMetricLabel"] p {
        color: #8f043e !important;
        font-size: 0.78rem !important;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: #8f043e !important;
        font-weight: 800 !important;
        font-size: 1.35rem !important;
    }

    /* Soft Blue Chat Alert Box */
    .stAlert {
        background-color: #EDF5FF !important;
        border-left: 4px solid #cf0864 !important;
        border-radius: 8px;
        padding: 0.85rem !important;
    }
    .stAlert div, .stAlert p {
        color: #3D2314 !important;
    }
    
    /* Interactive Tables & Input Fields */
    .stDataFrame, div[data-testid="stTable"] {
        font-size: 0.825rem !important;
    }
    .stCaption {
        font-size: 0.75rem !important;
        color: #5C4033 !important;
    }
    
    /* Primary Action Buttons */
    div.stButton > button:first-child {
        background-color: #cf0864 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold;
        font-size: 0.85rem;
        padding: 0.4rem 1rem;
    }
    div.stButton > button:first-child:hover {
        background-color: #8f043e !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. TOP PORTAL HEADER NAVIGATION BAR ---
st.markdown("""
    <div class="custom-navbar">
        <div class="navbar-brand">🎓 College Sync — Student Stream Triage Hub</div>
        <div class="user-profile">
            <span>Welcome, <b>Freshman Student</b></span>
            <div class="avatar">FS</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. PRESENTATION WELCOME BANNER ---
st.markdown("""
    <div class="portal-header-box">
        <div>
            <h2>Smart Student Assistant Dashboard</h2>
            <p>Helping students clean up chaotic chat groups and instantly organize their daily schedules.</p>
        </div>
        <div style="font-size: 0.825rem; font-weight: 600;">
            <span class="status-dot"></span>Live Chat Scanner Active
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. QUICK SCORE CARDS GRID ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="🎯 Target College CGPA", value="8.5 / 10")
with m2:
    st.metric(label="🏠 Campus Living Space", value="Block A - Room 304")
with m3:
    st.metric(label="🏫 Main Class Location", value="Lecture Hall 3 (Engineering)")
with m4:
    st.metric(label="🌸 Monitored Chat Feeds", value="5 Active Channels")

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. DUAL COLUMN PRESENTATION HUB ---
col_left, col_right = st.columns([1, 2]) # Balanced proportions for side-by-side view

with col_left:
    st.markdown("### 🎛️ Group Controller")
    selected_stream = st.selectbox(
        "Choose a Chat Group to Filter:",
        options=list(st.session_state.assignments_store.keys())
    )
    
    st.markdown("---")
    st.markdown("### 🎙️ Instant Voice Input")
    st.caption("Tell the app what to add (e.g., 'Submit physics files tomorrow morning'):")
    
    # Simple speech or text integration hub
    audio_input = st.audio_input("Record Your Voice Command")
    voice_command = st.text_input("Or type your reminder directly here:", placeholder="Type a reminder...")
    
    if st.button("⚡ Save Directly to Calendar", use_container_width=True):
        if voice_command:
            clean_cmd = voice_command.strip()
            st.session_state.deadlines_store[selected_stream].append(clean_cmd)
            st.success("Successfully saved to your Calendar list below!")
            st.rerun()
        else:
            st.warning("Please type or say something first.")

# --- 5. CLEAN INFORMATION WORKSPACE ---
with col_right:
    chat_links = {
        "✨ Group 1: Computer Science Official": "• [🌐 Join Online Class Link](https://google.com)\n• [💬 Join WhatsApp Lab Sub-Group](https://whatsapp.com)",
        "🍔 Group 2: Hostel Block A Notice Board": "• [📝 Fill Mess Menu Feedback Form](https://forms.gle)\n• [💬 Join Hostel Sports Chat](https://whatsapp.com)",
        "🤖 Group 3: AI/ML Coding Club": "• [🏆 Open Competition Register Page](https://devpost.com)\n• [💬 Join WhatsApp Projects Team](https://whatsapp.com)",
        "🎨 Group 4: College Festival Team": "• [📝 Fill Student Volunteer Signup Form](https://forms.gle)\n• [💬 Join WhatsApp Design Group](https://whatsapp.com)",
        "🍿 Group 5: Roommates Chat (Floor 3)": "• [🍿 Open Shared Movie Voting Poll](https://forms.gle)\n• [💬 Join Canteen Delivery Group](https://whatsapp.com)"
    }
    
    chat_summaries = {
        "✨ Group 1: Computer Science Official": "The class representative announced a mandatory lecture at 2 PM today in Seminar Hall 2. Professor Mehta also shared the chapters covered in the upcoming lab evaluation.",
        "🍔 Group 2: Hostel Block A Notice Board": "The hostel warden announced a room cleanliness inspection for tonight. Students are also voting on a Google Form to change the weekly mess menu options.",
        "🤖 Group 3: AI/ML Coding Club": "The club lead shared a reminder that project registration closes very soon. The team is holding their weekly synchronization meeting this Sunday evening on Discord.",
        }
    chat_summaries = {
        "✨ Group 1: Computer Science Official": "The class representative announced a mandatory lecture at 2 PM today in Seminar Hall 2. Professor Mehta also shared the chapters covered in the upcoming lab evaluation.",
        "🍔 Group 2: Hostel Block A Notice Board": "The hostel warden announced a room cleanliness inspection for tonight. Students are also voting on a Google Form to change the weekly mess menu options.",
        "🤖 Group 3: AI/ML Coding Club": "The club lead shared a reminder that project registration closes very soon. The team is holding their weekly synchronization meeting this Sunday evening on Discord.",
        "🎨 Group 4: College Festival Team": "The festival coordinators are looking for urgent student volunteers to manage logistics. Creative banners and templates are open for edits on Canva.",
        "🍿 Group 5: Roommates Chat (Floor 3)": "Students are pooling money to place a group food order this weekend and are organizing a movie night inside the main hostel common room lounge."
    }

    st.markdown("### 📊 Smart Stream Analysis Matrix")
    
    # 2x2 grid layout using clear formatting columns
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        st.markdown("#### 📝 Clean Chat Summary")
        st.info(chat_summaries[selected_stream])
        
    with r1_c2:
        st.markdown("#### 📚 Tracked Tasks & Homework")
        st.caption("Double-click a cell below to edit or type custom items:")
        df_asg = pd.DataFrame({"Your Tasks": st.session_state.assignments_store[selected_stream]})
        edited_asg = st.data_editor(df_asg, num_rows="dynamic", use_container_width=True, key=f"asg_ed_{selected_stream}")
        st.session_state.assignments_store[selected_stream] = edited_asg["Your Tasks"].tolist()
        
    st.markdown("<br>", unsafe_allow_html=True) # Pure clean vertical spacing
    
    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        st.markdown("#### 📅 Calendar & Deadlines")
        st.caption("Custom voice commands automatically drop here:")
        df_dl = pd.DataFrame({"Deadlines": st.session_state.deadlines_store[selected_stream]})
        edited_dl = st.data_editor(df_dl, num_rows="dynamic", use_container_width=True, key=f"dl_ed_{selected_stream}")
        st.session_state.deadlines_store[selected_stream] = edited_dl["Deadlines"].tolist()
        
    with r2_c2:
        st.markdown("#### 🔗 Found Invitation Links")
        st.markdown(chat_links[selected_stream])

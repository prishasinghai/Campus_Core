import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page settings
st.set_page_config(page_title="College Sync: Portal Triage Hub", page_icon="💖", layout="wide")

# Initialize Session States for editable dynamic frames so user entries persist across actions
if "assignments_store" not in st.session_state:
    st.session_state.assignments_store = {
        "✨ Group 1: Official CS Freshmen Batch '26": ["Review Chapters 1 through 3"],
        "🍔 Group 2: Hostel Block-A Banter & Mess": ["Organize living quarters", "Submit preferred dining choices"],
        "🤖 Group 3: AI/ML Student Club (Un-Official)": ["Find project teammates", "Install dependencies script"],
        "🎨 Group 4: Cultural Fest Core Committee '26": ["Draft event layout plan", "Design social graphics on Canva"],
        "🍿 Group 5: Block-A Third Floor Wing-Mates": ["Send share of pizza pool money to room 312", "Vote for movie choice on poll"]
    }

if "deadlines_store" not in st.session_state:
    st.session_state.deadlines_store = {
        "✨ Group 1: Official CS Freshmen Batch '26": ["Guest Lecture (2:00 PM today)", "Lab Quiz 1 (Friday morning)"],
        "🍔 Group 2: Hostel Block-A Banter & Mess": ["Room Inspection (9:00 PM tonight)", "Form Submission Cutoff (11:59 PM)"],
        "🤖 Group 3: AI/ML Student Club (Un-Official)": ["Hackathon Registration closes soon", "Weekly Sync Meet (Sunday 6:00 PM)"],
        "🎨 Group 4: Cultural Fest Core Committee '26": ["Volunteer Onboarding Form (By Thursday 5 PM)", "Theme Reveal Poster Draft (Friday midnight)"],
        "🍿 Group 5: Block-A Third Floor Wing-Mates": ["Pizza Money Collection deadline (Saturday 6 PM)", "Movie Night begins (Saturday 9:30 PM)"]
    }

# --- GLOBAL STYLING: COMPACT FONTS & PINK WORKSPACE ---
st.markdown("""
    <style>
    /* Global Core Framework Overrides with smaller fonts */
    .stApp {
        background-color: #FFF5F7 !important; /* Soft Pastel Rose Tint */
        font-size: 0.85rem !important; /* Reduces base font size across the dashboard */
    }
    
    /* Top Professional University Styled Navbar */
    .custom-navbar {
        background-color: #4A1525; /* Dark Plum Crimson */
        padding: 0.5rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .navbar-brand {
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .user-profile {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #FFFFFF !important;
        font-size: 0.85rem;
    }
    .avatar {
        width: 30px;
        height: 30px;
        background-color: #FF69B4;
        color: white !important;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    /* Custom Card Containers resembling the University Portal UI layout */
    div.portal-header-box {
        background-color: #FFFFFF;
        border: 1px solid #FFB6C1;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(255, 182, 193, 0.1);
    }
    div.portal-header-box h2 {
        font-size: 1.2rem !important;
        margin: 0;
    }
    div.portal-header-box p {
        font-size: 0.8rem !important;
    }
    
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #FF1493;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }
    
    /* Global Typography adjustments for headers */
    h1, h2, h3, h4, h5, h6 {
        color: #4A1525 !important;
        font-weight: 700 !important;
    }
    h3 { font-size: 1.1rem !important; }
    h4 { font-size: 0.95rem !important; }
    
    /* Streamlit Metric Container Overrides */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FFC0CB !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }
    div[data-testid="stMetricLabel"] > div {
        font-size: 0.75rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FF1493 !important;
        font-weight: 800 !important;
        font-size: 1.4rem !important;
    }

    /* Styling Alert Info Blocks to soft rose tints and small text */
    .stAlert div {
        font-size: 0.825rem !important;
    }
    .stAlert {
        background-color: #FFE4E1 !important; /* Misty Rose */
        border-left: 5px solid #FF69B4 !important;
        border-radius: 10px;
        padding: 0.75rem !important;
    }
    
    /* Force smaller font structure inside tables and input widgets */
    .stDataFrame, div[data-testid="stTable"] {
        font-size: 0.8rem !important;
    }
    .stCaption {
        font-size: 0.75rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. TOP PORTAL HEADER NAVIGATION BAR ---
st.markdown("""
    <div class="custom-navbar">
        <div class="navbar-brand">🎓 University Student Portal — Stream Triage & Action Hub</div>
        <div class="user-profile">
            <span>Welcome, <b>Freshman Student</b></span>
            <div class="avatar">FS</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. BREADCRUMB & LIVE SYNC STATUS ---
st.markdown("""
    <div class="portal-header-box">
        <div>
            <h2>💗 College Sync Dashboard</h2>
            <p style="color: #64748b; margin: 0;">Automated Local Filtering & Command Matrix Overview</p>
        </div>
        <div style="font-size: 0.8rem; color: #4A1525;">
            <span class="status-dot"></span>Active Simulation Feed Connected
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. METRIC QUICK PINS GRID (Updated with 8.5/10 CGPA) ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="🎯 Target Semester CGPA", value="8.5 / 10")
with m2:
    st.metric(label="🏠 Residence Room", value="Block A - 304")
with m3:
    st.metric(label="🏫 Daily Lecture Base", value="LT-3 (Engineering)")
with m4:
    st.metric(label="🌸 Active Club Badges", value="4 Active Streams")

st.markdown("---")

# --- 4. STREAM LAYOUT ENGINE (Sidebar Control Block + Voice Interface Hub) ---
col_left, col_right = st.columns([1, 3]) # Makes left panel tighter, right matrix wide

with col_left:
    st.markdown("### 🎛️ Feed Stream Triage")
    selected_stream = st.selectbox(
        "Select Active Feed Stream Channel:",
        options=list(st.session_state.assignments_store.keys())
    )
    
    st.markdown("---")
    st.markdown("### 🎙️ Voice Assistant Hub")
    st.caption("💖 Record audio or type a quick reminder below:")
    
    # Audio recorder widget
    audio_input = st.audio_input("Record Voice Action Command")
    
    # Process audio input text fallback box for seamless local integration execution
    voice_command = st.text_input("Or type spoken action phrase directly here:", placeholder="e.g., Submit lab file at 10 AM")
    
    if st.button("⚡ Execute Command", use_container_width=True):
        if voice_command:
            clean_cmd = voice_command.strip()
            if "at" in clean_cmd.lower() or "am" in clean_cmd.lower() or "pm" in clean_cmd.lower() or "deadline" in clean_cmd.lower():
                st.session_state.deadlines_store[selected_stream].append(clean_cmd)
                st.success(f"Added to Deadlines!")
            else:
                st.session_state.assignments_store[selected_stream].append(clean_cmd)
                st.success(f"Added to Assignments!")
            st.rerun()
        else:
            st.warning("Please type a command block phrase.")

# --- 5. THE FOUR COMPONENT VISUAL ACTION MATRIX BOARD (Cleanly Aligned Spacing) ---
with col_right:
    chat_links = {
        "✨ Group 1: Official CS Freshmen Batch '26": "• [🌐 Join Google Meet](https://google.com)\n• [💬 Join WhatsApp Subgroup](https://whatsapp.com)",
        "🍔 Group 2: Hostel Block-A Banter & Mess": "• [📝 Fill Menu Form](https://forms.gle)\n• [💬 Join Table Tennis Chat](https://whatsapp.com)",
        "🤖 Group 3: AI/ML Student Club (Un-Official)": "• [🏆 Register on Devpost](https://devpost.com)\n• [💬 Join Dev Projects Group](https://whatsapp.com)",
        "🎨 Group 4: Cultural Fest Core Committee '26": "• [📝 Fill Volunteer Sign-up](https://forms.gle)\n• [💬 Join Creative Team Chat](https://whatsapp.com)",
        "🍿 Group 5: Block-A Third Floor Wing-Mates": "• [🍿 Access Movie Vote Poll](https://forms.gle)\n• [💬 Join Snacks Run Chat](https://whatsapp.com)"
    }
    
    chat_summaries = {
        "✨ Group 1: Official CS Freshmen Batch '26": "CR Rahul announced a mandatory guest lecture for today. Professor Mehta provided syllabus details regarding an upcoming lab evaluation.",
        "🍔 Group 2: Hostel Block-A Banter & Mess": "The Warden issued a clean-room directive for an active inspection happening later tonight. The community is gathering votes to adjust the culinary selections.",
        "🤖 Group 3: AI/ML Student Club (Un-Official)": "The Lead Developer issued a final reminder for upcoming competitive hackathon registrations. The core group sync time was finalized.",
        "🎨 Group 4: Cultural Fest Core Committee '26": "Volunteers are needed urgently to handle logistics for the introductory winter carnival night. Design work templates are open.",
    }
    chat_summaries = {
        "✨ Group 1: Official CS Freshmen Batch '26": "CR Rahul announced a mandatory guest lecture for today. Professor Mehta provided syllabus details regarding an upcoming lab evaluation.",
        "🍔 Group 2: Hostel Block-A Banter & Mess": "The Warden issued a clean-room directive for an active inspection happening later tonight. The community is gathering votes to adjust the culinary selections.",
        "🤖 Group 3: AI/ML Student Club (Un-Official)": "The Lead Developer issued a final reminder for upcoming competitive hackathon registrations. The core group sync time was finalized.",
        "🎨 Group 4: Cultural Fest Core Committee '26": "Volunteers are needed urgently to handle logistics for the introductory winter carnival night. Design work templates are open.",
        "🍿 Group 5: Block-A Third Floor Wing-Mates": "Hostel residents are pooling orders for weekend food delivery and planning a movie night in the common room lounge area."
    }

    st.markdown("### 📊 Live Information Matrix Board")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("#### 📝 Chat Summary")
        st.info(chat_summaries[selected_stream])
        
    with c2:
        st.markdown("#### 📚 Assignments")
        st.caption("💖 Double-click below to modify:")
        df_asg = pd.DataFrame({"Current Homework": st.session_state.assignments_store[selected_stream]})
        edited_asg = st.data_editor(df_asg, num_rows="dynamic", use_container_width=True, key=f"asg_ed_{selected_stream}")
        st.session_state.assignments_store[selected_stream] = edited_asg["Current Homework"].tolist()
        
    with c3:
        st.markdown("#### 📅 Deadlines / Calendar")
        st.caption("💖 Modify or append rows:")
        df_dl = pd.DataFrame({"Target Deadlines": st.session_state.deadlines_store[selected_stream]})
        edited_dl = st.data_editor(df_dl, num_rows="dynamic", use_container_width=True, key=f"dl_ed_{selected_stream}")
        st.session_state.deadlines_store[selected_stream] = edited_dl["Target Deadlines"].tolist()
        
    with c4:
        st.markdown("#### 🔗 Links to Join")
        st.markdown(chat_links[selected_stream])

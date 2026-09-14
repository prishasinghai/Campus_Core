import streamlit as st
import pandas as pd

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

# --- GLOBAL STYLING: OFF-WHITE BACKGROUND, DARK BROWN & EXPLICIT BAR HEADER ---
st.markdown("""
    <style>
    /* Global Core Framework Overrides - Premium Warm Off-White */
    .stApp {
        background-color: #FAF9F6 !important;
        font-size: 0.85rem !important;
    }
    
    /* Top Professional University Styled Navbar - Matched Exactly to Your Image */
    .custom-navbar {
        background-color: #cf0864 !important; /* Solid vibrant pink background */
        padding: 0.75rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: none !important;
    }
    .navbar-brand {
        color: #FFFFFF !important; /* Bold White Title Text */
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
        color: #000000 !important; /* Black Welcome text to match your image */
        font-size: 0.85rem;
        font-weight: 600;
    }
    .avatar {
        width: 32px;
        height: 32px;
        background-color: #000000 !important; /* Black circular avatar badge */
        color: #FFFFFF !important; /* White FS initials */
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    /* Portal header message card box */
    div.portal-header-box {
        background-color: #FFFFFF;
        border: 1px solid #D2B48C;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(61, 35, 20, 0.05);
    }
    div.portal-header-box h2 {
        color: #cf0864 !important; /* RASPBERRY TITLE */
        font-size: 1.2rem !important;
        margin: 0;
    }
    div.portal-header-box p {
        color: #5C4033 !important;
    }
    
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #cf0864;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }
    
    /* Typography Global Rules forced to deep Raspberry #cf0864 */
    h1, h2, h3, h4, h5, h6 {
        color: #cf0864 !important;
        font-weight: 700 !important;
    }
    h3 { font-size: 1.1rem !important; }
    h4 { font-size: 0.95rem !important; margin-bottom: 0.5rem !important;}
    
    p, span, label, div {
        color: #3D2314 !important; /* Base texts default to Dark Brown */
    }
    
    /* Streamlit Metric Card Container & Text Customization matching #8f043e */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #8f043e !important; /* Changes the card border to your berry color */
        border-radius: 15px !important;
        padding: 10px !important;
    }
    
    /* Changes small top labels (e.g., Target Semester CGPA) to your berry color */
    div[data-testid="stMetricLabel"] > div, 
    div[data-testid="stMetricLabel"] span, 
    div[data-testid="stMetricLabel"] p {
        color: #8f043e !important; 
        font-size: 0.75rem !important;
    }
    
    /* Changes the big bottom text values (e.g., 8.5 / 10) to your berry color */
    div[data-testid="stMetricValue"] {
        color: #8f043e !important; 
        font-weight: 800 !important;
        font-size: 1.4rem !important;
    }

    /* Target native containers to create clean, solid background squares exactly under the metrics */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FAF9F6 !important; /* Darker off-white shading box tint */
        border: 1px solid #D1C9BC !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.02) !important;
    }

    /* Soft Alert Box settings */
    .stAlert {
        background-color: #FFFFFF !important; 
        border-left: 5px solid #cf0864 !important;
        border-radius: 8px;
        padding: 0.75rem !important;
    }
    
    .stDataFrame, div[data-testid="stTable"] {
        font-size: 0.8rem !important;
    }
    .stCaption {
        font-size: 0.75rem !important;
        color: #5C4033 !important;
    }
    
    /* Navigation execute functional button override */
    div.stButton > button:first-child {
        background-color: #cf0864 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold;
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
            <p style="margin: 0; font-size: 0.8rem;">Automated Local Filtering & Pair Container Matrix Overview</p>
        </div>
        <div style="font-size: 0.8rem; color: #3D2314;">
            <span class="status-dot"></span>Active Simulation Feed Connected
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. METRIC QUICK PINS GRID ---
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

# --- 4. STREAM LAYOUT ENGINE ---
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 🎛️ Feed Stream Triage")
    selected_stream = st.selectbox(
        "Select Active Feed Stream Channel:",
        options=list(st.session_state.assignments_store.keys())
    )
    
    st.markdown("---")
    st.markdown("### 🎙️ Voice Assistant Hub")
    st.caption("💖 Record audio input or drop text note below:")
    
    # Audio recorder native widget block
    audio_input = st.audio_input("Record Voice Action Command")
    
    # Text helper entry box
    voice_command = st.text_input("Or input spoken phrase action directly:", placeholder="e.g., Submit lab file at 10 AM")
    
    if st.button("⚡ Execute Command Direct to Calendar", use_container_width=True):
        if voice_command:
            clean_cmd = voice_command.strip()
            st.session_state.deadlines_store[selected_stream].append(clean_cmd)
            st.success(f"Successfully dropped directly to your Calendar matrix!")
            st.rerun()
        else:
            st.warning("Please input or speak an entry block first.")

# --- 5. THE PAIRED NATIVE CONTAINER HUB ---
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
        "🍿 Group 5: Block-A Third Floor Wing-Mates": "Hostel residents are pooling orders for weekend food delivery and planning a movie night in the common room lounge area."
    }

    st.markdown("### 📊 Live Information Matrix Board")
    
    # Define two main columns for our paired boxes
    card_col1, card_col2 = st.columns(2)
    
    # COLUMN PAIR 1: SUMMARY & CALENDAR (Wrapped in a unified background square)
    with card_col1:
        with st.container(border=True):
            st.markdown("#### 📝 Chat Summary")
            st.info(chat_summaries[selected_stream])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("#### 📅 Deadlines / Calendar")
            st.caption("💖 Modify or append rows:")
            df_dl = pd.DataFrame({"Target Deadlines": st.session_state.deadlines_store[selected_stream]})
            edited_dl = st.data_editor(df_dl, num_rows="dynamic", use_container_width=True, key=f"dl_ed_{selected_stream}")
            st.session_state.deadlines_store[selected_stream] = edited_dl["Target Deadlines"].tolist()
        
    # COLUMN PAIR 2: ASSIGNMENTS & LINKS (Wrapped in a unified background square)
    with card_col2:
        with st.container(border=True):
            st.markdown("#### 📚 Assignments")
            st.caption("💖 Double-click below to modify rows:")
            df_asg = pd.DataFrame({"Current Homework": st.session_state.assignments_store[selected_stream]})
            edited_asg = st.data_editor(df_asg, num_rows="dynamic", use_container_width=True, key=f"asg_ed_{selected_stream}")
            st.session_state.assignments_store[selected_stream] = edited_asg["Current Homework"].tolist()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("#### 🔗 Links to Join")
            st.markdown(chat_links[selected_stream])

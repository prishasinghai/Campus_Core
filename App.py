import streamlit as st
import pandas as pd

# Configure page settings
st.set_page_config(page_title="College Sync: Ultimate Pink Matrix", page_icon="💖", layout="wide")

# Custom Injecting CSS for an Ultra-Pink, Soft Pastel Aesthetic
st.markdown("""
    <style>
    /* Main body workspace colors */
    .stApp {
        background-color: #FFF0F5 !important; /* Lavender Blush/Soft Pink background */
    }
    
    /* Elegant typography overrides */
    h1 {
        color: #C71585 !important; /* Medium Violet Red */
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 800 !important;
        text-shadow: 1px 1px 4px rgba(199, 21, 133, 0.1);
    }
    h2, h3, p, span, label {
        color: #5C134F !important; /* Deep Plum Text */
        font-weight: 600;
    }
    
    /* Pinned metric layout customization with glowing pink borders */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #FF69B4 !important; /* Hot Pink Border */
        border-radius: 20px !important;
        padding: 18px !important;
        box-shadow: 0px 4px 15px rgba(255, 105, 180, 0.2) !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #FF1493 !important; /* Deep Pink numbers */
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    /* Styling Alert Info Blocks to soft rose tints */
    .stAlert {
        background-color: #FFE4E1 !important; /* Misty Rose */
        border-left: 5px solid #FF69B4 !important;
        border-radius: 10px;
    }
    
    /* Make the dropdown menu pop with a pink highlight */
    div[data-baseweb="select"] {
        border: 1px solid #FFB6C1 !important;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title Layout
st.title("💖 College Sync: The Ultimate Coquette Dashboard")
st.subheader("Filter through freshman chat clutter with ease. Click directly inside tables to manually customize tasks!")

st.markdown("---")

# --- SECTION 1: EXTENDED PINNED PIN DETAILS ---
st.markdown("### 📌 Pinned Student Quick-Stats")
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric(label="🎯 Target Semester GPA", value="3.85 / 4.0")
with m2:
    st.metric(label="🏠 Room Assignment", value="Hostel Block A - 304")
with m3:
    st.metric(label="🏫 Daily Lecture Base", value="LT-3 (Engineering)")
with m4:
    st.metric(label="🌸 Campus Activity Points", value="12 / 50 Credits")
with m5:
    st.metric(label="🎒 Semester Club Badges", value="3 Active Pins")

st.markdown("---")

# --- SECTION 2: ULTIMATE CHAT REPOSITORY WITH EXTRA WHATSAPP LINKS ---
PROCESSED_CHATS = {
    "✨ Group 1: Official CS Freshmen Batch '26": {
        "summary": "CR Rahul announced a mandatory guest lecture for today. Professor Mehta provided syllabus details regarding an upcoming lab evaluation.",
        "assignments": ["Review Chapters 1 through 3"],
        "deadlines": ["Guest Lecture (2:00 PM today)", "Lab Quiz 1 (Friday morning)"],
        "links": "• [🌐 Join Google Meet Room](https://google.com)\n• [💬 Join WhatsApp Lab Subgroup](https://whatsapp.com)"
    },
    "🍔 Group 2: Hostel Block-A Banter & Mess": {
        "summary": "The Warden issued a clean-room directive for an active inspection happening later tonight. The community is gathering votes to adjust the culinary selections.",
        "assignments": ["Organize living quarters", "Submit preferred dining choices"],
        "deadlines": ["Room Inspection (9:00 PM tonight)", "Form Submission Cutoff (11:59 PM)"],
        "links": "• [📝 Fill Menu Feedback Form](https://forms.gle)\n• [💬 Join Hostel Table Tennis Chat](https://whatsapp.com)"
    },
    "🤖 Group 3: AI/ML Student Club (Un-Official)": {
        "summary": "The Lead Developer issued a final reminder for upcoming competitive hackathon registrations. The core group sync time was finalized.",
        "assignments": ["Find project teammates", "Install Python dependencies setup script"],
        "deadlines": ["Hackathon Registration closes soon", "Weekly Sync Meet (Sunday 6:00 PM)"],
        "links": "• [🏆 Register on Devpost](https://devpost.com)\n• [💬 Join WhatsApp Dev Projects Group](https://whatsapp.com)"
    },
    "🎨 Group 4: Cultural Fest Core Committee '26 (NEW!)": {
        "summary": "Volunteers are needed urgently to handle logistics for the introductory winter carnival night. Design work templates are open.",
        "assignments": ["Draft event layout plan", "Design social graphics on Canva"],
        "deadlines": ["Volunteer Onboarding Form (By Thursday 5 PM)", "Theme Reveal Poster Draft (Friday midnight)"],
        "links": "• [📝 Fill Core Volunteer Sign-up Form](https://forms.gle)\n• [💬 Join WhatsApp Creative Team Chat](https://whatsapp.com)\n• [💬 Join WhatsApp Decoration Sub-Group](https://whatsapp.com)"
    },
    "🍿 Group 5: Block-A Third Floor Wing-Mates (NEW!)": {
        "summary": "Hostel residents are pooling orders for weekend food delivery and planning a movie night in the common room lounge area.",
        "assignments": ["Send share of pizza pool money to room 312", "Vote for movie choice on poll"],
        "deadlines": ["Pizza Money Collection deadline (Saturday 6 PM)", "Movie Night begins (Saturday 9:30 PM)"],
        "links": "• [🍿 Access Shared Movie Vote Poll](https://forms.gle)\n• [💬 Join WhatsApp Night Canteen Run Chat](https://whatsapp.com)"
    },
    "🎉 Group 6: Freshman Mixer & Socials 2026": {
        "summary": "The Student Council is organizing an icebreaker mixer night. Registrations are required to secure entry passes and free snacks.",
        "assignments": ["Coordinate carpool options with wingmates", "Confirm food preference choices"],
        "deadlines": ["Mixer Night Event (Saturday at 7:00 PM)", "Pass Registration Closes (Thursday noon)"],
        "links": "• [🎟️ Grab Entry Pass Here](https://forms.gle)\n• [💬 Join Official WhatsApp Carpool Network](https://whatsapp.com)"
    },
    "⚽ Group 7: Inter-College Football Selection Tryouts": {
        "summary": "The sports department released the initial schedule for physical fitness trials and tryouts for the varsity team jersey pool.",
        "assignments": ["Bring printed copy of medical clearance slip", "Pack workout kit and cleats"],
        "deadlines": ["Morning Fitness Tryouts (Wednesday 6:30 AM)", "Document Upload (Tonight 8:00 PM)"],
        "links": "• [📋 Upload Fitness Clearance Certificates](https://college.edu)\n• [💬 Join WhatsApp Varsity Practice Alerts](https://whatsapp.com)"
    },
    "📧 Email: Academic Dean Notification": {
        "summary": "The Academic Dean published the scheduling grid for midterms alongside strict parameters regarding immediate assignment submissions.",
        "assignments": ["Upload Calculus sheet to LMS", "Finalize Physics documentation"],
        "deadlines": ["Midterm Exams start next Monday", "LMS Upload Cutoff (Sunday at 11:59 PM)"],
        "links": "• [📑 Access Academic Exam Portal](https://college.edu)"
    }
}

# Dropdown selection for your active streams
selected_stream = st.selectbox(
    "🌸 Choose an incoming stream channel to inspect:",
    options=list(PROCESSED_CHATS.keys())
)

st.markdown("---")

# --- SECTION 3: THE HIGH-CONTRAST 4-COLUMN MATRIX BOARD ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 📝 Quick Digest")
    st.info(PROCESSED_CHATS[selected_stream]["summary"])
    
with col2:
    st.markdown("### 📚 Assignments")
    st.caption("✨ Add tasks or rewrite rows directly below:")
    df_assignments = pd.DataFrame({"Tasks & Homework": PROCESSED_CHATS[selected_stream]["assignments"]})
    edited_assignments = st.data_editor(df_assignments, num_rows="dynamic", use_container_width=True)
    
with col3:
    st.markdown("### 📅 Deadlines & Events")
    st.caption("✨ Keep track of dates effortlessly:")
    df_deadlines = pd.DataFrame({"Target Deadlines": PROCESSED_CHATS[selected_stream]["deadlines"]})
    edited_deadlines = st.data_editor(df_deadlines, num_rows="dynamic", use_container_width=True)
    
with col4:
    st.markdown("### 🔗 Join Group Links")
    st.markdown(PROCESSED_CHATS[selected_stream]["links"])

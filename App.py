import streamlit as st
import pandas as pd

# Configure page settings
st.set_page_config(page_title="College Sync: Matrix Board", page_icon="🎓", layout="wide")

# Custom Injecting CSS for a Beautiful Pink & White Aesthetic
st.markdown("""
    <style>
    /* Primary brand colors */
    :root {
        --primary-color: #FF69B4;
    }
    
    /* Background color overrides */
    .stApp {
        background-color: #FFF5F7;
    }
    
    /* Title text colors */
    h1, h2, h3, p {
        color: #4A1525 !important;
    }
    
    /* Styled container blocks */
    div[data-testid="stMetricValue"] {
        color: #FF1493;
    }
    
    /* Modify standard streamlit buttons to be bright pink */
    div.stButton > button:first-child {
        background-color: #FF69B4 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px;
        padding: 0.5rem 2rem;
    }
    div.stButton > button:first-child:hover {
        background-color: #FF1493 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("💗 College Sync")
st.subheader("Your personalized pink academic dashboard. Click into the tables below to type or add items manually!")

# Pre-packaged parsed data matrices
PROCESSED_CHATS = {
    "✨ Group 1: Official CS Freshmen Batch '26": {
        "summary": "CR Rahul announced a mandatory guest lecture for today. Professor Mehta provided syllabus details regarding an upcoming lab evaluation.",
        "assignments": ["Review Chapters 1 through 3"],
        "deadlines": ["Guest Lecture (2:00 PM today)", "Lab Quiz 1 (Friday morning)"],
        "links": "[🌐 Join Google Meet Room](https://google.com)"
    },
    "🍔 Group 2: Hostel Block-A Banter & Mess": {
        "summary": "The Warden issued a clean-room directive for an active inspection happening later tonight. The community is gathering votes to adjust the culinary selections.",
        "assignments": ["Organize living quarters", "Submit preferred dining choices"],
        "deadlines": ["Room Inspection (9:00 PM tonight)", "Form Submission Cutoff (11:59 PM)"],
        "links": "[📝 Fill Menu Feedback Form](https://forms.gle)"
    },
    "🤖 Group 3: AI/ML Student Club (Un-Official)": {
        "summary": "The Lead Developer issued a final reminder for upcoming competitive hackathon registrations. The core group sync time was finalized.",
        "assignments": ["Find project teammates"],
        "deadlines": ["Hackathon Registration closes soon", "Weekly Sync Meet (Sunday 6:00 PM)"],
        "links": "[🏆 Register on Devpost](https://devpost.com)"
    },
    "📧 Email: Academic Dean Notification": {
        "summary": "The Academic Dean published the scheduling grid for midterms alongside strict parameters regarding immediate assignment submissions.",
        "assignments": ["Upload Calculus sheet to LMS", "Finalize Physics documentation"],
        "deadlines": ["Midterm Exams start next Monday", "LMS Upload Cutoff (Sunday at 11:59 PM)"],
        "links": "[📑 Access Academic Exam Portal](https://college.edu)"
    }
}

# Dropdown selection for your active streams
selected_stream = st.selectbox(
    "🌸 Choose a notification channel stream to view:",
    options=list(PROCESSED_CHATS.keys())
)

st.markdown("---")

# Render the 4 columns requested by reading local storage matrices
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 📝 Chat Summary")
    st.info(PROCESSED_CHATS[selected_stream]["summary"])
    
with col2:
    st.markdown("### 📚 Assignments")
    st.caption("✨ Double-click cells to edit or add rows at the bottom")
    # Convert lists to a DataFrame so they are fully interactive and editable
    df_assignments = pd.DataFrame({"Your Assignments": PROCESSED_CHATS[selected_stream]["assignments"]})
    edited_assignments = st.data_editor(df_assignments, num_rows="dynamic", use_container_width=True)
    
with col3:
    st.markdown("### 📅 Calendar / Deadlines")
    st.caption("✨ Add personal events directly into this card stream")
    df_deadlines = pd.DataFrame({"Deadlines / Events": PROCESSED_CHATS[selected_stream]["deadlines"]})
    edited_deadlines = st.data_editor(df_deadlines, num_rows="dynamic", use_container_width=True)
    
with col4:
    st.markdown("### 🔗 Links to Join")
    st.success(PROCESSED_CHATS[selected_stream]["links"])

import streamlit as st
import re

# Configure page settings
st.set_page_config(page_title="College Sync: Local Matrix", page_icon="🎓", layout="wide")

# App Header
st.title("🎓 College Sync: Multi-Chat Digest")
st.subheader("Local rule-based layout module running with 0% API overhead.")

# Pre-analyzed data repository matching the selected college streams
PROCESSED_CHATS = {
    "✨ Group 1: Official CS Freshmen Batch '26": {
        "raw": """[10:15 AM] CR Rahul: @everyone Attendance is mandatory for the guest lecture today at 2 PM in Seminar Hall 2. 
[10:17 AM] Sneha: Is there a link for online joining? 
[10:19 AM] CR Rahul: Yes, for hostellers who are sick join here: https://google.com
[11:02 AM] Prof. Mehta: Please note that the Lab Quiz 1 syllabus covers Chapters 1 to 3. It will happen this Friday morning.""",
        "summary": "CR Rahul announced a mandatory guest lecture for today. Professor Mehta provided syllabus details regarding an upcoming lab evaluation.",
        "assignments": "• **Lab Quiz 1 Prep**:\nStudy Chapters 1 through 3.",
        "deadlines": "• **Guest Lecture**: Today at 2:00 PM (Seminar Hall 2)\n• **Lab Quiz 1**: This Friday morning",
        "links": "[🌐 Join Google Meet Room](https://google.com)"
    },
    
    "🍔 Group 2: Hostel Block-A Banter & Mess": {
        "raw": """[08:00 AM] Warden: Inspection tonight at 9 PM. Keep rooms clean.
[12:30 PM] Kabir: Who has the link to the Google Form to change the mess menu? 
[12:32 PM] Amit: Here bro: https://forms.gle. Fill it before midnight tonight or we are stuck with paneer every day.
[02:15 PM] Raj: Forgot my ID card at the mess. If anyone finds it please DM.""",
        "summary": "The Warden issued a clean-room directive for an active inspection happening later tonight. The community is gathering votes to adjust the culinary selections.",
        "assignments": "• **Room Cleanup**:\nOrganize living quarters for review.\n• **Menu Ballot**:\nSubmit preferred dining choices.",
        "deadlines": "• **Room Inspection**: Tonight at 9:00 PM\n• **Form Submission**: Tonight before 11:59 PM",
        "links": "[📝 Fill Menu Feedback Form](https://forms.gle)"
    },
    
    "🤖 Group 3: AI/ML Student Club (Un-Official)": {
        "raw": """[04:00 PM] Lead Dev: Hackathon registrations are closing day after tomorrow! Team up fast.
[04:05 PM] Ishan: What's the link to register?
[04:06 PM] Lead Dev: Register here: https://devpost.com. Cash prize is $500.
[05:20 PM] Dev: Also we have our weekly sync on Sunday at 6 PM on Discord.""",
        "summary": "The Lead Developer issued a final reminder for upcoming competitive hackathon registrations. The core group sync time was finalized.",
        "assignments": "• **Team Formulation**:\nFind members for the competitive sprint.",
        "deadlines": "• **Hackathon Registration Closes**: Day after tomorrow\n• **Weekly Sync Meet**: Sunday at 6:00 PM",
        "links": "[🏆 Register on Devpost](https://devpost.com)"
    },
    
    "📧 Email: Academic Dean Notification": {
        "raw": """From: academicdean@college.edu
Subject: Mid-Semester Timetable and Academic Warning
Dear Students,
Please find the attached link to view your midterm examination slots starting next Monday: https://college.edu. 
Your course assignments for Calculus and Applied Physics must be uploaded to the LMS portal no later than Sunday, September 21, at 11:59 PM. No late submissions will be entertained.""",
        "summary": "The Academic Dean published the scheduling grid for midterms alongside strict parameters regarding immediate assignment submissions.",
        "assignments": "• **Calculus Assignment**:\nUpload complete sheets to LMS.\n• **Applied Physics Assignment**:\nFinalize and post documentation.",
        "deadlines": "• **Midterm Examination Cycle**: Starts next Monday\n• **LMS Portal Upload Cutoff**: Sunday, September 21 at 11:59 PM",
        "links": "[📑 Access Academic Exam Portal](https://college.edu)"
    }
}

# Dropdown selection for mock streams
selected_stream = st.selectbox(
    "💬 Select an incoming notification stream to process:",
    options=list(PROCESSED_CHATS.keys())
)

# Display the raw feed container
with st.expander("🔍 View Raw Incoming Feed", expanded=True):
    st.code(PROCESSED_CHATS[selected_stream]["raw"], language="text")

st.markdown("---")

# Render the 4 columns requested by reading local storage matrices
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 📝 Chat Summary")
    st.info(PROCESSED_CHATS[selected_stream]["summary"])
    
with col2:
    st.markdown("### 📚 Assignments")
    st.error(PROCESSED_CHATS[selected_stream]["assignments"])
    
with col3:
    st.markdown("### 📅 Calendar / Deadlines")
    st.warning(PROCESSED_CHATS[selected_stream]["deadlines"])
    
with col4:
    st.markdown("### 🔗 Links to Join")
    st.success(PROCESSED_CHATS[selected_stream]["links"])

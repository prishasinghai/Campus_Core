import streamlit as st
import google.generativeai as genai
import json

# Configure page settings
st.set_page_config(page_title="College Sync: Feed Summarizer", page_icon="🎓", layout="wide")

# App Header
st.title("🎓 College Sync: Multi-Chat Digest")
st.subheader("Simulating real-time parsing of chaotic freshman group chats and emails.")

# Mock data simulating a student's unread notification feeds
MOCK_CHATS = {
    "✨ Group 1: Official CS Freshmen Batch '26": """
    [10:15 AM] CR Rahul: @everyone Attendance is mandatory for the guest lecture today at 2 PM in Seminar Hall 2. 
    [10:17 AM] Sneha: Is there a link for online joining? 
    [10:19 AM] CR Rahul: Yes, for hostellers who are sick join here: https://google.com
    [11:02 AM] Prof. Mehta: Please note that the Lab Quiz 1 syllabus covers Chapters 1 to 3. It will happen this Friday morning.
    """,
    
    "🍔 Group 2: Hostel Block-A Banter & Mess": """
    [08:00 AM] Warden: Inspection tonight at 9 PM. Keep rooms clean.
    [12:30 PM] Kabir: Who has the link to the Google Form to change the mess menu? 
    [12:32 PM] Amit: Here bro: https://forms.gle. Fill it before midnight tonight or we are stuck with paneer every day.
    [02:15 PM] Raj: Forgot my ID card at the mess. If anyone finds it please DM.
    """,
    
    "🤖 Group 3: AI/ML Student Club (Un-Official)": """
    [04:00 PM] Lead Dev: Hackathon registrations are closing day after tomorrow! Team up fast.
    [04:05 PM] Ishan: What's the link to register?
    [04:06 PM] Lead Dev: Register here: https://devpost.com. Cash prize is $500.
    [05:20 PM] Dev: Also we have our weekly sync on Sunday at 6 PM on Discord.
    """,
    
    "📧 Email: Academic Dean Notification": """
    From: academicdean@college.edu
    Subject: Mid-Semester Timetable and Academic Warning
    Dear Students,
    Please find the attached link to view your midterm examination slots starting next Monday: https://college.edu. 
    Your course assignments for Calculus and Applied Physics must be uploaded to the LMS portal no later than Sunday, September 21, at 11:59 PM. No late submissions will be entertained.
    """
}

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.caption("Get a free key from the Google AI Studio website.")
    st.markdown("---")
    st.markdown("### Active Feeds")
    st.write(f"Connected to **{len(MOCK_CHATS)}** active stream simulation modules.")

# Dropdown selection for mock data
selected_stream = st.selectbox(
    "💬 Select an incoming notification stream to process:",
    options=list(MOCK_CHATS.keys())
)

# Preview the raw content
with st.expander("🔍 View Raw Stream Content", expanded=True):
    st.code(MOCK_CHATS[selected_stream], language="text")

if st.button("⚡ Parse Stream Into Matrix", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar to extract structured intelligence.")
    else:
        # Initialize Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Construct prompt enforcing JSON back-end structure for reliable column distribution
        prompt = f"""
        You are a data extraction script for a college student dashboard. 
        Analyze the following text extract and format your response strictly as a JSON object with exactly these four keys:
        "summary": "A clean, bulleted 1-2 sentence breakdown summarizing what happened in this chat.",
        "assignments": "Extract any concrete graded assignments, homework, tasks, quizzes, or project deliverables mentioned. If none, write 'None declared'.",
        "deadlines": "Extract dates, specific deadlines, event timings, or exam dates mentioned. If none, write 'No schedule changes'.",
        "links": "Extract raw click-through URLs, Google Forms, WhatsApp groups, or Google Meet links. Format them as clickable Markdown links or lists. If none, write 'No links shared'."

        Raw Text content to parse:
        {MOCK_CHATS[selected_stream]}

        Respond ONLY with the raw JSON structure, nothing else. Do not wrap it inside a code block block quote.
        """
        
        with st.spinner("Extracting structured matrices..."):
            try:
                response = model.generate_content(prompt)
                clean_json_text = response.text.strip().replace("```json", "").replace("```", "")
                
                # Parse JSON string from AI
                parsed_data = json.loads(clean_json_text)
                
                st.success("✨ Stream Parsed Successfully!")
                st.markdown("---")
                
                # Create the four visual columns asked for
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("### 📝 Chat Summary")
                    st.info(parsed_data.get("summary", "No data"))
                    
                with col2:
                    st.markdown("### 📚 Assignments")
                    st.error(parsed_data.get("assignments", "No data"))
                    
                with col3:
                    st.markdown("### 📅 Calendar / Deadlines")
                    st.warning(parsed_data.get("deadlines", "No data"))
                    
                with col4:
                    st.markdown("### 🔗 Links to Join")
                    st.success(parsed_data.get("links", "No data"))
                    
            except Exception as e:
                st.error("Could not parse the AI payload. Please verify that your API key is correct and valid.")
                st.info("Debugging context: Make sure Gemini returned a valid JSON format.")

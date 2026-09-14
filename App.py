import streamlit as st
import google.generativeai as genai
import urllib.parse
from datetime import datetime

# Configure page settings
st.set_page_config(page_title="College Sync: WhatsApp & Email Digest", page_icon="🎓", layout="wide")

# App Header
st.title("🎓 College Sync")
st.subheader("Turn chaotic group chats and emails into a clean, actionable daily plan.")

# Sidebar for API Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.caption("Get a free key from the Google AI Studio website.")
    
    st.markdown("---")
    st.markdown("### How to use:")
    st.write("1. Copy a chunk of text from your noisy WhatsApp group or student email.")
    st.write("2. Paste it in the text box.")
    st.write("3. Click 'Process' to let AI organize your day!")

# Text input for chaotic data
chat_input = st.text_area(
    "Paste your WhatsApp chat logs or Email content here:",
    height=300,
    placeholder="[11:42 AM] Prof. Sharma: Reminder that the Calculus assignment submission deadline is extended to tomorrow 4 PM. Also, please join the official Lab group here: https://whatsapp.com..."
)

# Function to generate Google Calendar Link
def create_cal_link(title, date_str, details="Added via College Sync"):
    base_url = "https://google.com"
    text = urllib.parse.quote(title)
    # Formats a basic generic all-day date format YYYYMMDD
    formatted_date = datetime.today().strftime('%Y%m%d') 
    url = f"{base_url}&text={text}&dates={formatted_date}/{formatted_date}&details={urllib.parse.quote(details)}"
    return url

if st.button("Process & Plan My Day", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar to proceed.")
    elif not chat_input.strip():
        st.warning("Please paste some chat logs or email content first.")
    else:
        # Initialize Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # System instructions to enforce the parsing behavior
        prompt = f"""
        You are a highly efficient AI administrative assistant for a first-year college student. 
        Analyze the following raw WhatsApp chat logs or email texts and break them down into these exact sections:
        
        1. 📌 **Executive Summary**: A concise, 3-sentence summary of the most important things the student missed.
        2. 📅 **Actionable Deadlines & Events**: Extract every assignment deadline, exam date, class timing, or event. List them clearly with the Title and Date.
        3. 🔗 **Important Links**: Extract any group invite links (e.g., ://whatsapp.com), Discord invites, or meeting links (Zoom/Meet) explicitly mentioned.
        
        Raw Content:
        {chat_input}
        """
        
        with st.spinner("Filtering through the noise..."):
            try:
                response = model.generate_content(prompt)
                ai_output = response.text
                
                # Render results in structured columns
                st.success("Analysis Complete!")
                
                # Display Raw Summary
                st.markdown("### 📋 Your Personalized Briefing")
                st.markdown(ai_output)
                
                # Interactive Calendar Assistant Component
                st.markdown("---")
                st.markdown("### 🗓️ Quick Actions: Add to Google Calendar")
                st.info("Since we found events above, you can quickly draft a calendar placeholder below:")
                
                col1, col2 = st.columns(2)
                with col1:
                    event_title = st.text_input("Event Name:", placeholder="e.g., Calculus Assignment Due")
                with col2:
                    event_desc = st.text_input("Additional Notes:", placeholder="e.g., Submit via portal before 4 PM")
                
                if event_title:
                    cal_url = create_cal_link(event_title, datetime.today().strftime('%Y%m%d'), event_desc)
                    st.markdown(f"[➕ Click here to save '{event_title}' to Google Calendar]({cal_url})")
                    
            except Exception as e:
                st.error(f"An error occurred while communicating with the AI model: {e}")

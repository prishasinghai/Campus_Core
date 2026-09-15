import re
import streamlit as st
import pandas as pd
 
# Configure page settings
st.set_page_config(page_title="Student Chat Assistant", page_icon="🎓", layout="wide")
 
# Standardized channel keys to make sure dictionaries match perfectly
CHANNELS = [
    "✨ Group 1: Computer Science Official",
    "🍔 Group 2: Hostel Block A Notice Board",
    "🤖 Group 3: AI/ML Coding Club",
    "🎨 Group 4: College Festival Team",
    "🍿 Group 5: Roommates Chat (Floor 3)"
]
 
# Initialize storage for user tasks and calendar deadlines
if "assignments_store" not in st.session_state:
    st.session_state.assignments_store = {
        CHANNELS[0]: ["Study Lab Chapters 1 to 3"],
        CHANNELS[1]: ["Clean up room for inspection", "Vote for the new mess menu"],
        CHANNELS[2]: ["Find teammates for the hackathon", "Install Python on your laptop"],
        CHANNELS[3]: ["Make the event layout chart", "Create social media posters on Canva"],
        CHANNELS[4]: ["Pay money for weekend pizza pool", "Vote for the movie night pick"]
    }
 
if "deadlines_store" not in st.session_state:
    st.session_state.deadlines_store = {
        CHANNELS[0]: ["Guest Lecture (Today at 2:00 PM)", "Lab Quiz 1 (This Friday morning)"],
        CHANNELS[1]: ["Room Inspection (Tonight at 9:00 PM)", "Menu Form Cutoff (Tonight at 11:59 PM)"],
        CHANNELS[2]: ["Registration Deadline (Closing very soon)", "Weekly Club Meeting (Sunday at 6:00 PM)"],
        CHANNELS[3]: ["Volunteer Form Due (Thursday at 5:00 PM)", "Poster Draft Due (Friday at midnight)"],
        CHANNELS[4]: ["Pizza Pool Deadline (Saturday at 6:00 PM)", "Movie Night Starts (Saturday at 9:30 PM)"]
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
 
    /* AI Priority Assistant cards */
    .priority-card {
        background-color: #FFFFFF;
        border: 1px solid #EFECE6;
        border-left: 4px solid #cf0864;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.6rem;
    }
    .priority-card.cancelled { border-left-color: #999999; opacity: 0.7; }
    .priority-card.conflict { border-left-color: #d9534f; }
    .priority-card.limited { border-left-color: #e0a800; }
    .priority-card.registered { border-left-color: #4a8f3c; }
    .priority-card.incomplete { border-left-color: #6c757d; }
    .priority-tag {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        margin-right: 0.4rem;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)
 
# ======================================================================================
# AI PRIORITY ASSISTANT — rule-based announcement triage engine
#
# Design intent (per requirements):
#   - Surfaces deadlines, cancellations, conflicts, limited-seat opportunities and
#     already-registered events pulled from the raw channel data already in session_state.
#   - Flags repeated (duplicate) and incomplete announcements instead of silently
#     merging, deleting, or guessing at missing details.
#   - Sorts by urgency signals actually present in the text; never invents a date,
#     time, or seat count that wasn't stated.
#   - Never auto-cancels, auto-registers, or removes anything — it only labels and
#     ranks so the student can decide what to do.
# ======================================================================================
 
DAY_TOKENS = [
    "today", "tonight", "tomorrow",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
]
 
# Words/phrases that make a day-token "now-ish" for sorting purposes only.
URGENCY_RANK = {
    "today": 0, "tonight": 0,
    "tomorrow": 1,
    "monday": 2, "tuesday": 2, "wednesday": 2, "thursday": 2,
    "friday": 2, "saturday": 2, "sunday": 2,
}
 
CANCEL_KEYWORDS = ["cancelled", "canceled", "postponed", "called off", "rescheduled", "no longer happening"]
LIMITED_SEAT_KEYWORDS = ["limited seats", "few seats", "seats left", "closing soon", "closes soon",
                         "very soon", "first come", "hurry", "almost full", "few spots"]
REGISTERED_KEYWORDS = ["registered", "confirmed", "you're in", "you are in", "enrolled", "rsvp'd", "rsvped"]
 
 
def _extract_day(text):
    t = text.lower()
    for d in DAY_TOKENS:
        if re.search(rf"\b{d}\b", t):
            return d
    return None
 
 
def _has_time_detail(text):
    """A stated clock time OR a day word counts as 'has enough detail to act on'."""
    has_clock = bool(re.search(r"\d{1,2}(:\d{2})?\s*(am|pm)", text.lower()))
    return has_clock or (_extract_day(text) is not None)
 
 
def _normalize(text):
    t = re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()
    return re.sub(r"\s+", " ", t)
 
 
def _classify(text):
    t = text.lower()
    tags = set()
    if any(k in t for k in CANCEL_KEYWORDS):
        tags.add("cancelled")
    if any(k in t for k in LIMITED_SEAT_KEYWORDS):
        tags.add("limited_seats")
    if any(k in t for k in REGISTERED_KEYWORDS):
        tags.add("registered")
    if not _has_time_detail(text):
        tags.add("incomplete")
    return tags
 
 
def analyze_announcements(deadlines_store, assignments_store, channels):
    """Builds a flagged, ranked view of everything currently stored.
    Purely rule-based text matching over the student's own data — no external
    calls, no fabricated dates/seat counts. Ambiguous or missing detail is
    surfaced as 'incomplete' rather than guessed at.
    """
    entries = []
    for ch in channels:
        for item in deadlines_store.get(ch, []):
            if str(item).strip():
                entries.append({"channel": ch, "text": item, "kind": "Deadline/Event"})
        for item in assignments_store.get(ch, []):
            if str(item).strip():
                entries.append({"channel": ch, "text": item, "kind": "Task"})
 
    for e in entries:
        e["tags"] = _classify(e["text"])
        e["day"] = _extract_day(e["text"])
        e["norm"] = _normalize(e["text"])
 
    # --- Repeated / duplicate announcements (flagged, not deleted) ---
    seen = {}
    duplicate_pairs = []
    for e in entries:
        if e["norm"] in seen:
            duplicate_pairs.append((seen[e["norm"]], e))
            e["tags"].add("duplicate")
        else:
            seen[e["norm"]] = e
 
    # --- Conflicting commitments: same day, different channels, both time-bound ---
    by_day = {}
    for e in entries:
        if e["kind"] == "Deadline/Event" and e["day"] and "cancelled" not in e["tags"]:
            by_day.setdefault(e["day"], []).append(e)
 
    conflicts = []
    for day, items in by_day.items():
        channels_involved = {i["channel"] for i in items}
        if len(items) > 1 and len(channels_involved) > 1:
            conflicts.append({"day": day, "items": items})
            for i in items:
                i["tags"].add("conflict")
 
    cancelled = [e for e in entries if "cancelled" in e["tags"]]
    limited = [e for e in entries if "limited_seats" in e["tags"] and "cancelled" not in e["tags"]]
    registered = [e for e in entries if "registered" in e["tags"] and "cancelled" not in e["tags"]]
    incomplete = [e for e in entries if "incomplete" in e["tags"] and "cancelled" not in e["tags"]]
 
    # --- Action items: everything still live, not a duplicate-repeat, not purely
    #     informational (registered), ranked by urgency signal actually present.
    action_items = [
        e for e in entries
        if "cancelled" not in e["tags"] and "registered" not in e["tags"]
    ]
 
    def sort_key(e):
        conflict_first = 0 if "conflict" in e["tags"] else 1
        limited_next = 0 if "limited_seats" in e["tags"] else 1
        urgency = URGENCY_RANK.get(e["day"], 5)  # 5 = no day info -> lowest urgency confidence
        return (conflict_first, limited_next, urgency)
 
    action_items.sort(key=sort_key)
 
    return {
        "entries": entries,
        "duplicate_pairs": duplicate_pairs,
        "conflicts": conflicts,
        "cancelled": cancelled,
        "limited": limited,
        "registered": registered,
        "incomplete": incomplete,
        "action_items": action_items,
    }
 
 
def render_priority_assistant():
    st.markdown("### 🧠 AI Priority Assistant")
    st.caption(
        "Reads every stored task and deadline across all 5 channels and sorts the noise from what "
        "actually needs your attention. It only flags patterns from what was actually written — it "
        "never cancels, registers, or deletes anything, and never guesses a date or seat count that "
        "wasn't stated."
    )
 
    report = analyze_announcements(
        st.session_state.deadlines_store, st.session_state.assignments_store, CHANNELS
    )
 
    s1, s2, s3, s4, s5 = st.columns(5)
    s1.metric("⚠️ Conflicts", len(report["conflicts"]))
    s2.metric("🚫 Cancelled", len(report["cancelled"]))
    s3.metric("⏳ Limited Seats", len(report["limited"]))
    s4.metric("✅ Registered", len(report["registered"]))
    s5.metric("❓ Incomplete Info", len(report["incomplete"]))
 
    tab_priority, tab_conflicts, tab_cancelled, tab_limited, tab_registered, tab_incomplete = st.tabs(
        ["🔥 Priority Feed", "⚠️ Conflicts", "🚫 Cancelled", "⏳ Limited Seats", "✅ Registered", "❓ Incomplete"]
    )
 
    with tab_priority:
        st.caption(
            "Ranked by conflicts first, then limited-seat urgency, then how soon the stated day/time is. "
            "Items with no day or time mentioned are ranked last — not skipped — since urgency for them "
            "is unknown, not low."
        )
        if not report["action_items"]:
            st.info("Nothing pending right now.")
        for e in report["action_items"]:
            badges = ""
            if "conflict" in e["tags"]:
                badges += '<span class="priority-tag" style="background:#d9534f;">CONFLICT</span>'
            if "limited_seats" in e["tags"]:
                badges += '<span class="priority-tag" style="background:#e0a800;">LIMITED SEATS</span>'
            if "duplicate" in e["tags"]:
                badges += '<span class="priority-tag" style="background:#6c757d;">REPEATED ELSEWHERE</span>'
            if "incomplete" in e["tags"]:
                badges += '<span class="priority-tag" style="background:#6c757d;">NO DATE/TIME STATED</span>'
            css_class = "conflict" if "conflict" in e["tags"] else ("limited" if "limited_seats" in e["tags"] else "")
            st.markdown(
                f"""<div class="priority-card {css_class}">
                {badges}<b>{e['text']}</b><br>
                <span style="font-size:0.78rem;">{e['kind']} · {e['channel']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
 
    with tab_conflicts:
        st.caption(
            "Same day mentioned in two different channels. This does NOT decide which one you should "
            "attend — just flags that you have overlapping commitments to sort out yourself."
        )
        if not report["conflicts"]:
            st.info("No overlapping commitments detected.")
        for c in report["conflicts"]:
            st.markdown(f"**Possible conflict on: {c['day'].title()}**")
            for i in c["items"]:
                st.markdown(f"- {i['text']} — *{i['channel']}*")
            st.markdown("---")
 
    with tab_cancelled:
        if not report["cancelled"]:
            st.info("No cancellations detected.")
        for e in report["cancelled"]:
            st.markdown(
                f"""<div class="priority-card cancelled">
                <s>{e['text']}</s><br>
                <span style="font-size:0.78rem;">{e['kind']} · {e['channel']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
 
    with tab_limited:
        if not report["limited"]:
            st.info("No limited-seat or closing-soon opportunities detected.")
        for e in report["limited"]:
            st.markdown(
                f"""<div class="priority-card limited">
                {e['text']}<br>
                <span style="font-size:0.78rem;">{e['kind']} · {e['channel']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
 
    with tab_registered:
        st.caption("Informational only — shown so you can confirm it's still accurate, not as an action item.")
        if not report["registered"]:
            st.info("Nothing marked as registered/confirmed yet.")
        for e in report["registered"]:
            st.markdown(
                f"""<div class="priority-card registered">
                {e['text']}<br>
                <span style="font-size:0.78rem;">{e['kind']} · {e['channel']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
 
    with tab_incomplete:
        st.caption(
            "These mention no day or time, so the assistant can't tell you how urgent they are. "
            "Check the original chat for the missing detail rather than assuming."
        )
        if not report["incomplete"]:
            st.info("Everything currently stored has a day or time attached.")
        for e in report["incomplete"]:
            st.markdown(
                f"""<div class="priority-card incomplete">
                {e['text']}<br>
                <span style="font-size:0.78rem;">{e['kind']} · {e['channel']} · missing day/time</span>
                </div>""",
                unsafe_allow_html=True,
            )
 
    if report["duplicate_pairs"]:
        with st.expander(f"🔁 {len(report['duplicate_pairs'])} repeated announcement(s) found across channels"):
            st.caption("Shown so you know it's the same thing twice, not two separate commitments.")
            for original, dup in report["duplicate_pairs"]:
                st.markdown(f"- \"{original['text']}\" — seen in *{original['channel']}* and again in *{dup['channel']}*")
 
 
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
 
# --- 4. AI PRIORITY ASSISTANT (full-width, cross-channel) ---
render_priority_assistant()
 
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
 
# --- 5. DUAL COLUMN PRESENTATION HUB ---
col_left, col_right = st.columns(2)  # Fixed with structural balancing layout integers
 
with col_left:
    st.markdown("### 🎛️ Group Controller")
    selected_stream = st.selectbox(
        "Choose a Chat Group to Filter:",
        options=CHANNELS
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
 
# --- 6. CLEAN INFORMATION WORKSPACE ---
with col_right:
    chat_links = {
        CHANNELS[0]: "• [🌐 Join Online Class Link](https://google.com)\n• [💬 Join WhatsApp Lab Sub-Group](https://whatsapp.com)",
        CHANNELS[1]: "• [📝 Fill Mess Menu Feedback Form](https://forms.gle)\n• [💬 Join Hostel Sports Chat](https://whatsapp.com)",
        CHANNELS[2]: "• [🏆 Open Competition Register Page](https://devpost.com)\n• [💬 Join WhatsApp Projects Team](https://whatsapp.com)",
        CHANNELS[3]: "• [📝 Fill Student Volunteer Signup Form](https://forms.gle)\n• [💬 Join WhatsApp Design Group](https://whatsapp.com)",
        CHANNELS[4]: "• [🍿 Open Shared Movie Voting Poll](https://forms.gle)\n• [💬 Join Canteen Delivery Group](https://whatsapp.com)"
    }
    
    chat_summaries = {
        CHANNELS[0]: "The class representative announced a mandatory lecture at 2 PM today in Seminar Hall 2. Professor Mehta also shared the chapters covered in the upcoming lab evaluation.",
        CHANNELS[1]: "The hostel warden announced a room cleanliness inspection for tonight. Students are also voting on a Google Form to change the weekly mess menu options.",
        CHANNELS[2]: "The club lead shared a reminder that project registration closes very soon. The team is holding their weekly synchronization meeting this Sunday evening on Discord.",
        CHANNELS[3]: "The festival coordinators are looking for urgent student volunteers to manage logistics. Creative banners and templates are open for edits on Canva.",
        CHANNELS[4]: "Students are pooling money to place a group food order this weekend and are organizing a movie night inside the main hostel common room lounge."
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
        
    st.markdown("<br>", unsafe_allow_html=True)  # Pure clean vertical spacing
    
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
 

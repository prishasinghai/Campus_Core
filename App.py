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

# --- RAW ANNOUNCEMENT STREAM -----------------------------------------------
# The messy, unfiltered feed the assistant has to make sense of: emails, class
# groups and society channels all mixed together. Deliberately includes a
# cancellation, a repeat of the same notice in two places, an announcement with
# no date at all, an already-registered event, and two things on the same day.
if "announcement_stream" not in st.session_state:
    st.session_state.announcement_stream = [
        {"source": "📧 Email — Dept. Office", "channel": CHANNELS[0],
         "text": "Guest Lecture on Compiler Design, Today at 2:00 PM, Seminar Hall 2. Attendance mandatory."},
        {"source": CHANNELS[0], "channel": CHANNELS[0],
         "text": "Reminder: Guest Lecture on Compiler Design, Today at 2:00 PM, Seminar Hall 2. Attendance mandatory."},
        {"source": CHANNELS[0], "channel": CHANNELS[0],
         "text": "Lab Quiz 1 moved — the Friday morning slot is now confirmed. Chapters 1 to 3."},
        {"source": "📧 Email — Exam Cell", "channel": CHANNELS[0],
         "text": "The extra Data Structures tutorial scheduled for Thursday has been cancelled."},
        {"source": CHANNELS[1], "channel": CHANNELS[1],
         "text": "Room cleanliness inspection Tonight at 9:00 PM. Block A only."},
        {"source": CHANNELS[1], "channel": CHANNELS[1],
         "text": "Mess menu voting form closes Tonight at 11:59 PM."},
        {"source": CHANNELS[2], "channel": CHANNELS[2],
         "text": "Hackathon registration closing very soon — limited seats, first come first served."},
        {"source": CHANNELS[2], "channel": CHANNELS[2],
         "text": "Weekly club sync, Sunday at 6:00 PM on Discord. You are registered for this one already."},
        {"source": CHANNELS[2], "channel": CHANNELS[2],
         "text": "Bring your project idea to the next session."},
        {"source": CHANNELS[3], "channel": CHANNELS[3],
         "text": "Volunteer signup form due Thursday at 5:00 PM. Only a few spots left for the logistics team."},
        {"source": CHANNELS[3], "channel": CHANNELS[3],
         "text": "Poster draft due Friday at midnight on Canva."},
        {"source": CHANNELS[3], "channel": CHANNELS[3],
         "text": "Decoration committee meeting — venue and timing to be announced."},
        {"source": CHANNELS[4], "channel": CHANNELS[4],
         "text": "Pizza pool money collection ends Saturday at 6:00 PM."},
        {"source": CHANNELS[4], "channel": CHANNELS[4],
         "text": "Movie night Saturday at 9:30 PM in the common room."},
    ]

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

    /* --- AI Priority Assistant cards --- */
    .priority-card {
        background-color: #FFFFFF;
        border: 1px solid #EFECE6;
        border-left: 4px solid #cf0864;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.6rem;
    }
    .priority-card.cancelled { border-left-color: #9A9A9A; opacity: 0.72; }
    .priority-card.conflict  { border-left-color: #D9534F; }
    .priority-card.limited   { border-left-color: #E0A800; }
    .priority-card.registered{ border-left-color: #4A8F3C; }
    .priority-card.unclear   { border-left-color: #6C757D; }
    .priority-tag {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        padding: 0.12rem 0.55rem;
        border-radius: 999px;
        margin-right: 0.35rem;
        color: #FFFFFF !important;
    }
    .card-meta { font-size: 0.75rem; color: #5C4033 !important; }
    </style>
""", unsafe_allow_html=True)


# ======================================================================================
#  AI PRIORITY ASSISTANT — announcement triage engine
#
#  Turns the raw announcement stream (emails + class groups + society channels)
#  plus anything the student has stored into one ranked action plan.
#
#  Responsibility rules baked in deliberately:
#    • Never invents a date, time, venue or seat count that wasn't written down.
#      Missing detail is reported as missing, not filled in.
#    • Never deletes, merges or auto-resolves anything. Repeats are flagged as
#      repeats; conflicts are flagged as conflicts and left for the student.
#    • Never decides for the student — no auto-registering, no auto-dropping,
#      no "you should skip this". It ranks and labels only.
#    • Items with no date rank LAST but are never hidden, because unknown
#      urgency is not the same thing as low urgency.
# ======================================================================================

DAY_TOKENS = ["today", "tonight", "tomorrow", "monday", "tuesday", "wednesday",
              "thursday", "friday", "saturday", "sunday"]

URGENCY_RANK = {"today": 0, "tonight": 0, "tomorrow": 1,
                "monday": 2, "tuesday": 2, "wednesday": 2, "thursday": 2,
                "friday": 2, "saturday": 2, "sunday": 2}

CANCEL_WORDS = ["cancelled", "canceled", "postponed", "called off", "rescheduled to",
                "no longer happening", "stands cancelled", "withdrawn"]
LIMITED_WORDS = ["limited seats", "few seats", "seats left", "spots left", "few spots",
                 "closing very soon", "closing soon", "closes soon", "first come",
                 "almost full", "hurry", "last few"]
REGISTERED_WORDS = ["you are registered", "you're registered", "already registered",
                    "registered for this", "confirmed your", "rsvp confirmed", "enrolled"]
VAGUE_WORDS = ["tba", "to be announced", "to be decided", "tbd", "details soon",
               "venue and timing", "will share later", "shortly"]


def _find_day(text):
    low = text.lower()
    for d in DAY_TOKENS:
        if re.search(rf"\b{d}\b", low):
            return d
    return None


def _find_clock(text):
    m = re.search(r"\b\d{1,2}(:\d{2})?\s*(am|pm)\b", text.lower())
    if m:
        return m.group(0)
    if "midnight" in text.lower():
        return "midnight"
    if "noon" in text.lower():
        return "noon"
    return None


def _normalize(text):
    """Strip filler so an announcement repeated with a 'Reminder:' prefix still
    matches its original. Only used to FLAG repeats, never to remove them."""
    low = text.lower()
    low = re.sub(r"^(reminder|fwd|re|update|note)\s*[:\-]\s*", "", low)
    low = re.sub(r"[^a-z0-9 ]", " ", low)
    return re.sub(r"\s+", " ", low).strip()


def _missing_details(text):
    """Report what the announcement genuinely does not state. No guessing."""
    gaps = []
    if not _find_day(text):
        gaps.append("no date")
    if not _find_clock(text):
        gaps.append("no time")
    if any(v in text.lower() for v in VAGUE_WORDS):
        gaps.append("explicitly marked TBA")
    return gaps


def build_action_plan(stream, deadlines_store, assignments_store, channels):
    items = []

    # 1. Raw announcements from every feed
    for a in stream:
        items.append({"text": a["text"], "source": a["source"],
                      "channel": a["channel"], "kind": "Announcement"})

    # 2. Anything the student already saved themselves
    for ch in channels:
        for d in deadlines_store.get(ch, []):
            if str(d).strip():
                items.append({"text": str(d), "source": ch, "channel": ch, "kind": "Saved deadline"})
        for t in assignments_store.get(ch, []):
            if str(t).strip():
                items.append({"text": str(t), "source": ch, "channel": ch, "kind": "Saved task"})

    for it in items:
        low = it["text"].lower()
        it["tags"] = set()
        it["day"] = _find_day(it["text"])
        it["clock"] = _find_clock(it["text"])
        it["gaps"] = _missing_details(it["text"])
        it["norm"] = _normalize(it["text"])

        if any(w in low for w in CANCEL_WORDS):
            it["tags"].add("cancelled")
        if any(w in low for w in LIMITED_WORDS):
            it["tags"].add("limited")
        if any(w in low for w in REGISTERED_WORDS):
            it["tags"].add("registered")
        if it["gaps"]:
            it["tags"].add("unclear")

    # --- Repeated information: flagged side by side, never silently collapsed ---
    first_seen, repeats = {}, []
    for it in items:
        if it["norm"] in first_seen:
            it["tags"].add("repeat")
            repeats.append((first_seen[it["norm"]], it))
        else:
            first_seen[it["norm"]] = it

    # --- Conflicting commitments: two live, time-bound things on the same day ---
    by_day = {}
    for it in items:
        if it["day"] and "cancelled" not in it["tags"] and "repeat" not in it["tags"]:
            by_day.setdefault(it["day"], []).append(it)

    conflicts = []
    for day, group in by_day.items():
        timed = [g for g in group if g["clock"]]
        distinct = {g["norm"] for g in timed}
        if len(timed) > 1 and len(distinct) > 1:
            conflicts.append({"day": day, "items": timed})
            for g in timed:
                g["tags"].add("conflict")

    cancelled = [i for i in items if "cancelled" in i["tags"]]
    limited = [i for i in items if "limited" in i["tags"] and "cancelled" not in i["tags"]]
    registered = [i for i in items if "registered" in i["tags"] and "cancelled" not in i["tags"]]
    unclear = [i for i in items if "unclear" in i["tags"] and "cancelled" not in i["tags"]
               and "repeat" not in i["tags"]]

    # Action plan = everything still live and not a duplicate echo.
    plan = [i for i in items if "cancelled" not in i["tags"] and "repeat" not in i["tags"]]

    def rank(i):
        return (
            0 if "conflict" in i["tags"] else 1,
            0 if "limited" in i["tags"] else 1,
            URGENCY_RANK.get(i["day"], 9),   # 9 = no day stated → last, never dropped
            0 if i["clock"] else 1,
        )

    plan.sort(key=rank)

    return {"items": items, "plan": plan, "repeats": repeats, "conflicts": conflicts,
            "cancelled": cancelled, "limited": limited, "registered": registered,
            "unclear": unclear}


def _badges(it):
    out = ""
    if "conflict" in it["tags"]:
        out += '<span class="priority-tag" style="background:#D9534F;">CLASHES</span>'
    if "limited" in it["tags"]:
        out += '<span class="priority-tag" style="background:#E0A800;">LIMITED SEATS</span>'
    if "registered" in it["tags"]:
        out += '<span class="priority-tag" style="background:#4A8F3C;">ALREADY REGISTERED</span>'
    if "repeat" in it["tags"]:
        out += '<span class="priority-tag" style="background:#6C757D;">REPEAT</span>'
    if it["gaps"]:
        out += f'<span class="priority-tag" style="background:#6C757D;">{", ".join(it["gaps"]).upper()}</span>'
    return out


def _card(it, css=""):
    when = " · ".join(x for x in [it["day"].title() if it["day"] else None, it["clock"]] if x)
    when = when or "timing not stated"
    st.markdown(
        f"""<div class="priority-card {css}">
        {_badges(it)}<br>{it['text']}<br>
        <span class="card-meta">{it['kind']} · {it['source']} · {when}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def render_priority_assistant():
    st.markdown("### 🧠 AI Priority Assistant — Your Action Plan")
    st.caption(
        "Reads every feed at once — emails, class groups and society channels — and turns them into "
        "one ranked plan. It flags clashes, cancellations, limited seats, repeats and missing details, "
        "but it does not choose for you, drop anything, or fill in a date that was never written down."
    )

    r = build_action_plan(
        st.session_state.announcement_stream,
        st.session_state.deadlines_store,
        st.session_state.assignments_store,
        CHANNELS,
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("⚠️ Clashing Days", len(r["conflicts"]))
    c2.metric("🚫 Cancelled", len(r["cancelled"]))
    c3.metric("⏳ Limited Seats", len(r["limited"]))
    c4.metric("✅ Registered", len(r["registered"]))
    c5.metric("❓ Missing Details", len(r["unclear"]))

    t1, t2, t3, t4, t5, t6 = st.tabs(
        ["🔥 Action Plan", "⚠️ Clashes", "🚫 Cancelled", "⏳ Limited Seats",
         "✅ Registered", "❓ Needs Checking"]
    )

    with t1:
        st.caption(
            "Order: clashes first, then limited-seat chances, then how soon the stated time is. "
            "Anything with no date sits at the bottom — unknown urgency, not low urgency. "
            "Cancelled items and repeat copies are kept out of this list but not deleted; "
            "they're in their own tabs."
        )
        if not r["plan"]:
            st.info("Nothing outstanding.")
        for it in r["plan"]:
            css = "conflict" if "conflict" in it["tags"] else \
                  "limited" if "limited" in it["tags"] else \
                  "registered" if "registered" in it["tags"] else \
                  "unclear" if it["gaps"] else ""
            _card(it, css)

    with t2:
        st.caption(
            "Two or more time-bound commitments landing on the same day. The assistant will not pick "
            "one for you — attendance rules, how much each matters and whether they actually overlap "
            "are your call."
        )
        if not r["conflicts"]:
            st.info("No same-day clashes found.")
        for c in r["conflicts"]:
            st.markdown(f"**{c['day'].title()} — {len(c['items'])} commitments**")
            for i in c["items"]:
                st.markdown(f"- `{i['clock']}` {i['text']} — *{i['source']}*")
            st.markdown("---")

    with t3:
        st.caption("Pulled out of your plan so you don't prepare for something that isn't happening. "
                   "Kept visible in case the cancellation itself gets reversed.")
        if not r["cancelled"]:
            st.info("Nothing cancelled.")
        for it in r["cancelled"]:
            st.markdown(
                f"""<div class="priority-card cancelled">
                <s>{it['text']}</s><br>
                <span class="card-meta">{it['kind']} · {it['source']}</span>
                </div>""", unsafe_allow_html=True)

    with t4:
        st.caption("Opportunities where the announcement itself said seats are limited or closing. "
                   "No seat count is shown unless the message gave one.")
        if not r["limited"]:
            st.info("No limited-seat opportunities flagged.")
        for it in r["limited"]:
            _card(it, "limited")

    with t5:
        st.caption("Things you're already signed up for — listed for awareness, not as pending work.")
        if not r["registered"]:
            st.info("Nothing marked as registered.")
        for it in r["registered"]:
            _card(it, "registered")

    with t6:
        st.caption(
            "These arrived without a date, a time, or with details explicitly marked TBA. "
            "The assistant is telling you exactly what's missing instead of assuming it — "
            "go back to the original message or ask the organiser."
        )
        if not r["unclear"]:
            st.info("Everything currently has a date and time attached.")
        for it in r["unclear"]:
            _card(it, "unclear")

    if r["repeats"]:
        with st.expander(f"🔁 {len(r['repeats'])} repeated announcement(s) detected"):
            st.caption("Same notice arriving twice, so you don't treat it as two separate commitments. "
                       "Both copies are kept — nothing was deleted.")
            for original, dup in r["repeats"]:
                st.markdown(f"- **{original['text'][:70]}…**")
                st.markdown(f"  ↳ first from *{original['source']}*, repeated by *{dup['source']}*")

    with st.expander("ℹ️ How this assistant decides (and what it refuses to decide)"):
        st.markdown(
            "- **Reads, never rewrites.** Dates, times and venues are shown only if the message said them.\n"
            "- **Missing info stays missing.** A TBA event is labelled TBA, not given a guessed slot.\n"
            "- **Repeats are flagged, not merged.** You see both copies and who sent each.\n"
            "- **Clashes are surfaced, not resolved.** It won't tell you which commitment to drop.\n"
            "- **No silent deletion.** Cancelled items move to their own tab and stay readable.\n"
            "- **Undated ≠ unimportant.** Those items sit last in the plan but are never hidden."
        )


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

# --- 4. AI PRIORITY ASSISTANT (full width, reads every channel at once) ---
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

    audio_input = st.audio_input("Record Your Voice Command")
    voice_command = st.text_input("Or type your reminder directly here:", placeholder="Type a reminder...")

    if st.button("⚡ Save Directly to Calendar", use_container_width=True):
        if voice_command:
            clean_cmd = voice_command.strip()
            st.session_state.deadlines_store[selected_stream].append(clean_cmd)
            # No date parsing guesswork here — if the student didn't say when,
            # the assistant above will flag it as "no date" rather than inventing one.
            st.success("Successfully saved to your Calendar list below!")
            st.rerun()
        else:
            st.warning("Please type or say something first.")

    st.markdown("---")
    st.markdown("### 📥 Paste a New Announcement")
    st.caption("Drop in an email or group message and the assistant will triage it above.")
    new_ann = st.text_area("Announcement text:", placeholder="e.g. Seminar cancelled / Workshop Friday 4 PM, limited seats", height=90)
    if st.button("🔎 Add to Triage Feed", use_container_width=True):
        if new_ann.strip():
            st.session_state.announcement_stream.append(
                {"source": selected_stream, "channel": selected_stream, "text": new_ann.strip()}
            )
            st.success("Added — see the updated action plan above.")
            st.rerun()
        else:
            st.warning("Paste an announcement first.")

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

    st.markdown("<br>", unsafe_allow_html=True)

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

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📨 Raw Announcement Feed (this channel)")
    st.caption("Unfiltered messages the assistant is reading from — shown so you can always check the source.")
    raw = [a["text"] for a in st.session_state.announcement_stream if a["channel"] == selected_stream]
    if raw:
        st.dataframe(pd.DataFrame({"Incoming Messages": raw}), use_container_width=True, hide_index=True)
    else:
        st.info("No raw announcements captured for this channel yet.")

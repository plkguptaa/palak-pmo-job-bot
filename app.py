# app.py - Palak AI Job Assistant & PMO Career Navigator (Enterprise SaaS Edition)
import streamlit as st
import pandas as pd
import os
from pypdf import PdfReader
from docx import Document

# 1. Page Configuration
st.set_page_config(
    page_title="AI Job Assistant - PMO & Project Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern Enterprise Tokyo Night SaaS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0f1117;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #161821;
        border-right: 1px solid #2d3142;
    }
    h1, h2, h3 {
        color: #f7768e !important;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    p, label {
        color: #94a3b8 !important;
    }
    
    /* Sleek KPI Metrics Cards */
    [data-testid="metric-container"] {
        background-color: #1a1b26;
        border: 1px solid #2d3142;
        padding: 14px 18px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    [data-testid="metric-container"] label {
        color: #7aa2f7 !important;
        font-weight: 600;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #c0caf5 !important;
        font-size: 1.6rem !important;
    }

    /* Sleek Apply Button */
    .stLinkButton>a {
        border-radius: 8px;
        font-weight: 600 !important;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #7aa2f7 0%, #bb9af7 100%) !important;
        color: #0f1117 !important;
        border: none !important;
        text-align: center;
        box-shadow: 0 2px 4px rgba(122, 162, 247, 0.2);
        transition: all 0.2s ease;
    }
    .stLinkButton>a:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    /* Minimalist Action Button */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 500 !important;
        padding: 0.4rem 0.8rem;
        background-color: #1a1b26 !important;
        color: #c0caf5 !important;
        border: 1px solid #3b4261 !important;
    }
    div.stButton > button:hover {
        background-color: #24283b !important;
        border-color: #7aa2f7 !important;
    }

    /* Bordered Container Card Styling */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #161821;
        border: 1px solid #2d3142;
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #7aa2f7;
        box-shadow: 0 10px 20px -3px rgba(122, 162, 247, 0.1);
    }
    
    /* Sidebar Input Control Styling */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #1a1b26 !important;
        border: 1px solid #2d3142;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

PMO_SKILL_TAXONOMY = [
    "kpi", "stakeholder management", "excel", "pmo governance",
    "jira", "agile", "scrum", "risk management", "budgeting",
    "vendor management", "sla", "reporting", "power bi", "confluence",
]

STATUS_STYLES = {
    "Not Applied": ("#565f89", "⏳"),
    "Saved":       ("#7aa2f7", "📌"),
    "Applied":     ("#e0af68", "📨"),
    "Interview":   ("#9ece6a", "🎯"),
    "Offer":       ("#f7768e", "🏆"),
}

def get_skill_match(resume_text: str, taxonomy: list) -> tuple:
    matched = [skill for skill in taxonomy if skill in resume_text]
    missing = [skill for skill in taxonomy if skill not in matched]
    return matched[:4], missing[:2]

def extract_resume_text(uploaded_file):
    text = ""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_extension == "pdf":
                reader = PdfReader(uploaded_file)
                if reader.is_encrypted:
                    st.sidebar.error("This PDF is password-protected. Please upload an unlocked file.")
                    return ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
            elif file_extension in ["docx", "doc"]:
                doc = Document(uploaded_file)
                for para in doc.paragraphs:
                    text += para.text + " "
            else:
                st.sidebar.error("Unsupported file type. Please upload a PDF or DOCX.")
                return ""
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
            return ""
    return text.lower()

# --- HEADER BRANDING ---
st.title("⚡ AI Job Assistant & Career Navigator")
st.markdown("##### **Enterprise PMO • Project Management • Operations Command Center**")

# Load jobs data safely directly
if os.path.exists("jobs.csv"):
    try:
        raw_df = pd.read_csv("jobs.csv", on_bad_lines='skip')
        raw_df.columns = raw_df.columns.str.strip().str.lower()
        
        df = pd.DataFrame()
        df["Title"] = raw_df["job_profile"] if "job_profile" in raw_df.columns else (raw_df["title"] if "title" in raw_df.columns else "N/A")
        df["Company"] = raw_df["company"] if "company" in raw_df.columns else "N/A"
        df["Location"] = raw_df["location"] if "location" in raw_df.columns else ("city" if "city" in raw_df.columns else "N/A")
        df["Platform"] = raw_df["source"] if "source" in raw_df.columns else ("platform" if "platform" in raw_df.columns else "LinkedIn")
        df["Track"] = raw_df["track"] if "track" in raw_df.columns else "PMO"
        df["Job_Age"] = raw_df["posted_date"] if "posted_date" in raw_df.columns else "2 days ago"
        df["Link"] = raw_df["apply_link"] if "apply_link" in raw_df.columns else ("url" if "url" in raw_df.columns else "#")
        df["Description"] = raw_df["description"] if "description" in raw_df.columns else ""

        if "ATS_Status" not in df.columns:
            df["ATS_Status"] = "Not Applied"

        if "Saved" not in df.columns:
            df["Saved"] = False

        # --- SIDEBAR CONTROLS ---
        st.sidebar.markdown("### 👤 Candidate Profile")
        st.sidebar.info("Target Role: **PMO & Project Manager**\nStatus: Actively Interviewing")
        st.sidebar.divider()

        st.sidebar.header("🔍 Search & Filters")
        search_query = st.sidebar.text_input("Search Title / Company", key="search_query")

        tracks = ["All"] + sorted(df["Track"].dropna().unique().tolist()) if "Track" in df.columns else ["All"]
        selected_track = st.sidebar.selectbox("Career Track", tracks, key="track_sel")

        st.sidebar.markdown("### 🎯 PMO Focus Roles")
        quick_chip = st.sidebar.radio(
            "Quick Filter:",
            ["All", "PMO", "Project Coordinator", "Associate PM", "Project Analyst", "Program Coordinator"],
            label_visibility="collapsed",
            key="quick_chip_sel"
        )

        platforms = ["All"] + sorted(df["Platform"].dropna().unique().tolist()) if "Platform" in df.columns else ["All"]
        selected_platform = st.sidebar.selectbox("Platform Source", platforms, key="plat_sel")

        locations = ["All", "Bangalore", "Hyderabad", "Pune", "Noida", "Mumbai", "Chennai", "Delhi NCR", "India", "Remote", "Hybrid", "WFH"]
        selected_location = st.sidebar.selectbox("Work Mode / Location", locations, key="loc_sel")

        st.sidebar.divider()
        st.sidebar.header("📁 AI Resume Uploader")
        uploaded_resume = st.sidebar.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"], key="resume_up")

        resume_text = ""
        if uploaded_resume is not None:
            resume_text = extract_resume_text(uploaded_resume)
            if resume_text.strip():
                st.sidebar.success(f"✨ Parsed: {uploaded_resume.name}")

        st.sidebar.divider()
        with st.sidebar.expander("⚙️ Admin Settings"):
            admin_pass = st.text_input("Password", type="password", key="admin_pwd_input")
        
        is_admin = bool(admin_pass) and (admin_pass == st.secrets.get("ADMIN_PASSWORD", "palak2026"))

        # --- FILTERING LOGIC ---
        filtered_df = df.copy()

        if search_query:
            q = search_query.lower()
            filtered_df = filtered_df[
                filtered_df["Title"].str.lower().str.contains(q, na=False)
                | filtered_df["Company"].str.lower().str.contains(q, na=False)
            ]

        if selected_track != "All":
            filtered_df = filtered_df[filtered_df["Track"] == selected_track]

        if quick_chip != "All":
            filtered_df = filtered_df[
                filtered_df["Title"].str.lower().str.contains(quick_chip.lower(), na=False)
            ]

        if selected_platform != "All":
            filtered_df = filtered_df[filtered_df["Platform"] == selected_platform]

        if selected_location != "All":
            filtered_df = filtered_df[
                filtered_df["Location"].str.lower().str.contains(selected_location.lower(), na=False)
            ]

        # --- RESUME MATCH SCORING ---
        if resume_text.strip() and not filtered_df.empty:
            resume_words = set(w.strip() for w in resume_text.split() if len(w) >= 3)

            def calc_match(title):
                title_words = set(title.lower().split())
                matches = resume_words.intersection(title_words)
                return min(98, max(35, len(matches) * 35 + 35))

            filtered_df["Match_Score"] = filtered_df["Title"].apply(calc_match)
            filtered_df = filtered_df.sort_values(by="Match_Score", ascending=False)

        # --- TOP METRICS DASHBOARD ---
        saved_count = int((df["Saved"] == True).sum())
        applied_count = int((df["ATS_Status"] == "Applied").sum())
        interview_count = int((df["ATS_Status"] == "Interview").sum())
        avg_match_val = f"{int(filtered_df['Match_Score'].mean())}%" if resume_text.strip() and not filtered_df.empty and 'Match_Score' in filtered_df.columns else "N/A"

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📊 Filtered Openings", len(filtered_df))
        m2.metric("🎯 Resume Match Avg", avg_match_val)
        m3.metric("📌 Saved Positions", saved_count)
        m4.metric("🎯 Active Interviews", interview_count)

        st.divider()

        # --- SECTION CONTROLS ---
        col_head1, col_head2 = st.columns([3, 1])
        with col_head1:
            st.subheader(f"Active Job Feed ({len(filtered_df)} matches)")
        with col_head2:
            csv_export = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV Report", data=csv_export, file_name="pmo_tracked_jobs.csv", mime="text/csv")

        # --- EMPTY STATE ---
        if filtered_df.empty:
            st.warning("No positions match your current filter criteria. Try resetting filters.")
            if st.button("🔄 Reset Filters", key="clear_filters_btn"):
                st.rerun()

        # --- DISPLAY JOBS ---
        for index, row in filtered_df.iterrows():
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])

                with col1:
                    match_score_val = row.get("Match_Score", None)
                    match_badge = (
                        f" 🔥 **[Match: {match_score_val}%]**"
                        if resume_text.strip() and match_score_val is not None
                        else ""
                    )
                    st.markdown(f"### {row['Title']}{match_badge}")
                    st.write(f"🏢 **Company:** {row['Company']} | 📍 **Location:** {row['Location']}")
                    st.markdown(f"🕒 **Posted:** {row.get('Job_Age', '2 days ago')}")

                    if resume_text.strip():
                        matched, missing = get_skill_match(resume_text, PMO_SKILL_TAXONOMY)
                        matched_display = ", ".join(f"`{s.title()}`" for s in matched) or "None detected"
                        missing_display = ", ".join(f"`{s.title()}`" for s in missing) or "None"
                        st.markdown(f"✔️ **Matched Skills:** {matched_display}")
                        st.markdown(f"✖️ **Skill Gaps:** {missing_display}")

                with col2:
                    platform_name = row['Platform'] if pd.notna(row['Platform']) else "LinkedIn"
                    st.markdown(f"📌 **Platform:** `{platform_name}`")
                    st.markdown(f"📂 **Track:** {row['Track']}")

                    with st.expander("✨ AI Cover Pitch"):
                        pitch_text = f"Hello hiring team, I am an experienced PMO and project professional interested in the {row['Title']} role at {row['Company']}. With solid background in project governance, agile delivery, and stakeholder coordination, I am ready to add immediate value."
                        st.text_area("Draft Pitch:", pitch_text, height=80, key=f"pitch_{index}")

                with col3:
                    job_link = row['Link'] if pd.notna(row['Link']) and str(row['Link']).startswith("http") else "#"
                    company_name_clean = str(row['Company']).strip().replace(" ", "+")
                    company_search_url = f"https://www.google.com/search?q={company_name_clean}+company+profile+linkedin"

                    st.link_button("🚀 Apply Now", job_link, type="primary", use_container_width=True)
                    st.markdown(f"[🏢 Company Profile]({company_search_url})", unsafe_allow_html=True)

                with col4:
                    is_saved = bool(row.get("Saved", False))
                    save_label = "❤️ Saved" if is_saved else "🤍 Save"

                    if st.button(save_label, key=f"save_btn_{index}"):
                        df.at[index, "Saved"] = not is_saved
                        df.to_csv("jobs.csv", index=False)
                        st.rerun()

                    current_status = row.get("ATS_Status", "Not Applied")
                    status_options = ["Not Applied", "Saved", "Applied", "Interview", "Offer"]

                    if is_admin:
                        new_status = st.selectbox(
                            "Status",
                            status_options,
                            index=status_options.index(current_status) if current_status in status_options else 0,
                            key=f"status_{index}",
                        )
                        if new_status != current_status:
                            df.at[index, "ATS_Status"] = new_status
                            df.to_csv("jobs.csv", index=False)
                            st.rerun()
                    else:
                        color, icon = STATUS_STYLES.get(current_status, ("#565f89", "⏳"))
                        st.markdown(
                            f"""<div style="margin-top: 10px;"><span style="background:{color}22; color:{color}; padding:5px 10px; border-radius:999px; font-size:0.75rem; font-weight:600; border: 1px solid {color}44;">{icon} {current_status}</span></div>""",
                            unsafe_allow_html=True,
                        )

    except Exception as e:
        st.error(f"Error loading jobs data: {e}")
else:
    st.warning("`jobs.csv` not found in root directory.")
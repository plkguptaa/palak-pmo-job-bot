# app.py - Palak AI Job Assistant & PMO Career Navigator (Refined Minimalist UI)
import streamlit as st
import pandas as pd
import os
from pypdf import PdfReader
from docx import Document
import random

# 1. Page Configuration
st.set_page_config(
    page_title="Palak AI Job Assistant - PMO & Project Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Tokyo Night Refined Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1b26;
        color: #c0caf5;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #16161e;
        border-right: 1px solid #24283b;
    }
    h1, h2, h3 {
        color: #bb9af7 !important;
        font-weight: 700;
    }
    p, label {
        color: #a9b1d6 !important;
    }
    
    /* Sleek Apply Button */
    .stLinkButton>a {
        border-radius: 6px;
        font-weight: 600 !important;
        padding: 0.4rem 0.8rem;
        background-color: #24283b !important;
        color: #7aa2f7 !important;
        border: 1px solid #7aa2f7 !important;
        text-align: center;
        transition: all 0.2s ease;
    }
    .stLinkButton>a:hover {
        background-color: #7aa2f7 !important;
        color: #1a1b26 !important;
    }

    /* Minimalist Save Job Button */
    div.stButton > button {
        border-radius: 6px;
        font-weight: 500 !important;
        padding: 0.4rem 0.8rem;
        background-color: #16161e !important;
        color: #a9b1d6 !important;
        border: 1px solid #414868 !important;
    }
    div.stButton > button:hover {
        background-color: #24283b !important;
        color: #c0caf5 !important;
        border-color: #bb9af7 !important;
    }

    /* Bordered Container Card Styling */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #16161e;
        border: 1px solid #24283b;
        border-radius: 10px;
        padding: 4px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: border-color 0.15s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #7aa2f7;
    }
    /* Sidebar Input Control Styling */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] {
        min-height: 40px;
        border: 1px solid #24283b;
        border-radius: 6px;
    }
    [data-testid="stSidebar"] input:focus, [data-testid="stSidebar"] [data-baseweb="select"]:focus-within {
        border-color: #bb9af7;
        box-shadow: 0 0 0 2px rgba(187, 154, 247, 0.2);
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

    if uploaded_file is not None and not text.strip():
        st.sidebar.warning("No extractable text found — scanned resume. Match scoring unavailable.")
    return text.lower()

# Header branding
st.title("🚀 Palak AI Job Assistant")
st.markdown("### **PMO • Project Management • Operations Roles | Career Navigator**")
st.caption("🟢 **Multi-Platform Aggregator** | PMO & Agile Focused")

# Load jobs data safely
if os.path.exists("jobs.csv"):
    try:
        df = pd.read_csv("jobs.csv", on_bad_lines='skip')
        df.columns = df.columns.str.strip()

        required_cols = ["Title", "Company", "Location", "Platform", "Track", "Link"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = "N/A"

        text_cols = ["Title", "Company", "Location", "Platform", "Track"]
        df[text_cols] = df[text_cols].fillna("N/A")

        if "ATS_Status" not in df.columns:
            df["ATS_Status"] = "Not Applied"

        if "Saved" not in df.columns:
            df["Saved"] = False
        else:
            df["Saved"] = (
                df["Saved"]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({"true": True, "1": True, "false": False, "0": False})
                .fillna(False)
            )

        if "Job_Age" not in df.columns:
            ages = ["2 days ago", "6 hours ago", "1 week ago", "3 days ago", "Just now", "4 days ago"]
            df["Job_Age"] = [random.choice(ages) for _ in range(len(df))]

        # --- SIDEBAR CONTROLS ---
        st.sidebar.header("🔍 Search & Filters")
        search_query = st.sidebar.text_input("Search Title / Company", key="search_query")

        tracks = ["All"] + sorted(df["Track"].dropna().unique().tolist())
        selected_track = st.sidebar.selectbox("Career Track", tracks, key="track_sel")

        st.sidebar.markdown("### 🎯 PMO Focus Roles")
        quick_chip = st.sidebar.radio(
            "Quick Filter:",
            ["All", "PMO", "Project Coordinator", "Associate PM", "Project Analyst", "Program Coordinator"],
            label_visibility="collapsed",
            key="quick_chip_sel"
        )

        platforms = ["All"] + sorted(df["Platform"].dropna().unique().tolist())
        selected_platform = st.sidebar.selectbox("Platform Source", platforms, key="plat_sel")

        locations = ["All", "Bangalore", "Hyderabad", "Pune", "Noida", "Remote", "Hybrid", "WFH"]
        selected_location = st.sidebar.selectbox("Work Mode / Location", locations, key="loc_sel")

        st.sidebar.divider()
        st.sidebar.header("📁 AI Resume Uploader")
        uploaded_resume = st.sidebar.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"], key="resume_up")

        resume_text = ""
        if uploaded_resume is not None:
            resume_text = extract_resume_text(uploaded_resume)
            if resume_text.strip():
                st.sidebar.success(f"✨ Analyzed: {uploaded_resume.name}")

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
                score = min(96, max(30, len(matches) * 30 + 30))
                return score

            filtered_df["Match_Score"] = filtered_df["Title"].apply(calc_match)
            filtered_df = filtered_df.sort_values(by="Match_Score", ascending=False)

            avg_score = int(filtered_df["Match_Score"].mean())
            st.success(
                f"🎯 **Found {len(filtered_df)} PMO Jobs For You!** | Average Match: **{avg_score}%** | "
                f"Top Match: **{filtered_df.iloc[0]['Title']} ({filtered_df.iloc[0]['Match_Score']}% Match)**"
            )
        elif resume_text.strip() and filtered_df.empty:
            st.info("No jobs match your current filters — widen your search to see resume match scores.")

        # --- SAVED JOBS COUNTER ---
        saved_count = int((df["Saved"] == True).sum())

        col_head1, col_head2 = st.columns([3, 1])
        with col_head1:
            st.subheader(f"Available Openings ({len(filtered_df)} jobs found) | 📌 Saved Jobs: {saved_count}")
        with col_head2:
            csv_export = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV", data=csv_export, file_name="palak_pmo_tracked_jobs.csv", mime="text/csv")

        # --- EMPTY STATE ---
        if filtered_df.empty:
            st.warning("No jobs match your current filters. Try widening your search or clearing filters.")
            if st.button("🔄 Clear all filters", key="clear_filters_btn"):
                st.session_state["search_query"] = ""
                st.rerun()

        # --- DISPLAY JOBS ---
        for index, row in filtered_df.iterrows():
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])

                with col1:
                    match_score_val = row.get("Match_Score", None)
                    match_badge = (
                        f" 🔥 **[Resume Match: {match_score_val}%]**"
                        if resume_text.strip() and match_score_val is not None
                        else ""
                    )
                    st.markdown(f"### {row['Title']}{match_badge}")
                    st.write(f"🏢 **Company:** {row['Company']} | 📍 **Location:** {row['Location']}")
                    st.markdown(f"🕒 **Posted:** {row.get('Job_Age', '2 days ago')}")

                    if resume_text.strip():
                        matched, missing = get_skill_match(resume_text, PMO_SKILL_TAXONOMY)
                        matched_display = ", ".join(f"`{s.title()}`" for s in matched) or "None found yet"
                        missing_display = ", ".join(f"`{s.title()}`" for s in missing) or "None"
                        st.markdown(f"✔️ **Skills Matched:** {matched_display}")
                        st.markdown(f"✖️ **Missing:** {missing_display}")

                with col2:
                    platform_name = row['Platform'] if pd.notna(row['Platform']) else "LinkedIn"
                    st.markdown(f"📌 **Source:** `{platform_name}`")
                    st.markdown(f"📂 **Track:** {row['Track']}")

                    with st.expander("✨ AI Quick Pitch"):
                        pitch_text = f"Hi hiring team, I am an experienced PMO professional deeply interested in the {row['Title']} role at {row['Company']}. With strong expertise in project governance, stakeholder management, and agile tracking, I am ready to add value from day one."
                        st.text_area("Copy Cover Letter Pitch:", pitch_text, height=90, key=f"pitch_{index}")

                with col3:
                    job_link = row['Link'] if pd.notna(row['Link']) and str(row['Link']).startswith("http") else "#"
                    company_name_clean = str(row['Company']).strip().replace(" ", "+")
                    company_search_url = f"https://www.google.com/search?q={company_name_clean}+company+profile+linkedin"

                    st.link_button("🚀 Apply Now", job_link, type="primary", use_container_width=True)
                    st.markdown(f"[🏢 Company Profile]({company_search_url})", unsafe_allow_html=True)

                with col4:
                    is_saved = bool(row.get("Saved", False))
                    save_label = "❤️ Saved" if is_saved else "🤍 Save Job"

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
                            f"""<div style="margin-top: 10px;"><span style="background:{color}22; color:{color}; padding:6px 12px; border-radius:999px; font-size:0.8rem; font-weight:600; border: 1px solid {color}44;">{icon} {current_status}</span></div>""",
                            unsafe_allow_html=True,
                        )

    except Exception as e:
        st.error(f"Error loading jobs data: {e}")
else:
    st.warning("`jobs.csv` not found. Please check your data source.")
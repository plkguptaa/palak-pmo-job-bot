# app.py - PDF/Word Resume Matcher, Advanced Filters & Tokyo Night Theme
import streamlit as st
import pandas as pd
import os
import io
from pypdf import PdfReader
from docx import Document

# 1. Page Configuration MUST be the very first Streamlit command
st.set_page_config(
    page_title="Palak AI - Global Strategic Job Search Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Aesthetic Styling (Tokyo Night Vibe)
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
    p {
        color: #a9b1d6;
    }
    .stButton>button {
        background: linear-gradient(135deg, #7aa2f7 0%, #bb9af7 100%);
        color: #1a1b26;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 12px rgba(122, 162, 247, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #89b4fa, #cba6f7);
        color: #000000;
    }
    div.stContainer {
        background-color: #16161e;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #24283b;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to extract text from uploaded Resume (PDF or DOCX)
def extract_resume_text(uploaded_file):
    text = ""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_extension == "pdf":
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
            elif file_extension in ["docx", "doc"]:
                doc = Document(uploaded_file)
                for para in doc.paragraphs:
                    text += para.text + " "
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
    return text.lower()

# App Header
st.title("🚀 Palak AI: Global Strategic Job Search Portal")
st.markdown("Your multi-platform intelligent job hunting command center with Resume Upload, Advanced Filters, and Live Tracker.")

# Load jobs data safely
if os.path.exists("jobs.csv"):
    try:
        df = pd.read_csv("jobs.csv", on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        
        required_cols = ["Title", "Company", "Location", "Platform", "Track", "Link"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = "N/A"

        if "Applied" not in df.columns:
            df["Applied"] = False

        # --- SIDEBAR: ADVANCED FILTERS & RESUME UPLOADER ---
        st.sidebar.header("🔍 Advanced Filters")
        search_query = st.sidebar.text_input("Search Title / Company")
        selected_track = st.sidebar.selectbox("Select Career Track", ["All"] + list(df["Track"].unique()))
        selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + list(df["Platform"].unique()))
        show_applied_only = st.sidebar.checkbox("Show Applied Only")
        
        st.sidebar.divider()
        st.sidebar.header("📁 AI Resume Matcher")
        uploaded_resume = st.sidebar.file_uploader("Upload Resume (PDF or Word)", type=["pdf", "docx"])
        
        resume_text = ""
        if uploaded_resume is not None:
            resume_text = extract_resume_text(uploaded_resume)
            st.sidebar.success(f"✅ Uploaded: {uploaded_resume.name}")

        st.sidebar.divider()
        st.sidebar.header("🔐 Admin Access")
        admin_pass = st.sidebar.text_input("Admin Password", type="password")
        is_admin = (admin_pass == "palak2026")
        if is_admin:
            st.sidebar.success("🔓 Admin Mode Active")
        else:
            st.sidebar.info("👁️ Public View (Read-Only)")

        # --- DATA FILTERING & MATCHING ---
        filtered_df = df.copy()
        
        if search_query:
            query = search_query.lower()
            filtered_df = filtered_df[filtered_df["Title"].str.lower().str.contains(query) | filtered_df["Company"].str.lower().str.contains(query)]
            
        if selected_track != "All":
            filtered_df = filtered_df[filtered_df["Track"] == selected_track]
        if selected_platform != "All":
            filtered_df = filtered_df[filtered_df["Platform"] == selected_platform]
        if show_applied_only:
            filtered_df = filtered_df[filtered_df["Applied"] == True]

        # Calculate AI Match Score based on uploaded resume content
        if resume_text.strip():
            resume_words = set(w.strip() for w in resume_text.split() if len(w) > 3)
            def calc_score(title):
                if not resume_words:
                    return 50
                title_words = set(title.lower().split())
                matches = resume_words.intersection(title_words)
                # Dynamic scoring based on keyword overlap
                score = min(96, max(50, len(matches) * 35 + 55))
                return score
            filtered_df["Match_Score"] = filtered_df["Title"].apply(calc_score)
            filtered_df = filtered_df.sort_values(by="Match_Score", ascending=False)
            st.sidebar.info("✨ Jobs sorted by Resume Match Score!")

        st.subheader(f"Available Openings ({len(filtered_df)} jobs found)")

        # Display Jobs
        for index, row in filtered_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    match_badge = f" 🔥 **[{row.get('Match_Score', 0)}% Match]**" if "Match_Score" in row else ""
                    st.markdown(f"### {row['Title']}{match_badge}")
                    st.write(f"🏢 **Company:** {row['Company']} | 📍 **Location:** {row['Location']}")
                with col2:
                    st.markdown(f"🌐 **Platform:** `{row['Platform']}`")
                    st.markdown(f"📂 **Track:** {row['Track']}")
                with col3:
                    if pd.notna(row['Link']) and str(row['Link']).startswith("http"):
                        st.markdown(f"[Apply Link]({row['Link']})", unsafe_allow_html=True)
                    else:
                        st.markdown("Link N/A")
                with col4:
                    current_applied = bool(row.get("Applied", False))
                    if is_admin:
                        is_applied = st.checkbox("Applied", value=current_applied, key=f"apply_{index}")
                        if is_applied != current_applied:
                            df.at[index, "Applied"] = is_applied
                            df.to_csv("jobs.csv", index=False)
                    else:
                        status_text = "✅ Applied" if current_applied else "⏳ Not Applied"
                        st.markdown(f"**Status:** `{status_text}`")
                st.divider()

    except Exception as e:
        st.error(f"Error loading jobs data: {e}")
else:
    st.warning("`jobs.csv` not found. Please run `main.py` to generate job listings.")

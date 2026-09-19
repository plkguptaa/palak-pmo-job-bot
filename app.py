# app.py - Gen-Z Aesthetic / Tokyo Night Theme
import streamlit as st
import pandas as pd
import os

# 1. Page Configuration MUST be the very first Streamlit command
st.set_page_config(
    page_title="Palak AI - Global Strategic Job Search Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Aesthetic Styling (Tokyo Night / Minimalist Tech Vibe)
st.markdown("""
    <style>
    /* Main Background & Soft Text */
    .stApp {
        background-color: #1a1b26;
        color: #c0caf5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #16161e;
        border-right: 1px solid #24283b;
    }
    
    /* Headers - Soft Lavender/Purple Accent */
    h1, h2, h3 {
        color: #bb9af7 !important;
        font-weight: 700;
    }
    
    /* Subtitles / Markdown text */
    p {
        color: #a9b1d6;
    }
    
    /* Gradient Buttons (Indigo to Soft Purple) */
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
    
    /* Job Card Containers - Sleek Dark Cards with Soft Borders */
    div.stContainer {
        background-color: #16161e;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #24283b;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    div.stContainer:hover {
        border-color: #7aa2f7;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🚀 Palak AI: Global Strategic Job Search Portal")
st.markdown("Your multi-platform intelligent job hunting command center across LinkedIn, Naukri, IIMJobs, Instahyre, and Foundit with live Application Tracker.")

# Load jobs data safely
if os.path.exists("jobs.csv"):
    try:
        df = pd.read_csv("jobs.csv", on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        
        # Ensure required columns exist
        required_cols = ["Title", "Company", "Location", "Platform", "Track", "Link"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = "N/A"

        # Add Applied status column if not present
        if "Applied" not in df.columns:
            df["Applied"] = False

        # Sidebar Filters
        st.sidebar.header("🔍 Filter Jobs")
        selected_track = st.sidebar.selectbox("Select Career Track", ["All"] + list(df["Track"].unique()))
        selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + list(df["Platform"].unique()))
        show_applied_only = st.sidebar.checkbox("Show Applied Only")
        
        # Apply filters
        filtered_df = df.copy()
        if selected_track != "All":
            filtered_df = filtered_df[filtered_df["Track"] == selected_track]
        if selected_platform != "All":
            filtered_df = filtered_df[filtered_df["Platform"] == selected_platform]
        if show_applied_only:
            filtered_df = filtered_df[filtered_df["Applied"] == True]

        st.subheader(f"Available Openings ({len(filtered_df)} jobs found)")

        # Display Data with interactive Applied checkboxes
        for index, row in filtered_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.markdown(f"### {row['Title']}")
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
                    # Applied toggle button
                    is_applied = st.checkbox("Applied", value=bool(row.get("Applied", False)), key=f"apply_{index}")
                    if is_applied != row.get("Applied", False):
                        df.at[index, "Applied"] = is_applied
                        df.to_csv("jobs.csv", index=False)
                st.divider()

    except Exception as e:
        st.error(f"Error loading jobs data: {e}")
else:
    st.warning("`jobs.csv` not found. Please run `main.py` to generate job listings.")

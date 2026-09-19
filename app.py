# app.py - Robust Streamlit Dashboard
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Palak AI - PMO & Presales Job Tracker", layout="wide")

st.title("🚀 Palak AI: PMO & Presales Job Tracker")
st.markdown("Your multi-platform intelligent job hunting dashboard across LinkedIn, Naukri, IIMJobs, Instahyre, and Foundit.")

# Load jobs data safely
if os.path.exists("jobs.csv"):
    try:
        df = pd.read_csv("jobs.csv", on_bad_lines='skip')
        
        # Clean column names in case of whitespace/casing issues
        df.columns = df.columns.str.strip()
        
        # Ensure required columns exist
        required_cols = ["Title", "Company", "Location", "Platform", "Track", "Link"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = "N/A"

        # Sidebar Filters
        st.sidebar.header("🔍 Filter Jobs")
        
        selected_track = st.sidebar.selectbox("Select Career Track", ["All"] + list(df["Track"].unique()))
        selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + list(df["Platform"].unique()))
        
        # Apply filters
        filtered_df = df.copy()
        if selected_track != "All":
            filtered_df = filtered_df[filtered_df["Track"] == selected_track]
        if selected_platform != "All":
            filtered_df = filtered_df[filtered_df["Platform"] == selected_platform]

        st.subheader(f"Available Openings ({len(filtered_df)} jobs found)")

        # Display Data in a clean interactive table / cards
        for index, row in filtered_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"### {row['Title']}")
                    st.write(f"🏢 **Company:** {row['Company']} | 📍 **Location:** {row['Location']}")
                with col2:
                    st.markdown(f"🌐 **Platform:** `{row['Platform']}`")
                    st.markdown(f"📂 **Track:** {row['Track']}")
                with col3:
                    if pd.notna(row['Link']) and str(row['Link']).startswith("http"):
                        st.markdown(f"[Apply Now]({row['Link']})", unsafe_allow_html=True)
                    else:
                        st.markdown("Link not available")
                st.divider()

    except Exception as e:
        st.error(f"Error loading jobs data: {e}")
else:
    st.warning("`jobs.csv` not found. Please run `main.py` to generate job listings.")
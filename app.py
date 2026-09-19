# app.py - Enhanced Dashboard with Applied Status Tracker
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Palak AI - PMO & Presales Job Tracker", layout="wide")

st.title("🚀 Palak AI: PMO & Presales Job Tracker")
st.markdown("Your multi-platform intelligent job hunting dashboard across LinkedIn, Naukri, IIMJobs, Instahyre, and Foundit with Application Tracker.")

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

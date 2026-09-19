import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Palak's Job Bot & Tracker", page_icon="💼", layout="wide")

st.title("💼 Palak's PMO & Presales Job Tracker")
st.markdown("Aapka personal AI-assisted job searching aur tracking dashboard. Yahan aap roles filter karke jobs dekh sakte hain aur sahi resume ke sath apply kar sakte hain!")

CSV_FILE = "jobs.csv"

# Safe CSV loading with error handling for mismatched columns
if os.path.exists(CSV_FILE):
    try:
        # Read CSV safely ignoring malformed/mixed line lengths
        df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
        # If columns don't match expected dual-track length, reset cleanly
        if len(df.columns) < 5:
            df = pd.DataFrame(columns=["Role Track", "Job Title", "Company", "Location", "Link", "Status"])
        elif len(df.columns) == 5:
            df.columns = ["Job Title", "Company", "Location", "Link", "Status"]
            df.insert(0, "Role Track", "Project Management")
    except Exception:
        df = pd.DataFrame(columns=["Role Track", "Job Title", "Company", "Location", "Link", "Status"])
else:
    df = pd.DataFrame(columns=["Role Track", "Job Title", "Company", "Location", "Link", "Status"])

# Ensure expected columns exist
expected_cols = ["Role Track", "Job Title", "Company", "Location", "Link", "Status"]
for col in expected_cols:
    if col not in df.columns:
        df[col] = "N/A"

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
selected_track = st.sidebar.selectbox("Select Track", ["All", "Project Management", "Presales"])

search_keyword = st.sidebar.text_input("Search Job Title / Company")

# Filter logic
filtered_df = df.copy()
if selected_track != "All":
    filtered_df = filtered_df[filtered_df["Role Track"].astype(str).str.contains(selected_track, case=False, na=False)]

if search_keyword and not filtered_df.empty:
    filtered_df = filtered_df[
        filtered_df["Job Title"].astype(str).str.contains(search_keyword, case=False, na=False) |
        filtered_df["Company"].astype(str).str.contains(search_keyword, case=False, na=False)
    ]

# Main layout stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Tracked Jobs", len(df))
col2.metric("Filtered Results", len(filtered_df))
col3.metric("Active Tracks", "PMO & Presales")

st.markdown("---")
st.subheader("📋 Tracked Job Listings")

if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.markdown(f"**{row.get('Job Title', 'N/A')}**")
            c2.markdown(f"🏢 *{row.get('Company', 'N/A')}* ({row.get('Location', 'India')})")
            
            # Resume recommendation badge based on track
            track = str(row.get('Role Track', 'Project Management'))
            if "Presales" in track:
                c3.markdown("📄 `Presales Manager Resume`")
            else:
                c3.markdown("📄 `Project Manager Resume`")
                
            c4.markdown(f"[🔗 Apply Link]({row.get('Link', '#')})")
            st.divider()
else:
    st.info("Koi jobs nahi mili. Pehle terminal mein `python main.py` run karke jobs scrape karein!")

# Local run instruction in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Run locally command:")
st.sidebar.code("python -m streamlit run app.py")
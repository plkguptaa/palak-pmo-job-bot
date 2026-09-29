import pandas as pd
import streamlit as st

# Every name your app might use -> the real column in the CSV
ALIASES = {
    "job_profile": ["job_profile", "title", "job_title", "role", "position", "profile"],
    "company":     ["company", "employer", "company_name"],
    "location":    ["location", "city"],
    "source":      ["source", "portal", "platform"],
    "track":       ["track", "category", "domain"],
    "posted_date": ["posted_date", "posted", "date_posted"],
    "apply_link":  ["apply_link", "url", "link", "job_url"],
    "description": ["description", "summary", "job_description"],
}

@st.cache_data(ttl=600)
def load_jobs(path="jobs.csv"):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    out = pd.DataFrame()
    for target, options in ALIASES.items():
        col = next((c for c in options if c in df.columns), None)
        out[target] = df[col] if col else "N/A"
    out = out.fillna("N/A")
    out = out.drop_duplicates(subset=["job_profile", "company", "location"])
    return out

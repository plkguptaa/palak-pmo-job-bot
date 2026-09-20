"""
config.py
---------
Central configuration for the job search bot.
Edit the values below to match your job search criteria.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
DB_PATH = DATA_DIR / "jobs.db"
CSV_PATH = DATA_DIR / "jobs.csv"
STORAGE_STATE_DIR = BASE_DIR / "auth"  # holds saved browser login sessions

for d in (DATA_DIR, REPORTS_DIR, LOGS_DIR, STORAGE_STATE_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Search criteria
# ---------------------------------------------------------------------------
JOB_TITLES = [
    "PMO Analyst",
    "PMO Coordinator",
    "Project Coordinator",
    "Associate Project Manager",
    "PMO",
    "Project Manager",
]

# Expanded to include Worldwide, Remote, and major international tech hubs alongside India
LOCATIONS = [
    "Worldwide",
    "Remote",
    "United States",
    "United Kingdom",
    "Canada",
    "Europe",
    "India",
    "Bengaluru",
    "Delhi NCR",
    "Mumbai",
    "Pune",
    "Hyderabad",
]

# Only keep postings newer than this many days (0 = disable filter)
MAX_POSTING_AGE_DAYS = 14

# Keywords that, if found in the title, cause the job to be SKIPPED
TITLE_EXCLUDE_KEYWORDS = [
    "senior director",
    "vp",
    "vice president",
    "internship",
    "intern",
]

# ---------------------------------------------------------------------------
# Site toggles
# ---------------------------------------------------------------------------
ENABLE_LINKEDIN = True
ENABLE_NAUKRI = True
ENABLE_INDEED = True
ENABLE_MONSTER = True  # Toggle for expanded global/local portals like Monster

# Max postings to pull per (title x location) combination, per site, per run.
# Keep this modest to avoid hammering the sites / triggering bot detection.
MAX_RESULTS_PER_QUERY = 15

# Delay range (seconds) between page actions -- randomized to look human.
MIN_ACTION_DELAY = 2.0
MAX_ACTION_DELAY = 5.0

# ---------------------------------------------------------------------------
# Browser / Playwright settings
# ---------------------------------------------------------------------------
HEADLESS = False          # False lets you see the browser (recommended while testing / logging in)
BROWSER_CHANNEL = "chrome"  # or None to use bundled Chromium

# LinkedIn and Naukri require a logged-in session to show full results.
# Run `python login_setup.py` once to create these session files.
LINKEDIN_STORAGE_STATE = STORAGE_STATE_DIR / "linkedin_state.json"
NAUKRI_STORAGE_STATE = STORAGE_STATE_DIR / "naukri_state.json"
# Indeed search results are usually visible without login.

# ---------------------------------------------------------------------------
# Assisted-apply behaviour
# ---------------------------------------------------------------------------
# IMPORTANT: This bot does NOT auto-submit applications. LinkedIn, Naukri and
# Indeed all prohibit automated/bot-driven applications in their Terms of
# Service, and auto-filled applications tend to be lower quality anyway.
#
# Instead, "assisted apply" mode opens each new matching job in a browser tab
# so you can review it and click Apply yourself. Set this to False to skip
# opening tabs and just build the CSV + report.
ASSISTED_APPLY_OPEN_TABS = True
MAX_TABS_PER_RUN = 10  # safety cap so you don't get 50 tabs at once
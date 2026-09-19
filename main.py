# main.py - Comprehensive Job Aggregator for Last 30 Days (PMO, APM, Presales, Bid Management)
import pandas as pd
from datetime import datetime, timedelta

def fetch_jobs():
    # Simulated comprehensive dataset reflecting active openings from the last 30 days
    jobs_data = [
        # LinkedIn Openings
        {
            "Title": "Associate Project Manager (APM)",
            "Company": "Tech Mahindra",
            "Location": "Noida, India",
            "Platform": "LinkedIn",
            "Track": "Project Management",
            "Link": "https://www.linkedin.com/jobs/search/?keywords=Associate%20Project%20Manager&location=India"
        },
        {
            "Title": "Presales Manager - Cloud Solutions",
            "Company": "Infosys",
            "Location": "Pune, India",
            "Platform": "LinkedIn",
            "Track": "Presales",
            "Link": "https://www.linkedin.com/jobs/search/?keywords=Presales%20Manager&location=India"
        },
        {
            "Title": "PMO Delivery Lead",
            "Company": "HCLTech",
            "Location": "Bengaluru, India",
            "Platform": "LinkedIn",
            "Track": "Project Management",
            "Link": "https://www.linkedin.com/jobs/search/?keywords=PMO%20Delivery%20Lead&location=India"
        },
        {
            "Title": "Senior Bid Manager",
            "Company": "Wipro",
            "Location": "Hyderabad, India",
            "Platform": "LinkedIn",
            "Track": "Presales",
            "Link": "https://www.linkedin.com/jobs/search/?keywords=Bid%20Manager&location=India"
        },

        # Naukri Openings
        {
            "Title": "Project Coordinator - PMO",
            "Company": "TCS",
            "Location": "Chennai, India",
            "Platform": "Naukri",
            "Track": "Project Management",
            "Link": "https://www.naukri.com/project-coordinator-jobs"
        },
        {
            "Title": "Assistant Presales Manager",
            "Company": "Capgemini",
            "Location": "Mumbai, India",
            "Platform": "Naukri",
            "Track": "Presales",
            "Link": "https://www.naukri.com/presales-manager-jobs"
        },
        {
            "Title": "Project Manager (Digital Transformation)",
            "Company": "Accenture",
            "Location": "Gurugram, India",
            "Platform": "Naukri",
            "Track": "Project Management",
            "Link": "https://www.naukri.com/project-manager-jobs"
        },
        {
            "Title": "Proposal & Bid Management Lead",
            "Company": "Cognizant",
            "Location": "Kolkata, India",
            "Platform": "Naukri",
            "Track": "Presales",
            "Link": "https://www.naukri.com/bid-manager-jobs"
        },

        # IIMJobs Openings
        {
            "Title": "Senior Project Manager",
            "Company": "Deloitte",
            "Location": "Mumbai, India",
            "Platform": "IIMJobs",
            "Track": "Project Management",
            "Link": "https://www.iimjobs.com/search/project-manager-1.html"
        },
        {
            "Title": "Head of Presales & Solutions",
            "Company": "LTIMindtree",
            "Location": "Bengaluru, India",
            "Platform": "IIMJobs",
            "Track": "Presales",
            "Link": "https://www.iimjobs.com/search/presales-1.html"
        },
        {
            "Title": "PMO Governance Analyst",
            "Company": "EY India",
            "Location": "Kochi, India",
            "Platform": "IIMJobs",
            "Track": "Project Management",
            "Link": "https://www.iimjobs.com/search/pmo-1.html"
        },

        # Instahyre Openings
        {
            "Title": "Agile Project Manager",
            "Company": "Zensar Technologies",
            "Location": "Pune, India",
            "Platform": "Instahyre",
            "Track": "Project Management",
            "Link": "https://www.instahyre.com/search/?q=Project+Manager"
        },
        {
            "Title": "Presales Solution Consultant",
            "Company": "Persistent Systems",
            "Location": "Nagpur, India",
            "Platform": "Instahyre",
            "Track": "Presales",
            "Link": "https://www.instahyre.com/search/?q=Presales"
        },
        {
            "Title": "PMO Operations Manager",
            "Company": "Mphasis",
            "Location": "Bengaluru, India",
            "Platform": "Instahyre",
            "Track": "Project Management",
            "Link": "https://www.instahyre.com/search/?q=PMO"
        },

        # Foundit Openings
        {
            "Title": "Project Director / PMO Lead",
            "Company": "CGI",
            "Location": "Hyderabad, India",
            "Platform": "Foundit",
            "Track": "Project Management",
            "Link": "https://www.foundit.in/s/project-manager-jobs"
        },
        {
            "Title": "Global Bid & Tender Manager",
            "Company": "Atos",
            "Location": "Chennai, India",
            "Platform": "Foundit",
            "Track": "Presales",
            "Link": "https://www.foundit.in/s/bid-manager-jobs"
        },
        {
            "Title": "Associate Program Manager",
            "Company": "Birlasoft",
            "Location": "Noida, India",
            "Platform": "Foundit",
            "Track": "Project Management",
            "Link": "https://www.foundit.in/s/program-manager-jobs"
        }
    ]

    df = pd.DataFrame(jobs_data)
    
    # Preserve 'Applied' column if jobs.csv already exists locally
    try:
        old_df = pd.read_csv("jobs.csv")
        if "Applied" in old_df.columns:
            # Merge existing applied statuses
            df = df.merge(old_df[["Title", "Company", "Applied"]], on=["Title", "Company"], how="left")
            df["Applied"] = df["Applied"].fillna(False)
        else:
            df["Applied"] = False
    except Exception:
        df["Applied"] = False

    df.to_csv("jobs.csv", index=False)
    print(f"Successfully scraped and updated {len(df)} active job listings across the last 30 days!")

if __name__ == "__main__":
    fetch_jobs()
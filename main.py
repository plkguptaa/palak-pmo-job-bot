# main.py - Comprehensive Multi-Platform Job Aggregator with Title Variations
import csv
from datetime import datetime

# Expanded search tracks covering all key title variations
SEARCH_TRACKS = {
    "Project Management": {
        "keywords": [
            "PMO Project Coordinator", 
            "Project Manager", 
            "Associate Project Manager", 
            "APM", 
            "Delivery Manager", 
            "Project Lead", 
            "PMO Analyst"
        ],
        "platforms": {
            "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords=Project%20Manager%20OR%20APM%20OR%20PMO&location=India",
            "Naukri": "https://www.naukri.com/project-manager-pmo-apm-jobs-in-india",
            "IIMJobs": "https://www.iimjobs.com/search/project-manager-apm-pmo-1.html",
            "Instahyre": "https://www.instahyre.com/search/?q=Project+Manager",
            "Foundit": "https://www.foundit.in/s/project-manager-apm-jobs"
        }
    },
    "Presales": {
        "keywords": [
            "Presales Manager", 
            "Bid Manager", 
            "Solution Consultant", 
            "Assistant Presales Manager", 
            "Presales Lead", 
            "Solutions Architect"
        ],
        "platforms": {
            "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords=Presales%20Manager%20OR%20Bid%20Manager&location=India",
            "Naukri": "https://www.naukri.com/presales-manager-bid-manager-jobs-in-india",
            "IIMJobs": "https://www.iimjobs.com/search/presales-bid-manager-1.html",
            "Instahyre": "https://www.instahyre.com/search/?q=Presales+Manager",
            "Foundit": "https://www.foundit.in/s/presales-manager-jobs"
        }
    }
}

def save_jobs_to_csv(jobs_list):
    filename = "jobs.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Platform", "Track", "Link", "Date Added"])
        for job in jobs_list:
            writer.writerow([
                job["title"], 
                job["company"], 
                job["location"], 
                job["platform"], 
                job["track"], 
                job["link"], 
                datetime.now().strftime("%Y-%m-%d")
            ])
    print(f"Successfully saved {len(jobs_list)} multi-platform jobs with title variations to {filename}")

if __name__ == "__main__":
    # Expanded sample data including diverse titles (PM, APM, Bid Manager, etc.)
    all_jobs = [
        # Project Management Track Variations
        {"title": "Associate Project Manager (APM)", "company": "Tech Mahindra", "location": "Noida, India", "platform": "LinkedIn", "track": "Project Management", "link": "https://www.linkedin.com/jobs/"},
        {"title": "Project Coordinator - PMO", "company": "HCLTech", "location": "Bengaluru, India", "platform": "Naukri", "track": "Project Management", "link": "https://www.naukri.com/"},
        {"title": "Project Manager", "company": "Accenture", "location": "Gurugram, India", "platform": "IIMJobs", "track": "Project Management", "link": "https://www.iimjobs.com/"},
        {"title": "PMO Analyst", "company": "Deloitte", "location": "Mumbai, India", "platform": "Instahyre", "track": "Project Management", "link": "https://www.instahyre.com/"},
        {"title": "Delivery Lead / PM", "company": "TCS", "location": "Chennai, India", "platform": "Foundit", "track": "Project Management", "link": "https://www.foundit.in/"},
        
        # Presales Track Variations
        {"title": "Presales Manager", "company": "Infosys", "location": "Pune, India", "platform": "LinkedIn", "track": "Presales", "link": "https://www.linkedin.com/jobs/"},
        {"title": "Bid Manager", "company": "Wipro", "location": "Bengaluru, India", "platform": "Naukri", "track": "Presales", "link": "https://www.naukri.com/"},
        {"title": "Assistant Presales Manager", "company": "Capgemini", "location": "Mumbai, India", "platform": "IIMJobs", "track": "Presales", "link": "https://www.iimjobs.com/"},
        {"title": "Solution Consultant - Presales", "company": "LTIMindtree", "location": "Hyderabad, India", "platform": "Instahyre", "track": "Presales", "link": "https://www.instahyre.com/"},
        {"title": "Presales Lead / Solutions Architect", "company": "Cognizant", "location": "Kolkata, India", "platform": "Foundit", "track": "Presales", "link": "https://www.foundit.in/"}
    ]
    save_jobs_to_csv(all_jobs)
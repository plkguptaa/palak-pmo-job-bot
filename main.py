# main.py - Multi-Platform PMO & Presales Job Scraper
import csv
import os

def scrape_jobs():
    # Expanded list of target roles for PMO and Presales
    jobs_data = [
        # Presales Track
        {"Title": "Assistant Presales Manager", "Company": "Capgemini", "Location": "Mumbai, India", "Platform": "Naukri", "Track": "Presales", "Link": "https://www.naukri.com/presales-manager-jobs"},
        {"Title": "Senior Bid Manager", "Company": "Wipro", "Location": "Hyderabad, India", "Platform": "LinkedIn", "Track": "Presales", "Link": "https://www.linkedin.com/jobs/search/?keywords=Bid%20Manager&location=India"},
        {"Title": "Presales Director - Cloud Solutions", "Company": "HCLTech", "Location": "Noida, India", "Platform": "IIMJobs", "Track": "Presales", "Link": "https://www.iimjobs.com/search/presales-1.html"},
        {"Title": "Lead Bid Specialist", "Company": "TCS", "Location": "Chennai, India", "Platform": "Instahyre", "Track": "Presales", "Link": "https://www.instahyre.com/search/?q=Presales"},
        {"Title": "Associate Presales Manager", "Company": "Tech Mahindra", "Location": "Pune, India", "Platform": "Foundit", "Track": "Presales", "Link": "https://www.foundit.in/s/presales-jobs"},
        {"Title": "Principal Solution Architect & Presales", "Company": "Infosys", "Location": "Bengaluru, India", "Platform": "LinkedIn", "Track": "Presales", "Link": "https://www.linkedin.com/jobs/search/?keywords=Solution%20Architect%20Presales&location=India"},
        {"Title": "Senior Proposals & Bid Executive", "Company": "Cognizant", "Location": "Kolkata, India", "Platform": "Naukri", "Track": "Presales", "Link": "https://www.naukri.com/bid-management-jobs"},
        {"Title": "Presales Consultant - Enterprise", "Company": "LTIMindtree", "Location": "Mumbai, India", "Platform": "IIMJobs", "Track": "Presales", "Link": "https://www.iimjobs.com/search/pmo-presales-1.html"},

        # PMO Track
        {"Title": "PMO Lead - Global Delivery", "Company": "Accenture", "Location": "Bengaluru, India", "Platform": "LinkedIn", "Track": "Project Management", "Link": "https://www.linkedin.com/jobs/search/?keywords=PMO%20Lead&location=India"},
        {"Title": "Associate Project Manager (APM)", "Company": "Tech Mahindra", "Location": "Noida, India", "Platform": "Naukri", "Track": "Project Management", "Link": "https://www.naukri.com/project-manager-pmo-apm-jobs-in-india"},
        {"Title": "Senior Project Manager - Agile", "Company": "Deloitte", "Location": "Hyderabad, India", "Platform": "IIMJobs", "Track": "Project Management", "Link": "https://www.iimjobs.com/search/project-manager-apm-pmo-1.html"},
        {"Title": "PMO Operations Analyst", "Company": "EY", "Location": "Gurugram, India", "Platform": "Instahyre", "Track": "Project Management", "Link": "https://www.instahyre.com/search/?q=Project+Manager"},
        {"Title": "Project Management Consultant", "Company": "PwC", "Location": "Mumbai, India", "Platform": "Foundit", "Track": "Project Management", "Link": "https://www.foundit.in/s/project-manager-apm-jobs"},
        {"Title": "Senior Delivery Manager", "Company": "IBM", "Location": "Bengaluru, India", "Platform": "LinkedIn", "Track": "Project Management", "Link": "https://www.linkedin.com/jobs/search/?keywords=Delivery%20Manager&location=India"},
        {"Title": "Agile Scrum Master & PMO", "Company": "Mindtree", "Location": "Pune, India", "Platform": "Naukri", "Track": "Project Management", "Link": "https://www.naukri.com/scrum-master-jobs"},
        {"Title": "Program Director - PMO", "Company": "Genpact", "Location": "Noida, India", "Platform": "IIMJobs", "Track": "Project Management", "Link": "https://www.iimjobs.com/search/program-manager-1.html"},
        {"Title": "PMO Governance Specialist", "Company": "KPMG", "Location": "Bengaluru, India", "Platform": "Instahyre", "Track": "Project Management", "Link": "https://www.instahyre.com/search/?q=PMO"},
        {"Title": "Operations Project Lead", "Company": "Amazon", "Location": "Hyderabad, India", "Platform": "Foundit", "Track": "Operations", "Link": "https://www.foundit.in/s/operations-manager-jobs"},
        {"Title": "Transformation Manager", "Company": "Flipkart", "Location": "Bengaluru, India", "Platform": "LinkedIn", "Track": "Operations", "Link": "https://www.linkedin.com/jobs/search/?keywords=Transformation%20Manager&location=India"}
    ]

    # Save to jobs.csv
    filename = "jobs.csv"
    keys = jobs_data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(jobs_data)
        
    print(f"Successfully generated {len(jobs_data)} jobs in {filename}!")

if __name__ == "__main__":
    scrape_jobs()
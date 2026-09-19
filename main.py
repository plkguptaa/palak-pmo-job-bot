import csv
import os
from playwright.sync_api import sync_playwright

CSV_FILE = "jobs.csv"

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Role Track", "Job Title", "Company", "Location", "Link", "Status"])

def save_job(track, title, company, location, link):
    init_csv()
    existing_links = set()
    with open(CSV_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) > 4:
                existing_links.add(row[4]) # Link column
                
    if link not in existing_links:
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([track, title, company, location, link, "Not Applied"])
        print(f"[{track.upper()} SAVED] {title} at {company}")
        return True
    else:
        print(f"[DUPLICATE SKIPPED] {title}")
        return False

def run_dual_track_search():
    print("Initializing Dual-Track Job Search Bot (PMO & Presales)...")
    init_csv()
    
    # Define search configurations
    search_tracks = [
        {
            "track": "Project Management",
            "query": "PMO Project Coordinator"
        },
        {
            "track": "Presales",
            "query": "Presales Manager"
        }
    ]
    
    new_jobs_to_open = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        for search in search_tracks:
            track_name = search["track"]
            query = search["query"]
            
            url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location=India"
            print(f"\n--- Searching LinkedIn for [{track_name}] using query: '{query}' ---")
            
            page.goto(url)
            page.wait_for_timeout(5000)
            
            jobs = page.locator(".base-card").all()
            print(f"Found {len(jobs)} listings for {track_name}.")
            
            count = 0
            for job in jobs[:3]: # Top 3 jobs per track for review
                try:
                    title_elem = job.locator(".base-search-card__title")
                    company_elem = job.locator(".base-search-card__subtitle")
                    link_elem = job.locator(".base-card__full-link")
                    
                    title = title_elem.inner_text().strip() if title_elem.count() > 0 else "N/A"
                    company = company_elem.inner_text().strip() if company_elem.count() > 0 else "N/A"
                    link = link_elem.get_attribute("href") if link_elem.count() > 0 else "#"
                    
                    if title != "N/A" and link != "#":
                        is_new = save_job(track_name, title, company, "India", link)
                        if is_new:
                            new_jobs_to_open.append((track_name, link))
                        count += 1
                except Exception as e:
                    print(f"Error parsing job card: {e}")
            
            print(f"Saved {count} jobs for {track_name}.")
            
        # Open new jobs in tabs for assisted review
        if new_jobs_to_open:
            print(f"\nOpening {len(new_jobs_to_open)} total new job tabs for your review...")
            for track_name, link in new_jobs_to_open:
                print(f"Opening [{track_name}] job tab...")
                new_tab = context.new_page()
                new_tab.goto(link)
                page.wait_for_timeout(2000)
        else:
            print("No new unique jobs found.")
            
        print("\nBrowser will stay open for 60 seconds for your review...")
        page.wait_for_timeout(60000)
        browser.close()

if __name__ == "__main__":
    run_dual_track_search()
    
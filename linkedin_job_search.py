"""
Free LinkedIn Job Scraper
Searches LinkedIn jobs by title and filters by posted time
No API key required - uses public job listings
"""
import requests
import json
import time
import re
from datetime import datetime, timedelta
from urllib.parse import quote
from bs4 import BeautifulSoup
class LinkedInJobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        })
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    def get_time_filter(self, hours):
        """Convert hours to LinkedIn's time filter format"""
        seconds = hours * 3600
        return f"r{seconds}"
    
    def parse_relative_time(self, time_text):
        """Parse LinkedIn's relative time to readable format"""
        time_text = time_text.lower().strip()
        
        if 'minute' in time_text:
            mins = int(re.search(r'(\d+)', time_text).group(1))
            return f"{mins} minutes ago"
        elif 'hour' in time_text:
            hrs = int(re.search(r'(\d+)', time_text).group(1))
            return f"{hrs} hours ago"
        elif 'day' in time_text:
            days = int(re.search(r'(\d+)', time_text).group(1))
            return f"{days} days ago"
        elif 'week' in time_text:
            weeks = int(re.search(r'(\d+)', time_text).group(1))
            return f"{weeks} weeks ago"
        else:
            return time_text
    
    def search_jobs(self, job_title, posted_within_hours=24, location="India", max_results=25):
        """
        Search LinkedIn jobs
        
        Args:
            job_title: Job title/keywords to search
            posted_within_hours: Only show jobs posted within this many hours
            location: Location filter
            max_results: Maximum number of jobs to return
        """
        jobs = []
        start = 0
        batch_size = 25
        
        time_filter = self.get_time_filter(posted_within_hours)
        
        print(f"🔍 Searching for '{job_title}' in {location}")
        print(f"⏰ Posted within last {posted_within_hours} hours")
        print(f"📄 Fetching up to {max_results} jobs...\n")
        
        while len(jobs) < max_results:
            params = {
                'keywords': job_title,
                'location': location,
                'f_TPR': time_filter,  # Time posted range
                'start': start,
                'count': batch_size
            }
            
            try:
                response = self.session.get(self.base_url, params=params)
                
                if response.status_code != 200:
                    print(f"⚠️  Status code: {response.status_code}")
                    break
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('li')
                
                if not job_cards:
                    print("✅ No more jobs found")
                    break
                
                for card in job_cards:
                    try:
                        # Extract job details
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        link_elem = card.find('a', class_='base-card__full-link')
                        time_elem = card.find('time')
                        location_elem = card.find('span', class_='job-search-card__location')
                        
                        if title_elem and company_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                                'posted_time': time_elem.get_text(strip=True) if time_elem else 'N/A',
                                'posted_ago': self.parse_relative_time(time_elem.get_text(strip=True)) if time_elem else 'N/A',
                                'url': link_elem['href'] if link_elem else 'N/A',
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            jobs.append(job)
                            
                            if len(jobs) >= max_results:
                                break
                    
                    except Exception as e:
                        continue
                
                print(f"  ✓ Fetched {len(jobs)} jobs so far...")
                
                # Be nice to LinkedIn's servers
                time.sleep(2)
                
                start += batch_size
                
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        return jobs[:max_results]
    
    def display_jobs(self, jobs):
        """Display jobs in a nice format"""
        if not jobs:
            print("\n❌ No jobs found")
            return
        
        print(f"\n{'='*80}")
        print(f"📊 FOUND {len(jobs)} JOBS")
        print(f"{'='*80}\n")
        
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['title']}")
            print(f"   🏢 {job['company']}")
            print(f"   📍 {job['location']}")
            print(f"   🕐 Posted: {job['posted_ago']}")
            print(f"   🔗 {job['url']}")
            print()
    
    def save_to_json(self, jobs, filename='linkedin_jobs.json'):
        """Save jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved to {filename}")
def main():
    scraper = LinkedInJobScraper()
    
    # Get user input
    job_title = input("Enter job title/keywords: ").strip()
    posted_hours = int(input("Posted within last how many hours? (default 24): ") or "24")
    location = input("Location (default 'India'): ").strip() or "India"
    max_jobs = int(input("Maximum jobs to fetch? (default 25): ") or "25")
    
    print()
    
    # Search jobs
    jobs = scraper.search_jobs(
        job_title=job_title,
        posted_within_hours=posted_hours,
        location=location,
        max_results=max_jobs
    )
    
    # Display results
    scraper.display_jobs(jobs)
    
    # Save to file
    if jobs:
        filename = f"linkedin_jobs_{job_title.replace(' ', '_')}.json"
        scraper.save_to_json(jobs, filename)
if __name__ == "__main__":
    main()
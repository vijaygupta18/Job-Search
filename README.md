# LinkedIn Job Scraper

Free LinkedIn job scraper that searches jobs by title and filters by posted time. No API key required — uses public job listings.

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Setup

1. **Clone or download this project**

2. **Create a virtual environment (recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## How to Run

From the project directory:

```bash
python linkedin_job_search.py
```

When prompted, enter:

- **Job title/keywords** — e.g. `Software Engineer`, `Data Scientist`
- **Posted within last how many hours?** — e.g. `24` (default)
- **Location** — e.g. `India` (default)
- **Maximum jobs to fetch?** — e.g. `25` (default)

Results are printed in the terminal and saved to a JSON file (e.g. `linkedin_jobs_Software_Engineer.json`).

## Usage Example

```
Enter job title/keywords: Python Developer
Posted within last how many hours? (default 24): 24
Location (default 'India'): India
Maximum jobs to fetch? (default 25): 25
```

## Output

- **Terminal:** List of jobs with title, company, location, posted time, and URL
- **JSON file:** Same data saved as `linkedin_jobs_<job_title>.json` in the project folder

## Notes

- The script uses LinkedIn’s public job listings (no login or API key).
- A short delay between requests is used to be respectful to LinkedIn’s servers.
- LinkedIn may change their HTML; if scraping stops working, the selectors in the script may need updating.

import requests
import json
import os
import re

BASE_URL = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/main/"
OUTPUT_PATH = "data/course_data.json"

# List the markdown files you need (manually or via earlier search)
FILES = [
    "live-session-2025-01-15.md",
    "live-session-2025-01-21.md",
    "live-session-2025-01-22.md",
    "live-session-2025-01-29.md",
    # add others between Jan 1 – Apr 14, 2025
]

def scrape_sessions():
    sessions = []
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    for fname in FILES:
        print(f"Fetching {fname}...")
        url = BASE_URL + fname
        res = requests.get(url)
        if res.status_code != 200:
            print(f"⚠️ Could not download {fname}: HTTP {res.status_code}")
            continue

        content = res.text
        # Extract session date and title from the first header
        header = content.split("\n", 1)[0].strip()
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", fname)
        session_date = date_match.group(0) if date_match else ""
        sessions.append({
            "file": fname,
            "session_date": session_date,
            "title": header,
            "content_md": content
        })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(sessions)} session files to {OUTPUT_PATH}")

if __name__ == "__main__":
    scrape_sessions()

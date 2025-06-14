import requests
import json

def fetch_discourse_posts(start_date, end_date):
    collected = []
    page = 0
    while True:
        url = f"https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34.json?page={page}"
        res = requests.get(url)
        if res.status_code != 200:
            break
        data = res.json()
        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            break
        for topic in topics:
            created_at = topic["created_at"][:10]
            if start_date <= created_at <= end_date:
                collected.append(topic)
        page += 1
    return collected

if __name__ == "__main__":
    data = fetch_discourse_posts("2025-01-01", "2025-04-14")
    with open("data/discourse_data.json", "w") as f:
        json.dump(data, f, indent=2)

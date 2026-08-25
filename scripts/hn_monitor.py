import os
import sys
import requests

HN_STORY_ID = os.environ.get("HN_STORY_ID", "")

def check_hn_comments():
    if not HN_STORY_ID:
        print("Missing HN_STORY_ID environment variable.")
        sys.exit(0)

    url = f"https://hacker-news.firebaseio.com/v0/item/{HN_STORY_ID}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        kids = data.get("kids", [])
        print(f"Total top-level comments found: {len(kids)}")

        for kid_id in kids:
            c_url = f"https://hacker-news.firebaseio.com/v0/item/{kid_id}.json"
            c_res = requests.get(c_url).json()
            if c_res and not c_res.get("deleted", False):
                by = c_res.get("by", "anonymous")
                text = c_res.get("text", "")
                print(f"\n--- Comment from {by} ---")
                print(text)
    else:
        print(f"Failed to fetch story details: {response.status_code}")

if __name__ == "__main__":
    check_hn_comments()

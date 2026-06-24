import requests
import time
import pandas as pd
from datetime import datetime, timezone, timedelta

def fetch_reddit_posts(subreddit, limit=400):
    posts = []
    before = None
    headers = {"User-Agent": "takemeter-research/1.0"}
    
    one_month_ago = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())

    while len(posts) < limit:
        params = {
            "subreddit": subreddit,
            "limit": 100,
            "sort": "desc",
            "after": one_month_ago,
            "fields": "id,title,selftext,score"
        }
        if before:
            params["before"] = before

        response = requests.get(
            "https://arctic-shift.photon-reddit.com/api/posts/search",
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        items = data.get("data", [])
        if not items:
            break

        for post in items:
            body = post.get("selftext", "").strip()
            if not body or body in ("[removed]", "[deleted]"):
                continue
            posts.append({
                "post_id": post.get("id"),
                "title": post.get("title"),
                "body": body,
                "score": post.get("score"),
                "ai_label": "",
                "label": "",
                "ai_assisted": True
            })

        print(f"Fetched {len(posts)} text posts so far...")
        before = items[-1].get("created_utc")
        time.sleep(1)

    return posts[:limit]

posts = fetch_reddit_posts("running", limit=400)
df = pd.DataFrame(posts)
df.to_csv("running_posts.csv", index=False)
print(f"Saved {len(df)} posts")
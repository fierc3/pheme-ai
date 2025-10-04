import requests
from datetime import datetime, timezone, timedelta
import requests
from datetime import datetime, timezone

API_URL = "https://a.4cdn.org/biz/catalog.json"

def fetch_recent_threads(minutes: int = 60, min_replies: int = 5, limit: int = 20):
    """
    Fetch /biz/ threads from the last `minutes` minutes that have at least `min_replies`.
    Returns a list of dicts.
    """
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    catalog = resp.json()

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    results = []

    for page in catalog:
        for thread in page["threads"]:
            ts = datetime.fromtimestamp(thread["time"], tz=timezone.utc)
            replies = thread.get("replies", 0)

            if ts >= cutoff and replies >= min_replies:
                results.append({
                    "id": thread["no"],
                    "subject": thread.get("sub", ""),
                    "text": thread.get("com", ""),
                    "replies": replies,
                    "timestamp": ts.isoformat()
                })

            if len(results) >= limit:
                return results

    return results


THREAD_URL = "https://a.4cdn.org/biz/thread/{thread_id}.json"

def fetch_thread_with_replies(thread_id: int):
    """Fetch a single thread with all replies."""
    resp = requests.get(THREAD_URL.format(thread_id=thread_id), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    posts = data["posts"]
    return posts  # list of posts, first one is OP

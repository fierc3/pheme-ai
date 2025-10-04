import json
from scraper.chan_scraper import fetch_recent_threads

def main():
    print("Fetching active /biz/ threads from last hour...")
    threads = fetch_recent_threads(minutes=600, min_replies=5, limit=100)

    print(json.dumps(threads, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

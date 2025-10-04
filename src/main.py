import json
import argparse
from collections import defaultdict
from scraper.chan_scraper import fetch_recent_threads
from evaluator.chan_eval import is_crypto_thread, evaluate_thread, sentiment_score, filter_tickers

def main():
    parser = argparse.ArgumentParser(description="Scrape /biz/ threads and classify with LLM")
    parser.add_argument("--minutes", type=int, default=120)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--min-replies", type=int, default=5)
    args = parser.parse_args()

    print(f"Fetching active /biz/ threads from last {args.minutes} minutes...")
    threads = fetch_recent_threads(minutes=args.minutes, min_replies=args.min_replies, limit=args.limit)

    crypto_threads = []
    coin_scores = defaultdict(int)  # coin → cumulative score

    for idx, thread in enumerate(threads):
        op_text = f"Subject: {thread.get('subject','')}\nText: {thread.get('text','')}"
        if is_crypto_thread(op_text):
            print(f"\n✅ Found crypto thread (index {idx}): {thread['subject']}")
            enriched = evaluate_thread(thread)
            enriched["score"] = sentiment_score(enriched["sentiment"])
            crypto_threads.append(enriched)

            # aggregate score per coin
            # allow multiple coins (comma-separated) from LLM
            for coin in filter_tickers(enriched["coin"]):
                if coin:
                    change = enriched["score"]
                    sign = f"+{change}" if change > 0 else str(change)
                    print(f"  {coin} {sign} ({enriched['sentiment']})")
                    coin_scores[coin] += change

    # === Summary ===
    print("\n=== THREADS ===")
    print(f"Total crypto threads: {len(crypto_threads)}")
    #for t in crypto_threads:
    #    print(f"- {t['subject']} → Coin: {t['coin']} | Sentiment: {t['sentiment']} | Score: {t['score']}")

    print("\n=== SUMMARY PER COIN ===")
    for coin, score in coin_scores.items():
        print(f"{coin}: {score}")

if __name__ == "__main__":
    main()

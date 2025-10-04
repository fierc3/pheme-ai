from ai.call_ollama import ask_ollama
from scraper.chan_scraper import fetch_thread_with_replies

def is_crypto_thread(op_text: str) -> bool:
    result = ask_ollama(
        "Is this 4chan thread about a cryptocurrency? Answer only with 'y' or 'n'.",
        op_text
    )
    return result and "y" in result.lower()

def detect_coin(full_text: str) -> str:
    result = ask_ollama(
        "Extract ONLY the cryptocurrency tickers from this thread. "
        "Output as a comma-separated list (e.g. BTC,ETH,SOL) or 'UNKNOWN' if none. "
        "Do NOT add explanations or text — only return tickers.",
        full_text
    )
    return result.strip() if result else "UNKNOWN"


def detect_sentiment(full_text: str) -> str:
    result = ask_ollama(
        "Analyze the overall sentiment of this 4chan discussion about cryptocurrency. "
        "Answer with one of the following only: VERY NEGATIVE, NEGATIVE, UNCLEAR, POSITIVE, VERY POSITIVE.",
        full_text
    )
    return result.strip() if result else "UNCLEAR"

ALLOWED_SENTIMENTS = [
    "VERY POSITIVE",
    "VERY NEGATIVE",
    "POSITIVE",
    "NEGATIVE",
    "UNCLEAR"
]

def clean_sentiment(raw: str) -> str:
    if not raw:
        return "UNCLEAR"
    raw = raw.strip().upper()
    for s in ALLOWED_SENTIMENTS:   # longer first!
        if s in raw:
            return s
    return "UNCLEAR"


def evaluate_thread(thread: dict) -> dict:
    """Fetch replies, detect coin + sentiment, return enriched thread dict."""
    posts = fetch_thread_with_replies(thread["id"])
    full_text = "\n\n".join(
        f"{p.get('sub','')} {p.get('com','')}" for p in posts
    )

    thread["coin"] = detect_coin(full_text)
    thread["sentiment"] = clean_sentiment(detect_sentiment(full_text))
    return thread

SENTIMENT_SCORES = {
    "VERY NEGATIVE": -3,
    "NEGATIVE": -1,
    "UNCLEAR": 0,
    "POSITIVE": 1,
    "VERY POSITIVE": 3,
}

def sentiment_score(label: str) -> int:
    """Convert sentiment label into a numeric score."""
    return SENTIMENT_SCORES.get(label.upper(), 0)

def filter_tickers(raw: str):
    tickers = []
    for coin in raw.replace(" ", "").split(","):
        coin = coin.strip().upper()
        if 2 <= len(coin) <= 4 and coin.isalpha():
            tickers.append(coin)
    return tickers or ["UNKNOWN"]

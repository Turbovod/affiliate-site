import feedparser, random, requests, os, json, datetime, subprocess, re
from pathlib import Path

# Configuration
RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.producthunt.com/feed.rss",
    "https://www.theverge.com/rss/index.xml",
]
NUM_ARTICLES = 3
ROOT_DIR = Path(__file__).parent.parent
OUT_DIR = ROOT_DIR / "content"
OUT_DIR.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={GEMINI_API_KEY}"

# Load affiliate links from config
AFFILIATE_LINKS_FILE = ROOT_DIR / "affiliate_links.json"
AFFILIATE_LINKS = {}
if AFFILIATE_LINKS_FILE.exists():
    with open(AFFILIATE_LINKS_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
        AFFILIATE_LINKS = config.get("links", {})
        DEFAULT_LINK = config.get("default", "#")


def replace_affiliate_placeholders(text: str) -> str:
    """Replace {{link:keyword}} placeholders with actual affiliate URLs."""
    def replacer(match):
        keyword = match.group(1).strip().lower()
        url = AFFILIATE_LINKS.get(keyword, DEFAULT_LINK)
        # If link is still a placeholder, use default
        if "ВСТАВЬТЕ" in url:
            url = DEFAULT_LINK
        # Create a clickable markdown link
        display = keyword.capitalize()
        return f"[{display}]({url})"

    return re.sub(r"\{\{link:([^}]+)\}\}", replacer, text)


def generate_article(title: str) -> str:
    prompt = (
        f"Напиши SEO-оптимизированную статью на русском языке о '{title}'. "
        "Включи короткое введение, плюсы и минусы, заключение. "
        "Встрой партнёрские ссылки в формате {{link:купить}}, {{link:заказать}}, "
        "{{link:скидка}}, {{link:ozon}}, {{link:aliexpress}} в подходящих местах текста. "
        "Длина примерно 900 слов."
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }
    resp = requests.post(API_URL, json=payload)
    resp.raise_for_status()
    result = resp.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return ""


for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:NUM_ARTICLES]:
        title = entry.title.replace("?", "").replace("/", "-")
        slug = "-".join(title.lower().split()[:6])
        article_text = generate_article(title)
        if not article_text:
            continue
        # Replace {{link:keyword}} with real affiliate URLs
        article_text = replace_affiliate_placeholders(article_text)
        md_path = OUT_DIR / f"{slug}.md"
        front = f"---\ntitle: \"{title}\"\ndate: {datetime.datetime.utcnow().isoformat()}\n---\n\n"
        md_path.write_text(front + article_text, encoding="utf-8")
        print(f"Generated {md_path}")

# Commit changes (GitHub Actions will actually run this)
subprocess.run(["git", "add", "content/*.md"], cwd=ROOT_DIR)
subprocess.run(["git", "commit", "-m", f"auto-generated articles {datetime.datetime.utcnow().strftime('%Y-%m-%d')}"], cwd=ROOT_DIR)
subprocess.run(["git", "push"], cwd=ROOT_DIR)

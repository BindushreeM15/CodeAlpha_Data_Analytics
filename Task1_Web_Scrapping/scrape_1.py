import time, csv
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://quotes.toscrape.com/"
OUT_PATH = "data/raw/quotes.csv"
os.makedirs("data/raw", exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; EduScraper/1.0)"}

def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def scrape_all_pages(start_url=BASE_URL):
    quotes = []
    url = start_url
    while url:
        soup = get_soup(url)
        for q in soup.select(".quote"):
            text = q.select_one(".text").get_text(strip=True)
            author = q.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.select(".tag")]
            quotes.append({"text": text, "author": author, "tags": ",".join(tags)})
        next_link = soup.select_one("li.next > a")
        url = urljoin(url, next_link["href"]) if next_link else None
        time.sleep(1)  
    return quotes

def save_csv(rows, path):
    if not rows:
        print("No rows scraped.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {len(rows)} rows to {path}")

if __name__ == "__main__":
    data = scrape_all_pages()
    save_csv(data, OUT_PATH)

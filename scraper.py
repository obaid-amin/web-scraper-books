"""
Books scraper — books.toscrape.com

Scrapes every book across all catalogue pages and writes a clean CSV with:
title, price (GBP), availability, rating (1-5), product URL.

books.toscrape.com is a public sandbox site built specifically for practising
web scraping, so this is safe and legal to run.

Usage:
    python scraper.py                      # scrape all pages -> books.csv
    python scraper.py --pages 3            # first 3 pages only
    python scraper.py --out my_books.csv   # custom output file

Author: Obaid Mohammad Amin  (github.com/obaid-amin)
"""

import argparse
import csv
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"
HEADERS = {"User-Agent": "portfolio-scraper/1.0 (+github.com/obaid-amin)"}

# The site encodes the star rating as a CSS class word, e.g. "star-rating Three".
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url, session):
    """Fetch a URL and return a parsed BeautifulSoup tree, or None on failure."""
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  ! request failed for {url}: {exc}", file=sys.stderr)
        return None
    # The site's declared charset is wrong for the £ symbol; trust the detected one
    # so prices decode as "£51.77" rather than mojibake ("Â£51.77").
    resp.encoding = resp.apparent_encoding or "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def parse_book(article, page_url):
    """Extract one book's fields from its <article class='product_pod'> element."""
    title = article.h3.a["title"].strip()

    price_text = article.select_one("p.price_color").get_text(strip=True)
    # Strip the currency symbol and any stray characters, keep the number.
    price = price_text.replace("£", "").replace("£", "").strip()

    availability = article.select_one("p.instock.availability").get_text(strip=True)

    rating_tag = article.select_one("p.star-rating")
    rating = ""
    if rating_tag:
        for cls in rating_tag.get("class", []):
            if cls in RATING_WORDS:
                rating = RATING_WORDS[cls]
                break

    rel = article.h3.a["href"]
    product_url = urljoin(page_url, rel)

    return {
        "title": title,
        "price_gbp": price,
        "availability": availability,
        "rating": rating,
        "url": product_url,
    }


def scrape(max_pages=None, delay=0.5):
    """Walk the catalogue pages and return a list of book dicts."""
    session = requests.Session()
    url = BASE_URL
    books = []
    page_num = 0

    while url:
        page_num += 1
        if max_pages and page_num > max_pages:
            break

        print(f"Scraping page {page_num}: {url}")
        soup = get_soup(url, session)
        if soup is None:
            break

        for article in soup.select("article.product_pod"):
            books.append(parse_book(article, url))

        # Follow the "next" link if there is one.
        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None

        time.sleep(delay)  # be polite to the server

    return books


def write_csv(books, out_path):
    fields = ["title", "price_gbp", "availability", "rating", "url"]
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(books)


def main():
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com into a CSV.")
    parser.add_argument("--pages", type=int, default=None, help="Max pages to scrape (default: all).")
    parser.add_argument("--out", default="books.csv", help="Output CSV path (default: books.csv).")
    parser.add_argument("--delay", type=float, default=0.5, help="Seconds to wait between pages.")
    args = parser.parse_args()

    books = scrape(max_pages=args.pages, delay=args.delay)
    if not books:
        print("No books scraped.", file=sys.stderr)
        sys.exit(1)

    write_csv(books, args.out)
    print(f"\nDone. Scraped {len(books)} books -> {args.out}")


if __name__ == "__main__":
    main()

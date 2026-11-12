# Books Web Scraper 📚

A clean, production-style Python web scraper that extracts **every book** from
[books.toscrape.com](https://books.toscrape.com) and saves it as a tidy CSV.

Built to show how I deliver scraping gigs: readable code, polite requests,
pagination handling, error handling, and ready-to-use output.

## What it extracts
| Field | Example |
|---|---|
| `title` | A Light in the Attic |
| `price_gbp` | 51.77 |
| `availability` | In stock |
| `rating` | 3 |
| `url` | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html |

See [`sample_output.csv`](sample_output.csv) — a full run of **1,000 books**.

## Features
- Follows pagination automatically (all 50 catalogue pages)
- Converts the star rating from text to a number (1–5)
- Fixes the site's broken character encoding so prices are clean (no mojibake)
- Polite: sets a User-Agent and waits between requests
- Graceful error handling — one failed page won't crash the run
- Command-line options for page limit, output path, and delay

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python scraper.py                      # scrape all pages -> books.csv
python scraper.py --pages 3            # first 3 pages only
python scraper.py --out my_books.csv   # custom output file
python scraper.py --delay 1.0          # slower, extra-polite
```

## How it works
1. Requests each catalogue page with `requests`
2. Parses the HTML with `BeautifulSoup`
3. Extracts each book's fields from its product card
4. Follows the **next** link until there are no more pages
5. Writes everything to CSV with Python's `csv` module

## Notes on ethics & legality
`books.toscrape.com` is a sandbox site made specifically for scraping practice.
For real client work I only scrape **publicly accessible** data and respect each
site's `robots.txt` and terms of service.

## Tech
Python · requests · BeautifulSoup

---
Built by **Obaid Mohammad Amin** — [github.com/obaid-amin](https://github.com/obaid-amin)
Available for scraping & automation work.

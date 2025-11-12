import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def read_urls(file_path):
    """Reads all URLs from urls.txt"""
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def scrape_page(url):
    """Fetch one page and extract data"""
    try:
        # Get HTML content
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # throws error if 404 etc.

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Get title
        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # Get meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

        # Create a short summary (you can make this smarter later)
        summary = f"This page titled '{title}' describes: {description[:100]}"

        return {
            "url": url,
            "title": title,
            "meta_description": description,
            "summary": summary,
            "fetch_time": datetime.utcnow().isoformat()
        }

    except Exception as e:
        # If any error (like network issue), return an empty record
        return {
            "url": url,
            "title": "",
            "meta_description": "",
            "summary": f"Error fetching page: {e}",
            "fetch_time": datetime.utcnow().isoformat()
        }

def main():
    urls = read_urls("urls.txt")
    results = []
    for url in urls:
        print(f"Fetching {url} ...")
        data = scrape_page(url)
        results.append(data)
        time.sleep(1)  # small delay so we don't overload sites

    # Save everything to a CSV file
    df = pd.DataFrame(results)
    df.to_csv("scrape_summary.csv", index=False)
    print("\n✅ Done! Data saved in scrape_summary.csv")

if __name__ == "__main__":
    main()
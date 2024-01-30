import requests
from bs4 import BeautifulSoup
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

def crawl_web(start_url, max_urls):

    # Initialize our variables which are the urls to crawl and a set of variables to keep only unique values
    urls_to_crawl = [start_url]
    crawled_urls = set()

    # Check robots.txt
    if not check_robots_txt(start_url):
        return []

    with open("crawled_webpages.txt", "w") as f:
        while len(crawled_urls) < max_urls and urls_to_crawl:
            # Get next URL to crawl
            url = urls_to_crawl.pop(0)

            # Skip URL if already crawled
            if url in crawled_urls:
                continue

            if check_robots_txt(url):
                try:
                    page = requests.get(url)
                    page.raise_for_status()  # Check for HTTP errors
                    soup = BeautifulSoup(page.content, "html.parser")
                except requests.RequestException:
                    continue

                # Extract links
                links = extract_links(soup)

                # Convert relative URLs to absolute URLs
                links = [urljoin(url, link) for link in links]

                urls_to_crawl.extend(links)

                # Add URL to crawled set
                crawled_urls.add(url)

                # Write URL to file
                f.write(url + "\n")

                # Wait for 5 seconds
                time.sleep(5)
            else:
                continue

    return list(crawled_urls)

def check_robots_txt(url):
    # Initialize robot parser
    rp = RobotFileParser()
    rp.set_url(urljoin(url, "/robots.txt"))
    rp.read()
    # Check if URL is allowed to be crawled
    return rp.can_fetch("*", url)

def extract_links(soup):
    links = [link.get("href") for link in soup.find_all("a") if link.get("href")]
    return links

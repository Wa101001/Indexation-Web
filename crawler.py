
import requests
from bs4 import BeautifulSoup
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen

# Global variable to store the last crawled domain and its crawl delay
last_crawled_domain = None
last_crawl_delay = None

def crawl_web(start_url, max_urls):
    global last_crawled_domain, last_crawl_delay

    # Initialize variables
    urls_to_crawl = [start_url]
    crawled_urls = set()

    with open("crawled_webpages.txt", "w") as f:
        while len(crawled_urls) < max_urls and urls_to_crawl:
            # Get next URL to crawl
            url = urls_to_crawl.pop(0)

            # Skip URL if already crawled
            if url in crawled_urls:
                continue

            # Extract domain from the current URL
            current_domain = urlparse(url).netloc

            # Check if the domain has changed since the last crawl
            if current_domain != last_crawled_domain:
                # If the domain has changed, update last_crawled_domain and last_crawl_delay
                last_crawled_domain = current_domain
                last_crawl_delay = None  # Reset last_crawl_delay

                # Check robots.txt for the new domain
                if not check_robots_txt(url):
                    continue

            try:
                # Check and respect crawl delay from robots.txt
                crawl_delay = get_crawl_delay(url)
                if crawl_delay is not None:
                    time.sleep(crawl_delay)
                else:
                    # If no crawl delay is specified, wait for 5 seconds
                    time.sleep(5)

                # Attempt to get sitemap URLs from robots.txt
                sitemap_urls = extract_urls_from_sitemap(url)
                urls_to_crawl.extend(sitemap_urls)

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

    return list(crawled_urls)

def get_crawl_delay(url):
    # Initialize robot parser
    rp = RobotFileParser()
    rp.set_url(urljoin(url, "/robots.txt"))
    rp.read()

    # Check if the current domain has a crawl delay specified
    if rp.crawl_delay("*") is not None:
        return rp.crawl_delay("*")
    else:
        return None
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
def extract_urls_from_sitemap(url):
    rp = RobotFileParser()
    rp.set_url(urljoin(url, "/robots.txt"))

    try:
        rp.read()
        sitemaps = rp.site_maps()
        url_from_site_map = []

        for sitemap in sitemaps:
            response = urlopen(sitemap)
            soup = BeautifulSoup(response, 'lxml', from_encoding=response.info().get_param('charset'))
            urls = soup.find_all("url")

            for url in urls:
                loc = url.findNext("loc").text
                url_from_site_map.append(loc)

        return url_from_site_map

    except Exception as e:
        print(f"Error extracting URLs from sitemap: {e}")
        return []



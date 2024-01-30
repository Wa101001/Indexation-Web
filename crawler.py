import requests
from bs4 import BeautifulSoup
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor


# Global variables to store the last crawled domain and its crawl delay
last_crawled_domain = None
last_crawl_delay = None

def crawl_web(start_url, max_urls, max_workers=5):
    global last_crawled_domain, last_crawl_delay

    # Initialize variables
    urls_to_crawl = [start_url]
    crawled_urls = set()

    with open("crawled_webpages.txt", "w") as f:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
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

                # Submit the crawling task to the ThreadPoolExecutor
                future = executor.submit(crawl_url, url, f)

                # Attempt to get sitemap URLs from robots.txt
                sitemap_urls = extract_urls_from_sitemap(url)
                urls_to_crawl.extend(sitemap_urls)

                # Extract links asynchronously and add them to the URL queue
                link_futures = [executor.submit(extract_links_from_url, link) for link in sitemap_urls]

                # Wait for all link extraction tasks to complete
                for link_future in link_futures:
                    links = link_future.result()
                    urls_to_crawl.extend(links)

                # Add URL to crawled set
                crawled_urls.add(url)

                # Wait for the crawling task to complete
                future.result()

    return list(crawled_urls)

def crawl_url(url, file_handle):
    try:
        # Check and respect crawl delay from robots.txt
        crawl_delay = get_crawl_delay(url)
        if crawl_delay is not None:
            time.sleep(crawl_delay)
        else:
            # If no crawl delay is specified, wait for 5 seconds
            time.sleep(5)

        page = requests.get(url)
        page.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract links
        links = extract_links(soup)

        # Convert relative URLs to absolute URLs
        links = [urljoin(url, link) for link in links]

        # Write URL to file
        file_handle.write(url + "\n")

    except requests.RequestException:
        pass

    
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

def extract_links_from_url(url):
    try:
        page = requests.get(url)
        page.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract links
        links = extract_links(soup)

        # Convert relative URLs to absolute URLs
        links = [urljoin(url, link) for link in links]

        return links

    except requests.RequestException:
        return []

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



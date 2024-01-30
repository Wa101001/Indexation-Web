import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from collections import deque
import threading
import time

class WebCrawler:
    # Constructor: initializes the crawler with the start URL, max URLs to crawl and max worker threads
    def __init__(self, start_url, max_urls, max_workers=10):
        self.start_url = start_url
        self.max_urls = max_urls
        self.max_workers = max_workers
        self.urls_to_crawl = deque([start_url])  # Queue of URLs to crawl
        self.crawled_urls = set()  # Set of crawled URLs to avoid duplication
        self.last_crawled_domain = None  # Tracks the domain of the last crawled URL
        self.last_crawl_delay = None  # Stores delay as mentioed by the robots.txt of the current domain
        self.lock = threading.Lock()  # Lock for threadsafe writing to the file 

    # Main method to start crawling process
    def crawl_web(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while len(self.crawled_urls) < self.max_urls and self.urls_to_crawl:
                url = self.urls_to_crawl.popleft()

                if url in self.crawled_urls:
                    continue  # Skip the URL if it's already crawled

                current_domain = urlparse(url).netloc

                # Check if domain changed and update crawl delay
                if current_domain != self.last_crawled_domain:
                    self.last_crawled_domain = current_domain
                    self.last_crawl_delay = self.get_crawl_delay(url)

                    # Skip URL if not allowed by robots.txt
                    if not self.check_robots_txt(url):
                        continue

                # Execute crawl_url in a separate thread
                future = executor.submit(self.crawl_url, url)

                try:
                    # Extract and queue URLs from the sitemap
                    sitemap_urls = self.extract_urls_from_sitemap(url)
                    self.urls_to_crawl.extend(sitemap_urls)
                except Exception as e:
                    print(f"Error extracting URLs from sitemap: {e}")

        return self.crawled_urls

    # Method to crawl a single URL
    def crawl_url(self, url):
        delay = self.last_crawl_delay if self.last_crawl_delay is not None else 3 # Delay = 3 if the robot.txt doesn't specify
        time.sleep(delay)  # Respect crawl delay

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            links = self.extract_links(soup)
            links = [urljoin(url, link) for link in links]

            # Thread-safe writing to the file
            with self.lock:
                self.crawled_urls.add(url)
                with open("crawled_webpages.txt", "a") as f:
                    f.write(url + "\n")

            return links
        except requests.RequestException:
            return []

    # Extract a maximum of 5 links from each soup object 
    def extract_links(self, soup):
        links = [link.get("href") for link in soup.find_all("a", limit=5) if link.get("href")]
        return links

    # Get the crawl delay from robots.txt
    def get_crawl_delay(self, url):
        rp = RobotFileParser()
        rp.set_url(urljoin(url, "/robots.txt"))
        rp.read()

        delay = rp.crawl_delay("*")
        return delay if delay is not None else 3

    # Check if crawling is allowed by robots.txt
    def check_robots_txt(self, url):
        rp = RobotFileParser()
        rp.set_url(urljoin(url, "/robots.txt"))
        rp.read()
        return rp.can_fetch("*", url)

    # Extract URLs from the sitemap
    def extract_urls_from_sitemap(self, url):
        rp = RobotFileParser()
        rp.set_url(urljoin(url, "/robots.txt"))
        rp.read()
        sitemaps = rp.site_maps()

        url_from_site_map = []

        for sitemap in sitemaps:
            response = requests.get(sitemap)
            soup = BeautifulSoup(response.content, 'lxml')
            urls = soup.find_all("url")

            for url in urls:
                loc = url.findNext("loc").text
                url_from_site_map.append(loc)

        return url_from_site_map

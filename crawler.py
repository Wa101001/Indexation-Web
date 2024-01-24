# crawler.py
from crawl_delay import check_robots_txt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import time
import xml.etree.ElementTree as ET

def extract_links(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        html_content = response.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('https://')]
        return links
    except Exception as e:
        print(f'Error accessing {url}: {e}')
        return []

def extract_links_from_sitemap(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        xml_content = response.read()
        root = ET.fromstring(xml_content)

        links = [loc.text for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        return links
    except Exception as e:
        print(f'Error accessing {url}: {e}')
        return []


def write_to_file(urls):
    with open('crawled_webpages.txt', 'a') as file:
        for url in urls:
            file.write(url + '\n')

# Import the check_robots_txt function
from crawl_delay import check_robots_txt

def crawl_website(start_url, max_urls=100, max_links_per_page=10):
    explored_urls = set()
    to_explore_urls = [start_url]

    # Extract links from sitemap.xml if available
    sitemap_url = start_url.rstrip('/') + '/sitemap.xml'
    sitemap_links = extract_links_from_sitemap(sitemap_url)
    to_explore_urls.extend(sitemap_links)

    while len(explored_urls) < max_urls and to_explore_urls:
        current_url = to_explore_urls.pop(0)

        # Skip if the URL has already been explored
        if current_url in explored_urls:
            continue

        # Check if the site allows crawling based on robots.txt
        crawl_delay = check_robots_txt(current_url)

        # If crawl_delay is None, set it to 5 seconds
        crawl_delay = crawl_delay if crawl_delay is not None else 5

        print(f"Crawling {current_url} with a delay of {crawl_delay} seconds")
        time.sleep(crawl_delay)

        links_on_page = extract_links(current_url)[:max_links_per_page]

        for link in links_on_page:
            if link not in explored_urls and link not in to_explore_urls:
                to_explore_urls.append(link)

        explored_urls.add(current_url)

        time.sleep(5)

    write_to_file(explored_urls)

    print(f'Exploration terminée. {len(explored_urls)} URLs ont été trouvées et téléchargées.')

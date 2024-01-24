# crawler.py
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

def crawl_website(start_url, max_urls=50, max_links_per_page=5):
    explored_urls = set()  # Use a set to store unique URLs
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

        links_on_page = extract_links(current_url)[:max_links_per_page]

        for link in links_on_page:
            if link not in explored_urls and link not in to_explore_urls:
                to_explore_urls.append(link)

        # Add the current URL to the set of explored URLs
        explored_urls.add(current_url)

        # Wait for at least five seconds before making the next request
        time.sleep(5)

    # Write unique URLs to the file
    write_to_file(explored_urls)

    print(f'Exploration terminée. {len(explored_urls)} URLs ont été trouvées et téléchargées.')

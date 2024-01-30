import click
from urllib.parse import urlparse
from crawler import WebCrawler

@click.command()
# Define command-line interface using click
@click.option('--url', prompt='Enter the starting URL e.g: https://www.ensai.fr', help='The starting URL for the crawler.')
@click.option('--max-urls', default=50, help='Maximum number of URLs to crawl.', show_default=True)
def main(url, max_urls):
    # Main function to run the crawler
    if not is_valid_url(url):
        # Validate the input URL
        print("Error: Invalid URL. Please enter a valid URL starting with 'http://' or 'https://'")
        return

    # Initialize the WebCrawler with the specified URL and max URLs
    crawler = WebCrawler(start_url=url, max_urls=max_urls)
    # Start the crawling process and store the crawled URLs
    crawled_urls = crawler.crawl_web()

    # Output the results
    if not crawled_urls:
        print(f"No URLs crawled from {url}")
    else:
        print(f"Crawled URLs:\n{crawled_urls}")

def is_valid_url(url):
    # Function to validate the given URL
    try:
        result = urlparse(url)
        # Check if URL has both scheme (like http) and netloc (like www.example.com)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

if __name__ == '__main__':
    # Run the main function when the script is executed
    main()

import crawler
import click

@click.command()
def main():
    # Ask the user for an URL
    start_url = click.prompt("Enter the starting URL (must start with 'https://' e.g 'https://www.ensai.Fr'): ", type=str)

    # Check if the URL is in the correct format or if the URL is of a valid website :)
    if not start_url.startswith("https://") or not crawler.check_robots_txt(start_url):
        print("Error: Invalid URL or URL not allowed by robots.txt")
        return

    max_urls = 50
    crawled_urls = crawler.crawl_web(start_url, max_urls)

    if not crawled_urls:
        print(f"No URLs crawled from {start_url}")
    else:
        print(f"Crawled URLs:\n{crawled_urls}")

if __name__ == '__main__':
    main()

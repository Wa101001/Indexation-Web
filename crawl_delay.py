import requests
from urllib.parse import urljoin

def get_robots_txt_url(base_url):
    return urljoin(base_url, '/robots.txt')

def parse_robots_txt(robots_txt_content):
    # Parse the robots.txt content to extract crawl delay
    # Note: This is a simple example and may not cover all cases
    lines = robots_txt_content.split('\n')
    for line in lines:
        if line.lower().startswith('crawl-delay'):
            return int(line.split(':')[-1].strip())
    return None

def check_robots_txt(base_url):
    robots_txt_url = get_robots_txt_url(base_url)

    try:
        # Make a request to the robots.txt file
        response = requests.get(robots_txt_url)

        # Check if the request was successful
        if response.status_code == 200:
            crawl_delay = parse_robots_txt(response.text)
            return crawl_delay
        else:
            print(f"Failed to fetch robots.txt for {base_url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

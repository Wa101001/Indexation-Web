# Crawler

## Overview
"Crawler" is a Python-based web crawler application designed as an academic project for final year engineering students at ENSAI. Developed by Wajih Hammouda (GitHub: [Wa101001](https://github.com/Wa101001)), this project demonstrates the principles of web crawling, multi-threaded processing and compliance with website crawling policies.

## Features
- **Multi-threaded Web Crawling:** Efficiently crawls websites using multiple threads to speed up the process.
- **Robots.txt Compliance:** Respects the rules set in the robots.txt file of each website to ensure ethical scraping practices.
- **URL Management:** Manages a queue of URLs to crawl and keeps track of already crawled URLs to avoid duplication.
- **Command-Line Interface:** Easy to use CLI for initiating the crawl process with customizable parameters.

## Installation
To use this crawler, you need to have Python installed on your system. Clone the repository and install the required dependencies.

```bash
git clone https://github.com/Wa101001/Indexation-Web.git
cd Indexation-Web
pip install requests beautifulsoup4 urllib3 click
```

## Usage
Run `main.py` with the starting URL and the maximum number of URLs to crawl. For example:

```bash
python main.py --url TP1_crawler https://www.ensai.fr --max-urls 50
```


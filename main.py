# main.py
from crawler import crawl_website

def main():
    start_url = input("Enter the URL of the site you want to crawl (e.g., https://ensai.fr/): ")
    crawl_website(start_url)

if __name__ == "__main__":
    main()

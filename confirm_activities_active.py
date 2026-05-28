# Check if webpage has the download pdf or download activity button

import requests
from bs4 import BeautifulSoup

def check_download_word(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for specific <span> content
        for span in soup.find_all('span'):
            text = span.get_text(strip=True)
            if text in {"Download PDF", "Download Activity"}:
                return True

        return False

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return False

def main():
    input_file = 'Downloads/activityLinks.txt' 
    try:
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return

    for url in urls:
        has_download = check_download_word(url)
        if not has_download:
            print(f"{url}")

if __name__ == "__main__":
    main()

import requests
import re
import html
from bs4 import BeautifulSoup

# Load URLs from a file
def load_urls(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Setup session
session = requests.Session()
session.cookies.set('sessionid', 'choc-chip-cookie', domain='domain.tld')

# Extract and parse body section classes
def extract_classes_from_url(url):
    print(f"Fetching {url}")
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []

    html_text = response.text

    # Get <escape> block between <b>body:</b> and <b>outro:</b>
    match = re.search(r'<b>body:</b>\s*<escape>(.*?)</escape>.*?<b>outro:</b>', html_text, re.DOTALL | re.IGNORECASE)
    if not match:
        print(f"No body section found in {url}")
        return []

    unescaped_body = html.unescape(match.group(1))

    soup = BeautifulSoup(unescaped_body, 'html.parser')

    classes = []
    fullClasses = []
    for tag in soup.find_all(class_=True):
        classes.extend(tag.get("class", []))
        if tag.has_attr("class"):
            fullClasses.append(f'class="{" ".join(tag["class"])}"')


    return classes, fullClasses


# Main logic
if __name__ == "__main__":
    allTags = []

    urls = load_urls('Downloads/urls.txt')

    for url in urls:
        classes, fullClasses = extract_classes_from_url(url)

        allTags.extend(classes)

        with open("Downloads/classes.txt", "a") as file:    
            for aClass in fullClasses:
                file.write(f"{aClass}\n")
        with open("Downloads/dupeTags.txt", "a") as file:
            for aTag in classes:
                file.write(f"{aTag}\n")

    allTags = list(dict.fromkeys(allTags))
    with open("Downloads/tags.txt", "a") as file:
        for individTag in allTags:
            file.write(f"{individTag}\n")
    

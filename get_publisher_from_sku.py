import requests
import re

publisherList = []

with open("skuLinks.txt", "r") as inputFile:
    skuLinks = [line.strip() for line in inputFile if line.strip()]

# Set up session
session = requests.Session()
session.cookies.set('sessionid', 'pump-cheesecake-cookie', domain='domain.tld')

for link in skuLinks:
    # Step 1: Get raw HTML
    response = session.get(link)
    html = response.text

    # Step 2: Extract product number with regex
    match = re.search(r'<b>product:</b>\s*<escape>(\d+)</escape>', html)
    if match:
        product_number = match.group(1)
        product_url = f'https://domain.tld/internal/product/product/{product_number}/change/'
    else:
        publisherList.append(link+" Product Number not found.")
        continue

    response = session.get(product_url)
    html = response.text

    # Step 3: Extract slug
    slug_match = re.search(r'<b>slug:</b>\s*<escape>(.*?)</escape>', html)
    if slug_match:
        slug = slug_match.group(1)
    else:
        print("Slug not found.")

    # Step 4: Visit public product page
    public_url = f'https://domain.tld/store/product/{slug}/'
    response = session.get(public_url)
    html = response.text

    # Step 5: Extract Publisher
    publisher_match = re.search(
        r'<li[^>]*><b[^>]*>Publisher:</b>\s*(.*?)\s*(?=<li|</ul>)',
        html,
        re.IGNORECASE | re.DOTALL
    )

    if publisher_match:
        publisher_raw = publisher_match.group(1)
        # Strip HTML tags inside captured group, if any
        publisher_clean = re.sub(r'<.*?>', '', publisher_raw).strip()
        print("Publisher:", publisher_clean)
        publisherList.append(publisher_clean)
    else:
        publisherList.append(public_url + "Publisher not found")

with open("pubilsherList.txt", "w") as outputFile:
    for pub in publisherList:
        outputFile.write(pub + "\n")

print("Done :)")
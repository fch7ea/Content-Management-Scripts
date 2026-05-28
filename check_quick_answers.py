# Check quick answers to see if they work - for aig site, ignores drafts

import requests
import re
import html
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# List for ones that need manual checking
notQuick = []
review = []
myNodeLinks = []
myTerms = []

# Get all the answer links to use - each line of the txt that isn't empty after stripping
with open("answerLinks.txt", "r") as inputFile:
    answerLinks = [line.strip() for line in inputFile if line.strip()]

# Set up session
session = requests.Session()
session.cookies.set('sessionid', 'cookie', domain='domain.tld')

# For each link
for link in answerLinks:

    # Get the html page
    response = session.get(link)
    if response.status_code != 200:
        print(f"Failed to fetch {link}")
        continue
    htmlText = response.text

    # Get all the search terms
    match = re.search(r'<b>searches:</b>\s*<escape>(.*?)</escape>.*?<b>content:</b>', htmlText, re.DOTALL | re.IGNORECASE)
    if not match:
        print(f"No searches found in {link}")
        continue
    rawTerms = html.unescape(match.group(1))
    searchTerms = [term.strip() for term in rawTerms.splitlines() if term.strip()]

    # Run each search term
    for term in searchTerms:
        newTerm = quote_plus(term)
        query = requests.get("https://domain/search/?q="+newTerm)
        queryText = query.text

        # Message so it looks cool
        print("Running https://domain/search/?q="+newTerm)

        # Check if there is a quick answer
        soup = BeautifulSoup(queryText, 'html.parser')
        quick_answers = soup.find_all("li", attrs={"data-category": "search-quick-answer"})

        # If there isn't a quick answer in the page source
        if not quick_answers:
            notQuick.append(link + ": " + term)
            myTerms.append(term)
            myNodeLinks.append(link)
            review.append("https://domain/search/?q="+newTerm)

myNodeLinks = list(dict.fromkeys(myNodeLinks))
# Write not quick answers in a file
for filename, items in [("reviewTheseAnswers.txt", review), ("brokenSearches.txt", notQuick), ("myTerms.txt", myTerms), ("nodeLinks.txt", myNodeLinks)]:
    with open(filename, "w") as f:
        f.writelines(item + "\n" for item in items)


# Print completion message
print("Done ;:")
###
# NOTE: No CSRF tokens or session cookies should EVER be made publicly available, 
# including pushing to a GitHub repository
# In fact, storing them as environment variables would be better.
###

import requests
from bs4 import BeautifulSoup

# Set up session to preserve cookies
session = requests.Session()

# STEP 1: GET the form page to get cookies + CSRF token
url = "link to create a new snippet"
response = session.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Get CSRF token from hidden input
csrf_token = soup.find("input", {"name": "csrf-middleware-token"})["value"]

englishPhrases = []
spanishPhrases = []
snippetLinks = []

with open("englishSnippets.txt", "r", encoding="utf-8") as englishFile:
    englishPhrases = [line.strip() for line in englishFile if line.strip()]
    englishPhrases = list(dict.fromkeys(englishPhrases))

with open("spanishSnippets.txt", "r", encoding="utf-8") as spanishFile:
    spanishPhrases = [line.strip() for line in spanishFile if line.strip()]
    spanishPhrases = list(dict.fromkeys(spanishPhrases))

for i in range(len(englishPhrases)):
    english = englishPhrases[i]
    spanish = spanishPhrases[i]

    # Replace with actual session cookie and CSRF token
    cookies = {
        "sessionid": "snckrddl-cookie",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": url,
    }

    data = {
        "csrfmiddlewaretoken": csrf_token,
        "name": english,
        "location": "",
        "count": "0",
        "snippettranslation_set-TOTAL_FORMS": "3",
        "snippettranslation_set-INITIAL_FORMS": "0",
        "snippettranslation_set-MIN_NUM_FORMS": "0",
        "snippettranslation_set-MAX_NUM_FORMS": "1000",
        "snippettranslation_set-0-id": "",
        "snippettranslation_set-0-snippet": "",
        "snippettranslation_set-0-language": "1",
        "snippettranslation_set-0-office": "",
        "snippettranslation_set-0-text": english,
        "snippettranslation_set-1-id": "",
        "snippettranslation_set-1-snippet": "",
        "snippettranslation_set-1-language": "2",
        "snippettranslation_set-1-office": "",
        "snippettranslation_set-1-text": spanish,
        "_continue": "Save and continue editing"
    }

    response = session.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)

    if response.status_code == 302:
        new_url = response.headers.get("Location")
        snippetLinks.append("root URL" + new_url)
    else:
        print("Something went wrong!")
        print(english)
        print("Status Code:", response.status_code)
        print(response.text[:500])
        break

with open("snippetLinks.txt", "w", encoding="utf-8") as outputFile:
    for link in snippetLinks:
        outputFile.write(link + "\n")

print("Done :)")




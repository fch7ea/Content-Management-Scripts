# Content Management Scripts

A collection of scripts written during a web content development internship, covering Django template tag generation, web scraping, and automated quality testing. Sensitive information (session cookies, domain names, and internal URLs) has been sanitized. See below for descriptions regarding each file's use cases.

---

## Scripts

### `check_quick_answers.py`
Takes a list of internal quick answer (search results similar to an overview result in a search engine) URLs, extracts the search terms for that quick answer, and checks whether each term surfaces a quick answer on the live site. Outputs flagged terms and links for manual review.

---

### `confirm_activities_active.py`
Scrapes a list of URLs and flags any that are missing a **Download PDF** or **Download Activity** button.

---

### `identify_classes.py`
Fetches internal content pages and extracts all CSS classes from the body section. Outputs three text files for full class names (ex. class="foo bar"), all individual class names (ex. foo), and deduplicated individual class names.

---

### `get_publisher_from_sku.py`
Given a list of internal product links based on SKUs, this script completes the following steps:
1. Extracts the product number using regex from the HTML of that page
2. Uses the product number to construct a link to the internal product page
3. Extracts the slug of the public product page URL from the HTML
4. Uses the slug to construct the link for and visit the public-facing product page
5. Extracts the publisher name from the HTML of that page
6. Writes all publisher names to a text file

---

### `create_translation_snippet.py`
Reads paired English/Spanish phrases from two text files and programmatically submits them as translation snippets via a Django admin web form. Outputs the resulting snippet URLs to a file.

---

### `format_footnote_tags.py`
Takes a pasted block of footnotes as a single line and formats each one into Django template tags, writing the result to a file.

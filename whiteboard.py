# sample whiteboard file for first commit 

# beautifulsoup testing

import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com"
resp = requests.get(url)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "lxml")
print(soup.title.string)

for q in soup.select(".quote .text"):
    print(q.get_text(strip=True))

    
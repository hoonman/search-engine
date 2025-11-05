# Search Engine

## Tokenizer
Responsible for taking a sample file (HTML, PDF, docx, etc), parse it, and produce a frequency map of all the tokens. 
First, we unicode-normalize the token using NFKC form by default. If stripping accents is required by the user, we will use NFKD to decompose, strip the accents and recompose again.
We then use casefold to lowercase the token so that it covers for other language types.
Finally, we will filter out any punctuations that remain at the start or end of a token. 

## Crawler
Manages and orchestrates the Frontier and Worker threads. Called from launch.py and reads config.ini. This config is later used in other parts of the app as well. Main part: Frontier, Worker 

### Frontier
Manages the URLs in the to_be_downloaded list.
* persists state using shelve so when user exits out of the crawling process, we can recover the state using shelve file
* tracks completion status of each url
* restart and resume logic
    * restart: delete save file and start from seed URLs
    * resume: load incomplete URLs from shelve file
* provide thread-safe operations. more on this later.

### Worker
main functionality:
1. get URL from frontier
2. download pages via direct_download(). we don't want to use the cache server because they might be down.
3. pass response to Scraper
4. add discovered URLs back to Frontier
5. mark URL as complete when done
6. respects politeness delay from RobotsParser

## Scraper
Pop the latest link from our frontier (stack), extract valid links, and add new ones to our frontier. Initially, we have four main seed URLs all being ICS web pages. We pop one of these and find new ones to extract links from anchor tags using BeautifulSoup. For each of the extracted links we must validate with the following methods: 
1. Defragmented link
2. Check uniqueness
3. Must have a valid schema / valid URL structure
4. Must not contain any disallowed extensions (ex. pdf, png, img, mp4, etc)
5. The content of the new page must not be over 90% similar than any of the web pages we have encountered
6. Must contain valid domain (A2 requirement)
7. Respect disallowed sites with robots.txt
8. Filter out exact and similar pages 
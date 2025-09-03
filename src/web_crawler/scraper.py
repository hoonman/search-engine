import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit

class Scraper:
    def __init__(self, config):
        self.unique_links = set()
        self.unfragmented_links = set()
        self.config = config # we can use this for similarity threshold later.
    
    def scraper(self, url, resp):
        links = self.extract_next_links(url, resp)
        return [link for link in links if self.is_valid(link)]

    def extract_next_links(self, url, resp):
        extracted_links = set()
        if resp.status != 200:
            return []

        if resp.raw_response and resp.raw_response['content']:
            soup = BeautifulSoup(resp.raw_response['content'], "lxml") # uses lxml parser
            for link in soup.find_all('a'):
                parsed_url = link.get('href')
                joined_url = urljoin(url, parsed_url)
                extracted_links.add(joined_url)
                self.extract_unfragmented_links(joined_url)
        extracted_links.difference_update(self.unique_links)
        self.unique_links = self.unique_links | extracted_links
        return extracted_links

    def is_valid(self, url):
        # Decide whether to crawl this url or not. 
        # If you decide to crawl it, return True; otherwise return False.
        # There are already some conditions that return False.
        try:
            parsed = urlparse(url)
            if parsed.scheme not in set(["http", "https"]):
                return False
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

        except TypeError:
            print ("TypeError for ", parsed)
            raise

    # the below functions are for the actual report
    def extract_unfragmented_links(self, url):
        parts = urlsplit(url)
        unfragmented_url = urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
        if unfragmented_url not in self.unfragmented_links:
            self.unfragmented_links.add(unfragmented_url)









def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    '''
    given the url, and the response, we must first parse the raw_response and retrieve any hyperlinks.
    since hyperlinks are usually in anchor tags, if we see any <a> tags we will parse. 
    <a href="http://www.google.com"></a>

    use resp.raw_response.content to parse content. should we also retreive URLs that are not part of anchor tags? they are not hyperlinks though.

    why do we need the urL? 

    1. parse the web content with a library like beautifulsoup 
    2. extract all the links from <a> tags
    
    '''
    links = []
    if resp.status != 200:
        return []

    if resp.raw_response and resp.raw_response['content']:
        soup = BeautifulSoup(resp.raw_response['content'], "lxml") # uses lxml parser
        for link in soup.find_all('a'):
            parsed_url = link.get('href')
            joined_url = urljoin(url, parsed_url)
            print("joined url: ", joined_url)
            links.append(joined_url)
    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

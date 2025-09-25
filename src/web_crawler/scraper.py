import re
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser
from utils import get_logger

class Scraper:
    def __init__(self, config):
        self.logger = get_logger(f"Scraper", "SCRAPER")
        self.unique_links = set()
        self.defragmented_links = set()
        self.config = config # we can use this for similarity threshold later.
        self.start_time = time.time()
        self.subdomains = {}
        self.robot_parser = RobotFileParser()
        self.robots_cache = {}
        self.robots_delay = {}
        self.agent_name = "ICSCrawler"

        # similarity url tracking

    def scraper(self, url, resp):
        self.unique_links.add(url)

        try:
            extracted_links = self.extract_next_links(url, resp)
            valid_links = []
            for link in extracted_links:
                if self.is_valid(link) and (link not in self.unique_links):
                    self.unique_links.add(link)
                    defrag_link = self.defragment_link(link)
                    valid_links.append(defrag_link)
            self.logger.info(f"Found {len(valid_links)} new valid links from {url}")
            return valid_links
        except Exception as e:
            self.logger.error(f"Exception in scraper for URL {url}: {str(e)}")
            self.append_to_json_file('crawler_report_error.json', 
                {
                    "error": f"An exception ocurred while running the crawler. Crawler did not finish successfully. Exception: {str(e)}.",
                    "last_url": url,
                    "timestamp": time.time()
                })

    def extract_next_links(self, url, resp):
        extracted_links = set()
        if resp.status != 200:
            return []

        if resp.raw_response and resp.raw_response['content']:
            soup = BeautifulSoup(resp.raw_response['content'], "lxml")
            for link in soup.find_all('a'):
                joined_url = urljoin(url, link.get('href'))
                extracted_links.add(joined_url)
        extracted_links.difference_update(self.unique_links) # from extracted links remove all links that exist already in unique links
        return extracted_links

    def is_valid(self, url):
        try:
            parsed = urlparse(url)
            if parsed.scheme not in set(["http", "https"]):
                return False
                
            robots_parser = self.get_robots_parser(url, parsed)
            self.check_robots_delay(url, parsed)
            if robots_parser and not robots_parser.can_fetch(self.agent_name, url):
                self.logger.debug(f"Robots.txt disallows crawling: {url}")
                return False
                
            if not self.filter_valid_domains(url, parsed):
                return False

            disallowed_extensions = (r".*\.(css|js|bmp|gif|jpe?g|ico|img|apk|sql|webp|svg|json|xml|woff2?|tsx?|jsx|ya?ml" 
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$")

            if re.match(disallowed_extensions, parsed.path.lower()) or re.match(disallowed_extensions, parsed.query.lower()):
                return False
            return True
        except TypeError:
            self.logger.info("TypeError for ", parsed)
            raise

    def defragment_link(self, url):
        parts = urlsplit(url)
        defragmented_url = urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
        if defragmented_url not in self.defragmented_links:
            self.defragmented_links.add(defragmented_url)
        return defragmented_url
        

    def filter_valid_domains(self, url, parsed):
        '''
        given the url itself, urlparse object parsed, determine if the url contains valid domain.
        method: break down the url since we have a urlparse object and see if that broken down url matches one of the valid ones we have
        returns: boolean if the given url is valid or not
        '''
        allowed_suffixes = tuple("." + d for d in self.config.valid_domains)
        try:
            host = parsed.hostname 
            if not host: 
                return False
            host = host.rstrip(".").lower()
            result = (host in self.config.valid_domains) or host.endswith(allowed_suffixes)
            if result:
                self.is_subdomain('ics.uci.edu', host, parsed)
            return result
        except Exception as e:
            self.logger.info(f"an exception occured in filter valid domains function: {str(e)}")
            return False

    def is_subdomain(self, domain, filtered_host, parsed_url):
        if filtered_host == domain or (filtered_host == ("." + domain)):
            scheme_hostname = parsed_url.scheme + "://" + parsed_url.hostname
            if domain in self.subdomains:
                self.subdomains[scheme_hostname] += 1
            else:
                self.subdomains[scheme_hostname] = 1

    def get_robots_parser(self, url, parsed):
        '''
        takes url that we are validating, parsed object from urlparse and returns a robots parser using RobotFileParser
        '''
        try:
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            if robots_url in self.robots_cache:
                return self.robots_cache[robots_url]

            rp = RobotFileParser()
            rp.set_url(robots_url)
            return self.load_robots_parser(rp, robots_url)
        except Exception as e:
            self.logger.error(f"Error creating robots parser for {url}: {e}")
            return None

    def load_robots_parser(self, rp, robots_url):
        try:
            rp.read()
            self.robots_cache[robots_url] = rp
            return rp
        except Exception as e:
            self.logger.warning(f"could not read robots.txt from {robots_url}: {e}")
            fallback_rp = RobotFileParser()
            fallback_rp.set_url(robots_url)
            self.robots_cache[robots_url] = fallback_rp
            return fallback_rp

    def check_robots_delay(self, url, parsed):
        rp = self.get_robots_parser(url, parsed)
        if rp:
            delay = rp.crawl_delay(self.agent_name)
            if delay:
                self.robots_delay[url] = delay

    def get_robots_delay(self, url):
        if url in self.robots_delay:
            return self.robots_delay[url]
        return self.config.time_delay

    def normalize_url(self):
        pass

    def append_to_json_file(self, filename, data):
        try:
            with open('report/' + filename, 'r') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        except FileNotFoundError:
            existing_data = []
        
        existing_data.append(data)
        
        with open('report/' + filename, 'w') as f:
            json.dump(existing_data, f, indent=2)

    def report(self, finish_reason):
        '''
        reports back important information such as time elapsed, count of urls, longest pages, etc
        '''
        end_time = time.time()
        total_time = end_time - self.start_time
        report_data = {
            "unique_link_count": len(list(self.defragmented_links)),
            "time_elapsed": total_time,
            "subdomain_counts": self.subdomains,
            "finish_reason": finish_reason
        }
        print(f"Time elapsed: {total_time:.4f} seconds")
        self.append_to_json_file('crawler_report.json', report_data)
        pass

    # comments regarding response object for the resp obj param
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
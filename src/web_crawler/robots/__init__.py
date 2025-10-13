from urllib.robotparser import RobotFileParser
from utils import get_logger

class RobotsParser:
    def __init__(self, agent_name, config):
        self.logger = get_logger(f"Robots", "ROBOTS")
        self.robots_parser = RobotFileParser()
        self.robots_cache = {}
        self.robots_delay = {}
        self.agent_name = agent_name
        self.config = config
        pass

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

    def can_fetch(self, agent_name, url):
        return self.robots_parser.can_fetch(agent_name, url)


    def check_robots(self, url, parsed):
        '''get the robot parser, check robot delay, and finally check if we can fetch using robots'''
        robots_parser = self.get_robots_parser(url, parsed)
        self.check_robots_delay(url, parsed)
        if robots_parser and not robots_parser.can_fetch(self.agent_name, url):
            self.logger.debug(f"Robots.txt disallows crawling: {url}")
            return False
        return True

import re


class Config(object):
    def __init__(self, config):
        self.user_agent = config["IDENTIFICATION"]["USERAGENT"].strip()
        print (self.user_agent)
        assert self.user_agent != "DEFAULT AGENT", "Set useragent in config.ini"
        assert re.match(r"^[a-zA-Z0-9_ ,]+$", self.user_agent), "User agent should not have any special characters outside '_', ',' and 'space'"
        self.threads_count = int(config["LOCAL PROPERTIES"]["THREADCOUNT"])
        self.save_file = config["LOCAL PROPERTIES"]["SAVE"]

        self.host = config["CONNECTION"]["HOST"]
        self.port = int(config["CONNECTION"]["PORT"])

        self.seed_urls = config["CRAWLER"]["SEEDURL"].split(",")
        self.valid_domains = set(config["CRAWLER"]["VALID_DOMAINS"].split(","))
        self.time_delay = float(config["CRAWLER"]["POLITENESS"])

        self.cache_server = None
        self.page_threshold = int(config["CRAWLER"]["PAGE_THRESHOLD"])
        if self.page_threshold == -1:
            self.page_threshold = float('inf')
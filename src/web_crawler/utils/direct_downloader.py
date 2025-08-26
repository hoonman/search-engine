import requests
import time
import random
from utils.response import Response
from urllib.parse import urlparse

domain_last_accessed = {}

def direct_download(url, config):
    '''Downloads content directly from the web without using cache server'''
    domain = urlparse(url).netloc

    if domain in domain_last_accessed:
        elapsed = time.time() - domain_last_accessed[domain]
        if elapsed < config.time_delay:
            time.sleep(config.time_delay - elapsed + random.uniform(0, 0.1))

    domain_last_accessed[domain] = time.time()

    try:
        headers = {
            'User-Agent': config.user_agent
        }
        raw_response = requests.get(url, headers=headers, timeout=5)
        return Response(url, raw_response.status_code, "", raw_response)
    except Exception as e:
        return Response(url, 400, str(e), None)
        

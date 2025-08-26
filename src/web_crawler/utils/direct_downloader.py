import requests
import time
import random
from utils.response import Response
from urllib.parse import urlparse

domain_last_accessed = {}
global_request_count = 0
MAX_REQUESTS = 200

def direct_download(url, config):
    '''Downloads content directly from the web without using cache server'''
    global global_request_count
    domain = urlparse(url).netloc

    if global_request_count >= MAX_REQUESTS:
        return Response({
            "url": url,
            "status": 429,
            "error": "Max pages limit reached",
        })
    global_request_count += 1

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
        
        # Create a response dictionary similar to what the cache server would return
        response_data = {
            "url": url,
            "status": raw_response.status_code,
            "error": "",
            "content": raw_response.content,
            "raw_content": raw_response.content,
            "headers": dict(raw_response.headers)
        }
        return Response(response_data)
    except Exception as e:
        error_data = {
            "url": url,
            "status": 400,
            "error": str(e),
            "content": None,
            "raw_content": None,
            "headers": {}
        }
        return Response(error_data)
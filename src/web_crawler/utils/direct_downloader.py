import requests
import time
import random
import pickle
from utils.response import Response
from urllib.parse import urlparse

def direct_download(url, config):
    '''Downloads content directly from the web without using cache server'''
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
            "raw_response": {
                "url": url,
                "content": raw_response.content
            },
        }
        return Response(response_data)
    except Exception as e:
        error_data = {
            "url": url,
            "status": 400,
            "error": str(e),
            "raw_response": {
                "url": url,
                "content": b""
            }
        }
        return Response(error_data)
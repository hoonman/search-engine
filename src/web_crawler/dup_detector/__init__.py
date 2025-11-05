from bs4 import BeautifulSoup, Comment
import hashlib
import zlib
import re
from collections import defaultdict, Counter
'''
steps:

1. canonicalization: remove unnnecessary useless stuff from the html content like script tags, headers. we should be considering the main meat of the web page
2. determine the byte for each important content in the web page? 
3. sum them up and keep them somewhere so we can compare this with other web content 

functions:
* compute bytes 
* text -> bytes -> digest bytes
* incremental streaming function (not sure if we need this?)
* is_exact_duplicate
* register_document: register the digest 

digst: random ass value (hash value) that represents a web page

'''
class ExactDupDetector:
    def __init__(self):
        pass
    
    def canonicalize_text_html(self, html: str, soup: BeautifulSoup, language_normalize: bool = True) -> str:
        '''
        extracts meaningful text from a web page
        '''
        for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
            tag.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        for noisy in soup.select('[id^=ad], [class*="ad-"], .nav, .footer'):
            noisy.decompose()

        text = soup.get_text(separator=" ")

        text = re.sub(r"\s+", " ", text).strip()

        if language_normalize:
            text = text.lower()

        return text

    def compute_digest_bytes(data: bytes, method: str = "sha256") -> str:
        """
        Compute a digest for bytes. Supported: crc32, md5, sha1, sha256, blake3.
        Return hex string (crc32 zero-padded 8 hex digits).
        """
        method = method.lower()
        if method == "crc32":
            return format(zlib.crc32(data) & 0xffffffff, "08x")
        if method == "md5":
            return hashlib.md5(data).hexdigest()
        if method == "sha1":
            return hashlib.sha1(data).hexdigest()
        if method == "sha256":
            return hashlib.sha256(data).hexdigest()
        if method == "blake3":
            if not _HAS_BLAKE3:
                raise RuntimeError("blake3 requested but not installed. `pip install blake3`")
            return blake3.blake3(data).hexdigest()
        raise ValueError(f"Unknown digest method: {method}")

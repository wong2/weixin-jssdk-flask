#-*-coding:utf-8-*-

from urlparse import urlparse, urlsplit, urlunsplit

def extract_hostname(url):
    url = url.strip()
    if not url:
        return
    parts = urlsplit(url, scheme='http')
    url = urlunsplit(parts)
    return urlparse(url).hostname

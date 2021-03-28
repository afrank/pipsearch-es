
import requests
import re
import json
import time
import os
from pipsearch.util.soup import parse_pkg_page

def expire_pkg_cache(pkg, cache_dir):
    m = pkg[0].lower()
    filename = f"{cache_dir}/{m}/{pkg}.html"
    if os.path.exists(os.path.expanduser(filename)):
        os.remove(os.path.expanduser(filename))

def get_pkg_page(pkg, cache_dir):
    base_url = "https://pypi.org"

    m = pkg[0].lower()

    filename = f"{cache_dir}/{m}/{pkg}.html"
    url = f"{base_url}/project/{pkg}/"

    if not os.path.exists(os.path.expanduser(filename)):
        print(f"Cache page does not exist for {pkg}, re-caching")
        txt = requests.get(url).text
        w = open(os.path.expanduser(filename), "w")
        w.write(txt)
        w.close()
        return txt

    return open(os.path.expanduser(filename)).read()

def get_pkg_meta(pkg, cache_dir):
    pattern = re.compile(r'[ ]*<meta property="og:([^"]+)" content="([^"]+)">')
    txt = get_pkg_page(pkg, cache_dir)
    out = parse_pkg_page(txt)
    out["name"] = pkg
    out["ts"] = int(time.time() * 1000)
    return out

def download(url, filename):
    if os.path.exists(os.path.expanduser(filename)):
        os.remove(os.path.expanduser(filename))

    txt = requests.get(url).text
    
    w = open(os.path.expanduser(filename), "w")
    w.write(txt)
    w.close()

def get_pkg_list(filename):
    pattern = re.compile(r'[ ]*<a href="([^"]+)">([^<]+)</a>')

    simple = open(os.path.expanduser(filename)).read().split("\n")

    pkg = []
    for line in simple:
        m = pattern.match(line)
        if not m:
            continue
        pkg += [m.group(2)]

    return pkg


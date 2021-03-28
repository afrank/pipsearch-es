
from elasticsearch import Elasticsearch
import time
import os

from pipsearch.util.misc import download, get_pkg_list, get_pkg_meta, expire_pkg_cache

def refresh_pkg_list(es, directory, filename="simple.html", url="https://pypi.org/simple/"):
    """
    # 1. move simple.html to simple.html-old
    # 2. Download simple.html
    # 3. compare simple.html and simple.html-old
    # 4. remove objects which no longer exist in simple.html from ES
    # 5. add new ES objects for new items in simple.html
    """

    new = os.path.expanduser(f"{directory}/{filename}")
    old = os.path.expanduser(f"{directory}/{filename}-old")

    if not os.path.exists(new):
        download(url, new)

    pkg_new = get_pkg_list(new)
    pkg_old = []

    if os.path.exists(old):
        pkg_old = get_pkg_list(old)
        os.remove(old)

    os.rename(new,old)
    download(url, new)

    pkgs_to_add = list(set(pkg_new) - set(pkg_old))
    pkgs_to_del = list(set(pkg_old) - set(pkg_new))

    add_c = len(pkgs_to_add)
    del_c = len(pkgs_to_del)

    bulk_s = 1000

    if add_c >= bulk_s:
        print(f"Adding {add_c} documents to ES")

    i=0
    for pkg in pkgs_to_add:
        meta = {}
        meta["name"] = pkg
        meta["ts"] = 0
        meta["latest_version"] = ""
        meta["summary"] = ""
        meta["project_links"] = [["",""]]
        meta["releases"] = [["",""]]
        meta["meta"] = [["",""]]
        meta["maintainers"] = [""]
        meta["description"] = ""
        es.index(index='packages', id=pkg, body=meta)
        i+=1
        if add_c >= bulk_s and i%bulk_s == 0:
            print(i)
        elif add_c < bulk_s:
            print(f"Added {pkg} to ES")

    if del_c >= bulk_s:
        print(f"Removing {del_c} documents from ES")

    i=0
    for pkg in pkgs_to_del:
        es.delete(index='packages', id=pkg)
        i+=1
        if del_c >= bulk_s and i%bulk_s == 0:
            print(i)
        elif del_c < bulk_s:
            print(f"Removing {pkg} from ES")

def refresh_metadata(es, ttl=1, max_sync=10000, cache_dir="~/.pipsearch/cache", force_recache=False):

    ts = int((time.time() - ttl) * 1000)
    body = { "query": { "range": { "ts": { "lt": ts } } }, "sort": [ { "ts": { "order": "asc" } } ] }

    i = 0
    res = es.search(index='packages', size=max_sync, body=body)
    for pkg in res["hits"]["hits"]:
        pkg = pkg["_id"]
        if force_recache:
            expire_pkg_cache(pkg, cache_dir)
        refresh_pkg_metadata(es,pkg, cache_dir)
        i+=1
        if i >= max_sync:
            break
    print(f"Refreshed {i} documents")

def refresh_pkg_metadata(es, pkg, cache_dir):
    print(f"Refreshing {pkg}")
    meta = get_pkg_meta(pkg, cache_dir)
    es.index(index='packages', id=pkg, body=meta)

def setup_es():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])

def search(es, q, max_results=100):
    body = {
        "query": {
            "query_string": {
                "query": q,
            }
        }
    }

    res = es.search(index='packages', size=max_results, body=body)
    return res["hits"]["hits"]

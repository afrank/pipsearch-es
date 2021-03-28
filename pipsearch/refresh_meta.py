#!/usr/bin/python3

from pipsearch.util.search import setup_es, refresh_pkg_list, refresh_metadata

from pipsearch.config import config

if __name__ == '__main__':
    es = setup_es()
    refresh_metadata(es, ttl=config["cache_ttl"], max_sync=config["max_sync"], cache_dir=config["cache_dir"], force_recache=True)

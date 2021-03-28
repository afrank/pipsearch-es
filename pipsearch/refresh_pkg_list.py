#!/usr/bin/python3

from pipsearch.util.search import setup_es, refresh_metadata, refresh_pkg_list
from pipsearch.config import config

if __name__ == '__main__':
    es = setup_es()
    refresh_pkg_list(es, config["cfg_dir"])

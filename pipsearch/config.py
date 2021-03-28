
import json
import os

CFG_DIR = os.environ.get("CFG_DIR", "~/.pipsearch")

CFG = os.environ.get("CFG", f"{CFG_DIR}/config.json")

CFG = os.path.expanduser(CFG)

config_keys = [
    ("cache_ttl", "Number of seconds for cache pages to live", 86400),
    ("max_sync", "Max documents to sync in a single run", 1000),
    ("cache_dir", "Directory where pages are cached to", "~/.pipsearch/cache"),
    ("api_url", "URL for client to get json results from", "http://pipsearch.org/"),
    ("cfg_dir", "Directory where config is located", CFG_DIR),
]

config = {}

_cfg = {}
if os.path.exists(CFG):
    _cfg = json.loads(open(CFG).read())

for k,_,v in config_keys:
    if k in _cfg.keys():
        config[k] = _cfg[k]
    else:
        config[k] = v


import json


class WhitelistManager:
    def __init__(self, whitelist_file='whitelist.json'):
        self.whitelist = {}
        with open(whitelist_file) as f:
            self.whitelist = json.load(f)

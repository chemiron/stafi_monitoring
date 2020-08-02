import json
import re
import requests

from functools import partial


class Node:
    methods = ('system_health', 'chain_getHeader', 'system_version')

    def __init__(self, url):
        self.url = url

    def rpc_request(self, method=None, *args):
        data = None
        if method is not None:
            data = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": method,
                "params": args,
            }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.url, data=json.dumps(data) if data is not None else None,
                          headers=headers)
        r.raise_for_status()
        return r.json()['result']

    def __getattribute__(self, item):
        if not item.startswith('__') and item in self.__class__.methods:
            return partial(self.rpc_request, item)
        return super(Node, self).__getattribute__(item)

    def peers(self):
        try:
            return self.system_health()['peers']
        except requests.HTTPError:
            return None

    def block_height(self):
        try:
            return int(self.chain_getHeader()['number'], 16)
        except requests.HTTPError:
            return None

    def version(self):
        try:
            return re.search(r"[\d.]+", self.system_version()).group(0)
        except requests.HTTPError:
            return None

    def is_online(self):
        try:
            self.rpc_request()
        except requests.HTTPError:
            return False
        return True

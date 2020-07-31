import json
import re
import requests

from functools import partial


class Node:
    methods = ('system_health', 'chain_getHeader', 'system_version')

    def __init__(self, url):
        self.url = url

    def rpc_request(self, method, *args):
        data = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
            "params": args,
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.url, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        return r.json()['result']

    def __getattribute__(self, item):
        if item in self.methods:
            return partial(self.rpc_request, item)
        return super(Node, self).__getattribute__(item)

    def peers(self):
        return self.system_health()['peers']

    def block_height(self):
        return int(self.chain_getHeader()['number'], 16)

    def version(self):
        return re.search(r"[\d.]+", self.system_version()).group(0)

import json
import re
import requests

from functools import partial


class Node:
    methods = ('system_health', 'chain_getHeader', 'system_version')

    _name = None

    def __init__(self, url, monitor_url=None):
        self.url = url
        self.monitor_url = monitor_url

    @property
    def name(self):
        if self._name is None:
            self._name = ""
            data = self.monitor_request()
            if data is not None:
                for key, value in data.items():
                    if key.startswith('substrate_build_info'):
                        res = re.search(r'\{[^}]*name="([^"]+)"', key)
                        if res is not None:
                            self._name = res.group(1)
                            break
        return self._name

    def monitor_request(self):
        if self.monitor_url is not None:
            r = requests.get(self.monitor_url)
            r.raise_for_status()

            data = {}
            for line in r.text.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split(" ", 1)
                data[key] = value
            return data

        return None

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
        if method is None:
            return None
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

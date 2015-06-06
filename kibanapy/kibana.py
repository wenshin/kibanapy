#!/usr/bin/env python
# coding=utf-8

import json
import requests


class KibanaService(object):

    DEFAULT_SEARCH_SOURCE_JSON = {
        'filter': [],
        'index': '*',
        'query': {
            'query_string': {
                'query': '*',
                'analyze_wildcard': True
            }
        }
    }

    def __init__(self):
        self._search_source_json = self.DEFAULT_SEARCH_SOURCE_JSON.copy()

    def use(self, kibana_url):
        self.url = self.url_pattern.format(base_url=kibana_url, id=self.title)

    def save(self, overwrite=False):
        params = {} if overwrite else {'op_type': 'create'}
        headers = {'content-type': 'application/json; charset=UTF-8'}
        return requests.post(self.url, params=params,
                             data=json.dumps(self.data), headers=headers)

    def delete(self):
        return requests.delete(self.url)

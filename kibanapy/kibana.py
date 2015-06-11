#!/usr/bin/env python
# coding=utf-8

import json
import requests
import copy


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

    ELASTICSEARCH_URL = "elasticsearch"
    INDEX = ".kibana"

    def __init__(self, host='127.0.0.1', port=5601, query='*',
                 search_source_filter=[]):
        self.base_url = 'http://%s:%s' % (host, port)
        self.search_source_filter = search_source_filter

        self._query = query
        self._search_source_json = copy.deepcopy(self.DEFAULT_SEARCH_SOURCE_JSON)

    @property
    def url(self):
        return self.base_url

    @property
    def query(self):
        if isinstance(self._query, str) or isinstance(self._query, unicode):
            return {
                'query': self._query,
                'analyze_wildcard': True
            }
        elif isinstance(self._query, dict):
            return self._query

    @property
    def search_source_json(self):
        self._search_source_json['filter'] = self.search_source_filter
        self._search_source_json['query'] = self.query
        return json.dumps(self._search_source_json)

    def save(self, overwrite=False):
        params = {} if overwrite else {'op_type': 'create'}
        headers = {'content-type': 'application/json; charset=UTF-8'}
        return requests.post(self.url, params=params,
                             data=json.dumps(self.data), headers=headers)

    def delete(self):
        return requests.delete(self.url)


class KibanaElasticsearchOperator(KibanaService):
    pass

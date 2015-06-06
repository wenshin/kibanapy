#!/usr/bin/env python
# coding=utf-8

import json
import requests


class Dashboard(object):

    url_pattern = '{base_url}/dashboard/{id}'

    def __init__(self, title, description='', query=None):
        self.title = title
        self.desc = description
        self.query = query
        self.panels = []

    @property
    def search_source_json(self):
        if isinstance(self.query, str) or isinstance(self.query, unicode):
            query_string = {
                'query': self.query,
                'analyze_wildcard': True
            }
            self._search_source_json['query']['query_string'] = query_string
        elif isinstance(self.query, dict):
            self._search_source_json['query'] = self.query
        return json.dumps(self._search_source_json)

    def add_visualization(self, vis):
        self.panels.append(vis.config)

    def use(self, kibana_url):
        self.url = self.url_pattern.format(base_url=kibana_url, id=self.title)

    def save(self, kibana_url, overwrite=False):
        data = {}
        data['hits'] = 0
        data['title'] = self.title
        data['description'] = self.desc
        data['panelsJSON'] = json.dumps(self.panels)
        data['kibanaSavedObjectMeta'] = {}
        data['kibanaSavedObjectMeta']['searchSourceJSON'] = self.search_source_json

        params = {}
        if not overwrite:
            params['op_type'] = 'create'

        headers = {'content-type': 'application/json; charset=UTF-8'}
        return requests.post(self.url, params=params,
                             data=json.dumps(data), headers=headers)

    def delete(self):
        return requests.delete(self.url)

    def get_share_link(self):
        pass

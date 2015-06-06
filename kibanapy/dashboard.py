#!/usr/bin/env python
# coding=utf-8

import json

from .kibana import KibanaService


class Dashboard(KibanaService):

    url_pattern = '{base_url}/dashboard/{id}'

    def __init__(self, title, description='', query=None):
        super(Dashboard, self).__init__()
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

    @property
    def data(self):
        d = {}
        d['hits'] = 0
        d['title'] = self.title
        d['description'] = self.desc
        d['panelsJSON'] = json.dumps(self.panels)
        d['kibanaSavedObjectMeta'] = {}
        d['kibanaSavedObjectMeta']['searchSourceJSON'] = self.search_source_json
        return d

    def add_visualization(self, vis):
        self.panels.append(vis.config)

    @property
    def share_link(self):
        return ''

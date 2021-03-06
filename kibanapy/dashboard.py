#!/usr/bin/env python
# coding=utf-8

import json
import urllib

from .libs import rison
from .kibana import KibanaService


class Dashboard(KibanaService):

    url_pattern_share = '{url_base}/#/dashboard/{title}?{query}'

    def __init__(self, title, id=None, description='', **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.id = id or title
        self.title = title
        self.desc = description
        self.panels = []

    @property
    def url(self):
        return self.URL_PATTERN_ES.format(
            url_base=self.url_base, index=self.index, type='dashboard', id=self.id)

    @property
    def data(self):
        d = {}
        d['hits'] = 0
        d['title'] = self.title
        d['description'] = self.desc
        d['panelsJSON'] = json.dumps(self.panels)
        d['kibanaSavedObjectMeta'] = {}
        d['kibanaSavedObjectMeta']['searchSourceJSON'] = [self.search_source_json]
        return d

    def add_visualization(self, vis):
        self.panels.append(vis.config)

    def get_share_link(self, url_base='', embed=False):
        _a = {}
        _a['filters'] = []
        _a['title'] = self.title
        _a['query'] = self.query
        _a['panels'] = self.panels

        _g = {}
        _g['refreshInterval'] = {'display': 'Off', 'section': 0, 'value': 0}
        _g['time'] = {'from': 'now/y', 'mode': 'quick', 'to': 'now/y'}

        query = {}
        query['_a'] = rison.dumps(_a).encode('utf-8')
        query['_g'] = rison.dumps(_g).encode('utf-8')

        share_url = self.url_pattern_share.format(
            url_base=url_base, title=self.title,
            query=urllib.urlencode(query))

        if embed:
            share_url = share_url.replace('?', '?embed&')

        return share_url

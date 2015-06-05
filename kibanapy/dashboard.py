#!/usr/bin/env python
# coding=utf-8

import json
import requests


class Dashboard(object):

    url_pattern = '{base_url}/dashboard/{id}'

    def __init__(self, title, description=""):
        self.title = title
        self.desc = description
        self.panels = []

    def add_panel(self, vis):
        self.panels.append(vis.dict)

    def save(self, kibana_url, overwrite=False):
        data = {}
        data['title'] = self.title
        data['description'] = self.desc
        data['panelsJSON'] = json.dumps(self.panels)

        params = {}
        if not overwrite:
            params['op_type'] = 'create'

        url = self.url_pattern.format(base_url=kibana_url, id=self.title)

        requests.post(url, params=params, data=data, content_type='application/json')

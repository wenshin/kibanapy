#!/usr/bin/env python
# coding=utf-8

import requests


class KibanaServer(object):
    '''
    '''
    DEFAULT_KIBANA_URL = "http://127.0.0.1:5601"

    def __init__(self, url=DEFAULT_KIBANA_URL):
        self.url = url

    def save_visualization(self, query, filter=None, overwrite=False):
        pass

    def save_dashboard(self, overwrite=False):
        pass

    def generate_share_link(self):
        pass

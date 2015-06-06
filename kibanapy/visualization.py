#!/usr/bin/env python
# coding=utf-8

import json
import requests


class Visualization(object):

    DEFAULT_POSITION = {
        # 宽，整数，使用12等分栅格系统
        'size_x': 4,
        # 高，整数，使用和宽相同的最小单位，可以与 size_x 不同
        'size_y': 4,
        # 行数
        'row': 1,
        # 列数。当前行前一个图表的宽 + 1。
        # 如：
        #        |col1=1         |col1=5       |
        #   row1 |default config | next config |
        'col': 1
    }

    DEFAULT_CHART_CONFIG = {
        'addLegend': True,
        'addTooltip': True,
        'isDonut': False,
        'shareYAxis': True
    }

    DEFAULT_SEARCH_SOURCE_JSON = {
        'filter': [],
        'index': '*',
        'query': {
            'query_string': {
                'query': '*',
                'analyze_wildcard': True
            }
        },
        'highlight': {
            'pre_tags': ['@kibana-highlighted-field@'],
            'post_tags': ['@/kibana-highlighted-field@'],
            'fields': {'*': {}}
        }
    }

    url_pattern = '{base_url}/visualization/{id}'

    def __init__(self, title, chart_type, aggs=None, query=None,
                 desc='', position={}, chart_config={}):
        '''
        :param position: Kibana 的位置和大小配置
        :param config: Kibana 图表信息配置，如：是否显示图例等
        '''
        chart_config.update(self.DEFAULT_CHART_CONFIG)

        self.title = title
        self.chart_type = chart_type
        self.aggs = aggs
        self.query = query
        self.desc = desc
        self.position = position.update(self.DEFAULT_POSITION)
        self.chart_config = chart_config
        self._search_source_json = self.DEFAULT_SEARCH_SOURCE_JSON.copy()

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
    def vis_state(self):
        vis = {}
        vis['aggs'] = self.aggs
        vis['listeners'] = {}
        vis['params'] = self.chart_config
        vis['type'] = self.chart_type
        return json.dumps(vis)

    def use(self, kibana_url):
        self.url = self.url_pattern.format(base_url=kibana_url, id=self.title)

    def save(self, overwrite=False):
        data = {}
        data['title'] = self.title
        data['visState'] = self.vis_state
        data['description'] = self.desc
        data['version'] = 1
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

    @property
    def config(self):
        '''
        返回Dashboard需要的可视化配置信息
        '''
        conf = {}
        conf['id'] = self.title
        conf['type'] = 'visualization'
        conf.update(self.position)
        return conf


class Chart(object):

    DEFAULT_PARAMS = {
        'addLegend': True,
        'addTooltip': True,
        'isDonut': False,
        'shareYAxis': True
    }

    def __init__(self, chart_type, chart_params=DEFAULT_PARAMS.copy()):
        self.chart_type

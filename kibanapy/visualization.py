#!/usr/bin/env python
# coding=utf-8

import json
from .kibana import KibanaService


class Visualization(KibanaService):

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

    CUSTOM_SEARCH_SOURCE_JSON = {
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
        super(Visualization, self).__init__()

        position.update(self.DEFAULT_POSITION)
        chart_config.update(self.DEFAULT_CHART_CONFIG)

        self.title = title
        self.chart_type = chart_type
        self.aggs = aggs
        self.query = query
        self.desc = desc
        self.position = position
        self.chart_config = chart_config
        self._search_source_json.update(self.CUSTOM_SEARCH_SOURCE_JSON)

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

    @property
    def data(self):
        d = {}
        d['title'] = self.title
        d['visState'] = self.vis_state
        d['description'] = self.desc
        d['version'] = 1
        d['kibanaSavedObjectMeta'] = {}
        d['kibanaSavedObjectMeta']['searchSourceJSON'] = self.search_source_json
        return d

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

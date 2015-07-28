#!/usr/bin/env python
# coding=utf-8

import os
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

    INDEX = ".kibana"
    HEADERS = {'content-type': 'application/json; charset=UTF-8'}
    URL_PATTERN_ES = "{url_base}/elasticsearch/{index}/{type}/{id}"

    def __init__(self, host='127.0.0.1', port=5601, query='*',
                 search_source_filter=[], index=INDEX):
        self.url_base = 'http://%s:%s' % (host, port)
        self.search_source_filter = search_source_filter
        self.index = index

        self._query = query
        self._search_source_json = copy.deepcopy(self.DEFAULT_SEARCH_SOURCE_JSON)

    @property
    def url(self):
        return self.url_base

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

    def format_url_indice(self, indice_id):
        return self.URL_PATTERN_ES.format(
            url_base=self.url_base, index=self.index,
            type='index-pattern', id=indice_id)

    def create_indice(self, timefield, indice_id='*', fields=[], headers=HEADERS):
        ''' 创建Kibana 搜索的索引范围，默认为 '*'
        '''
        url_indice = self.format_url_indice(indice_id)
        data = {
            'customFormats': json.dumps({}),
            'fields': json.dumps(fields),
            'timeFieldName': timefield,
            'title': indice_id
        }
        return requests.post(url_indice, data=json.dumps(data), headers=headers)

    def save(self, overwrite=False, headers=HEADERS):
        params = {} if overwrite else {'op_type': 'create'}
        return requests.post(self.url, params=params,
                             data=json.dumps(self.data), headers=headers)

    def delete(self, url=None, **kwargs):
        ''' 删除当前实例对应的数据
        '''
        url = url or self.url
        return requests.delete(url, **kwargs)

    def delete_indice(self, indice_id):
        return self.delete(self.format_url_indice(indice_id))

    def clean(self, **kwargs):
        '''清理kibana 在 Elasticsearch dashboard 或者visualization 下的所有数据
        '''
        return requests.delete(os.path.dirname(self.url), **kwargs)

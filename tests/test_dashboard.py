#!/usr/bin/env python
# coding=utf-8

import unittest
from kibanapy.dashboard import Dashboard
from kibanapy.visualization import Visualization
from kibanapy.kibanapy import KibanaServer


PORT_AGGS = [{
    'id': '1',
    'params': {'field': 'target'},
    'schema': 'metric',
    'type': 'cardinality'},

{
    'id': '2',
    'params': {
        'field': 'portinfo.port',
        'order': 'desc',
        'orderBy': '1',
        'size': 10000000
    },
    'schema': 'segment',
    'type': 'terms'
}]


class DashboardTestCase(unittest.TestCase):

    def setUp(self):
        query = 'abc'
        self.kibana_url = 'http://10.8.150.69:5601/elasticsearch/.kibana'
        self.vis1 = Visualization('kibanapyVis1', 'pie', PORT_AGGS, query=query)
        self.vis1.use(self.kibana_url)

    def tearDown(self):
        self.vis1.delete()

    def test_save_visualization_not_overwrite_success(self):
        ''' 测试保存 visualization 使用非复写模式成功，重复写入返回409 Conflict
        '''
        resp = self.vis1.save()
        self.assertEqual(resp.status_code, 201, resp.json())

        resp = self.vis1.save()
        self.assertEqual(resp.status_code, 409, resp.json())

    def test_save_visualization_with_overwrite_success(self):
        ''' 测试保存 visualization 使用复写模式，重复写入成功
        '''
        resp = self.vis1.save(overwrite=True)
        self.assertEqual(resp.status_code, 201, resp.json())


    def test_save_dashboard_not_overwrite_success(self):
        ''' 测试保存 dashboard 使用非复写模式
        '''
        ds1 = Dashboard('kibanapyD1')
        ds1.use(self.kibana_url)
        ds1.add_visualization(self.vis1)
        resp = ds1.save(self.kibana_url)
        self.assertEqual(resp.status_code, 201, resp.json())

#!/usr/bin/env python
# coding=utf-8

import urllib
import unittest
from kibanapy.dashboard import Dashboard
from kibanapy.visualization import Visualization


PORT_AGGS = [{
    'id': '1',
    'params': {'field': 'target'},
    'schema': 'metric',
    'type': 'cardinality'
}, {
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
        self.kibana_host = '10.8.150.69'
        self.vis = Visualization(
            'kibanapyVis1', 'pie', aggs=PORT_AGGS, query=query, host=self.kibana_host)

        self.ds = Dashboard('kibanapyD1', host=self.kibana_host)
        self.ds.add_visualization(self.vis)

    def tearDown(self):
        self.vis.delete()
        self.ds.delete()

    def test_save_visualization_not_overwrite_success(self):
        ''' 测试保存 visualization 使用非复写模式成功，重复写入返回409 Conflict
        '''
        resp = self.vis.save()
        self.assertEqual(resp.status_code, 201, resp.json())

        resp = self.vis.save()
        self.assertEqual(resp.status_code, 409, resp.json())

    def test_save_visualization_with_overwrite_success(self):
        ''' 测试保存 visualization 使用复写模式，重复写入成功
        '''
        resp = self.vis.save(overwrite=True)
        self.assertEqual(resp.status_code, 201, resp.json())

    def test_save_dashboard_not_overwrite_success(self):
        ''' 测试保存 dashboard 使用非复写模式
        '''
        resp = self.ds.save()
        self.assertEqual(resp.status_code, 201, resp.json())

        resp = self.ds.save()
        self.assertEqual(resp.status_code, 409, resp.json())

    def test_save_dashboard_with_overwrite_success(self):
        ''' 测试保存 dashboard 使用复写模式，重复写入成功
        '''
        resp = self.ds.save(overwrite=True)
        self.assertEqual(resp.status_code, 201, resp.json())

    def test_dashboard_share_link(self):
        '''测试获取 dashboard 的分享链接
        '''
        share_link = self.ds.get_share_link(embed=True)
        self.assertTrue('kibanapyVis1' in share_link)
        self.assertTrue(urllib.quote('!') in share_link)
        self.assertTrue(urllib.quote('(') in share_link)
        self.assertTrue(urllib.quote(':') in share_link)
        self.assertTrue(urllib.quote('') in share_link)

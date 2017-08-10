# -*- coding: utf-8 -*-
"""
Virtual Network
~~~~~~~~~~~~~~~

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on May 2, 2017
"""

import unittest
import sys
import logging
import config
from resttestms import http, json, log, test, parse

LOG = logging.getLogger(__name__)

# Leave as None to use default host
HOST_OVERRIDE = None

# Leave as None to use default json directory
DATA_OVERRIDE = None

# Leave as None to use default depth
DEPTH_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin Virtual Network Tests")
    VirtualNetworkTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE, DEPTH_OVERRIDE)

class VirtualNetworkTest(unittest.TestCase):
    """Collection of data to test the virtual network microservice"""

    PORT = '46016'
    JSON_NAME = 'data_virtualnetwork.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override, depth_override):
        """Initialize base url, json file path, and depth"""
        cls.HOST = test.select_host(config.HOST, host_override)
        cls.DATA = test.select_directory(config.DATA, directory_override)
        cls.DEPTH = test.select_depth(config.DEPTH, depth_override)
        cls.BASE_URL = test.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = test.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Get
###################################################################################################

class Get(VirtualNetworkTest):
    """Tests for Get Endpoint"""

    ENDPOINT = 'get'

    def test_json(self):
        """GET JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# Post
###################################################################################################

class Post(VirtualNetworkTest):
    """Tests for Post Endpoint"""

    ENDPOINT = 'post'

    def test_json(self):
        """POST JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Delete NetworkId
###################################################################################################

class DeleteNetworkId(VirtualNetworkTest):
    """Tests for Delete NetworkId Endpoint"""

    ENDPOINT = 'delete_networkId'

    def test_json(self):
        """DELETE NETWORKID JSON TESTS"""
        test.auto_run_json_tests('DELETE', self)

###################################################################################################
# Get NetworkId
###################################################################################################

class GetNetworkId(VirtualNetworkTest):
    """Tests for Get NetworkId Endpoint"""

    ENDPOINT = 'get_networkId'

    def test_json(self):
        """GET NETWORKID JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# Put NetworkId
###################################################################################################

class PutNetworkId(VirtualNetworkTest):
    """Tests for Put NetworkId Endpoint"""

    ENDPOINT = 'put_networkId'

    def test_json(self):
        """PUT NETWORKID JSON TESTS"""
        test.auto_run_json_tests('PUT', self)

###################################################################################################
# Delete NetworkId IpAddressPools
###################################################################################################

class DeleteNetworkIdIpAddressPools(VirtualNetworkTest):
    """Tests for Delete NetworkId IpAddressPools Endpoint"""

    ENDPOINT = 'delete_networkId_ipAddressPools'

    def test_json(self):
        """DELETE NETWORKID IPADDRESSPOOLS JSON TESTS"""
        test.auto_run_json_tests('DELETE', self)

###################################################################################################
# Get NetworkId IpAddressPools
###################################################################################################

class GetNetworkIdIpAddressPools(VirtualNetworkTest):
    """Tests for Get NetworkId IpAddressPools Endpoint"""

    ENDPOINT = 'get_networkId_ipAddressPools'

    def test_json(self):
        """GET NETWORKID IPADDRESSPOOLS JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# Post NetworkId IpAddressPools
###################################################################################################

class PostNetworkIdIpAddressPools(VirtualNetworkTest):
    """Tests for Post NetworkId IpAddressPools Endpoint"""

    ENDPOINT = 'post_networkId_ipAddressPools'

    def test_json(self):
        """POST NETWORKID IPADDRESSPOOLS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Put NetworkId IpAddressPools
###################################################################################################

class PutNetworkIdIpAddressPools(VirtualNetworkTest):
    """Tests for Put NetworkId IpAddressPools Endpoint"""

    ENDPOINT = 'put_networkId_ipAddressPools'

    def test_json(self):
        """PUT NETWORKID IPADDRESSPOOLS JSON TESTS"""
        test.auto_run_json_tests('PUT', self)

###################################################################################################
# NetworkId IpAddressPools Export
###################################################################################################

class NetworkIdIpAddressPoolsExport(VirtualNetworkTest):
    """Tests for NetworkId IpAddressPools Export Endpoint"""

    ENDPOINT = 'networkId_ipAddressPools_export'

    def test_json(self):
        """NETWORKID IPADDRESSPOOLS EXPORT JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# NetworkId IpAddressPools IpAddress
###################################################################################################

class NetworkIdIpAddressPoolsIpAddress(VirtualNetworkTest):
    """Tests for NetworkId IpAddressPools IpAddress Endpoint"""

    ENDPOINT = 'networkId_ipAddressPools_ipAddress'

    def test_json(self):
        """NETWORKID IPADDRESSPOOLS IPADDRESS JSON TESTS"""
        test.auto_run_json_tests('DELETE', self)

###################################################################################################
# NetworkId Ipv4Ranges
###################################################################################################

class NetworkIdIpIpv4Ranges(VirtualNetworkTest):
    """Tests for NetworkId Ipv4Ranges Endpoint"""

    ENDPOINT = 'networkId_ipv4Ranges'

    def test_json(self):
        """NETWORKID IPADDRESSPOOLS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Delete NetworkId Ipv4Ranges RangeId
###################################################################################################

class DeleteNetworkIdIpIpv4RangesRangeId(VirtualNetworkTest):
    """Tests for Delete NetworkId Ipv4Ranges RangeId Endpoint"""

    ENDPOINT = 'delete_networkId_ipv4Ranges_rangeId'

    def test_json(self):
        """DELETE NETWORKID IPADDRESSPOOLS RANGEID JSON TESTS"""
        test.auto_run_json_tests('DELETE', self)

###################################################################################################
# Put NetworkId Ipv4Ranges RangeId
###################################################################################################

class PutNetworkIdIpIpv4RangesRangeId(VirtualNetworkTest):
    """Tests for Put NetworkId Ipv4Ranges RangeIdEndpoint"""

    ENDPOINT = 'put_networkId_ipv4Ranges_rangeId'

    def test_json(self):
        """PUT NETWORKID IPADDRESSPOOLS RANGEID JSON TESTS"""
        test.auto_run_json_tests('PUT', self)

###################################################################################################
# Test Sequences
###################################################################################################

class TestSequences(VirtualNetworkTest):
    """Test Sequences for Virtual Network"""

    def test_create_and_delete(self):
        """CREATE AND DELETE NETWORK"""
        test.run_json_test('GET', self, Get, "test_empty_network")
        network_id = test.run_json_test('POST', self, Post, "test_create_network1")["id"]
        path_mod = {"path":"/api/1.0/networks/{}".format(network_id)}
        test.run_mod_json_test('DELETE', self, DeleteNetworkId, "test_networkId", path_mod)

    def test_create_and_update(self):
        """CREATE AND UPDATE NETWORK"""
        test.run_json_test('GET', self, Get, "test_empty_network")
        network_id = test.run_json_test('POST', self, Post, "test_create_network1")["id"]
        path_mod = {"path": "/api/1.0/networks/{}".format(network_id)}
        test.run_json_test('GET', self, Get, "test_network_present")
        test.run_mod_json_test('GET', self, GetNetworkId, "test_network1", path_mod)
        test.run_mod_json_test('PUT', self, PutNetworkId, "test_update_networkX", path_mod)
        test.run_mod_json_test('GET', self, GetNetworkId, "test_networkX", path_mod)
        test.run_mod_json_test('DELETE', self, DeleteNetworkId, "test_networkId", path_mod)

    def test_create_duplicate_networks(self):
        """CREATE DUPLICATE NETWORK"""
        test.run_json_test('GET', self, Get, "test_empty_network")
        network_id = test.run_json_test('POST', self, Post, "test_create_network1")["id"]
        path_mod = {"path": "/api/1.0/networks/{}".format(network_id)}
        test.run_json_test('POST', self, Post, "test_create_duplicate")
        test.run_mod_json_test('DELETE', self, DeleteNetworkId, "test_networkId", path_mod)
    
    def test_ip_address_pools(self):
        """CHECK IP ADDRESS POOLS"""
        test.run_json_test('GET', self, Get, "test_empty_network")
        network_id = test.run_json_test('POST', self, Post, "test_create_network1")["id"]
        path_mod = {"path": "/api/1.0/networks/{}".format(network_id)}
        ip_path_mod = {"path": "/api/1.0/networks/{}/ipAddressPools".format(network_id)}
        test.run_mod_json_test('GET', self, GetNetworkIdIpAddressPools, "test_networkId_ipAddressPools", ip_path_mod)
        test.run_mod_json_test('DELETE', self, DeleteNetworkId, "test_networkId", path_mod)
    
    def test_create_pool_and_reserve(self):
        """RESERVE IPV4 RANGE"""
        test.run_json_test('GET', self, Get, "test_empty_network")
        network_id = test.run_json_test('POST', self, Post, "test_create_network1")["id"]
        id_mod = {"path":"/api/1.0/networks/{}".format(network_id)}
        ipv4_id_mod = {"path":"/api/1.0/networks/{}/ipv4Ranges".format(network_id)}
        range_id = test.run_mod_json_test('POST', self, NetworkIdIpIpv4Ranges, "test_network1_ipv4pool", ipv4_id_mod)["id"]
        test.run_mod_json_test('GET', self, GetNetworkId, "test_network1_rangeid", id_mod)
        ipv4_range_mod = {"path":"/api/1.0/networks/{}/ipv4Ranges/{}".format(network_id, range_id)}
        test.run_mod_json_test('DELETE', self, DeleteNetworkIdIpIpv4RangesRangeId, "test_delete_network1_pool", ipv4_range_mod)
        test.run_mod_json_test('DELETE', self, DeleteNetworkId, "test_networkId", id_mod)

###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA, DEPTH = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    DEPTH_OVERRIDE = DEPTH if DEPTH else DEPTH_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()

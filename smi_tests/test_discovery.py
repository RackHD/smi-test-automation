# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Prashanth_L_Gowda
'''

import unittest
import sys
import logging
import config
from resttestms import http, json, log, test, parse

LOG = logging.getLogger(__name__)

# Leave as None to use default Host
HOST_OVERRIDE = None

# Leave as None to use default json directory
DATA_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin Discovery Tests")
    DiscoveryTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE)

class DiscoveryTest(unittest.TestCase):
    """Collection of data to test the discovery microservice"""
 
    PORT = '46002'
    JSON_NAME = 'data_discovery.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(config.HOST, host_override)
        cls.DATA = json.select_directory(config.DATA, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Config Device
###################################################################################################

class ConfigDevice(DiscoveryTest):
    """Tests for Config Device Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'config_device'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """CONFIG DEVICE JSON TESTS"""
        test.get_json(self)

###################################################################################################
# IPS
###################################################################################################

class IPS(DiscoveryTest):
    """Tests for IPS Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'ips'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """IPS JSON TESTS"""
        test.post_json(self)

###################################################################################################
# Range
###################################################################################################

class Range(DiscoveryTest):
    """Tests for Range Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'range'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """RANGE JSON TESTS"""
        test.post_json(self)

###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()

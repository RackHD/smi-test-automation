# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Rahman Muhammad
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
    LOG.info("Begin Power Thermal Tests")
    PowerThermalTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE)

class PowerThermalTest(unittest.TestCase):
    """Collection of data to test the power thermal microservice"""
 
    PORT = '46019'
    JSON_NAME = 'data_powerthermal.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(config.HOST, host_override)
        cls.DATA = json.select_directory(config.DATA, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Powerthermal Post
###################################################################################################

class PowerThermalPost(PowerThermalTest):
    """Tests for Powerthermal Post Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'powerthermal_post'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)
    def test_json(self):
        """POWERTHERMAL POST JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# Powerthermal Put
###################################################################################################

class PowerThermalPut(PowerThermalTest):
    """Tests for Powerthermal Put Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'powerthermal_put'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)
    def test_json(self):
        """POWERTHERMAL PUT JSON TESTS"""
        test.run_json('PUT', self)

###################################################################################################
# Version
###################################################################################################

class Version(PowerThermalTest):
    """Tests for Version Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'version'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """VERSION JSON TESTS"""
        test.run_json('GET', self)

###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()

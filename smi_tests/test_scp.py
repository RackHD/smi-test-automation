# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: mkowkab
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
    LOG.info("Begin Server Configuration Profile Tests")
    SCPTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE)

class SCPTest(unittest.TestCase):
    """Collection of data to test the scp microservice"""

    PORT = '46018'
    JSON_NAME = 'data_scp.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(config.HOST, host_override)
        cls.DATA = json.select_directory(config.DATA, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Export
###################################################################################################

class Export(SCPTest):
    """Tests for Export Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'export'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)
    def test_json(self):
        """EXPORT JSON TESTS"""
        test.run_all_json_tests('POST', self)

###################################################################################################
# GetComponents
###################################################################################################

class GetComponents(SCPTest):
    """Tests for GetComponents Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'getComponents'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """GETCOMPONENTS JSON TESTS"""
        test.run_all_json_tests('POST', self)

###################################################################################################
# Import
###################################################################################################

class Import(SCPTest):
    """Tests for Import Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'import'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """IMPORT JSON TESTS"""
        test.run_all_json_tests('POST', self)

###################################################################################################
# UpdateComponents
###################################################################################################

class UpdateComponents(SCPTest):
    """Tests for UpdateComponents Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'updateComponents'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """UPDATECOMPONENTS JSON TESTS"""
        test.run_all_json_tests('POST', self)

###################################################################################################
# Trap ConfigureTraps Foo
###################################################################################################

class TrapConfigureTrapsFoo(SCPTest):
    """Tests for Trap ConfigureTraps Foo Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'trap_configureTraps_foo'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """TRAPS CONFIGURETRAPS FOO JSON TESTS"""
        test.run_all_json_tests('POST', self)

###################################################################################################
# Trap UpdateTrapFormat Foo
###################################################################################################

class TrapUpdateTrapFormatFoo(SCPTest):
    """Tests for Trap UpdateTrapFormat Foo Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'trap_updateTrapFormat_foo'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """TRAPS UPDATETRAPFORMAT FOO JSON TESTS"""
        test.run_all_json_tests('POST', self)

###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()

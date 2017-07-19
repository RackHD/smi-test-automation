# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 4, 2017

@author: Prashanth_L_Gowda, Dan_Phelps
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
    LOG.info("Begin Server Inventory Tests")
    ServerInventoryTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE)

class ServerInventoryTest(unittest.TestCase):
    """Collection of data to test the server inventory microservice"""

    PORT = '46011'
    JSON_NAME = 'data_serverinventory.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(config.HOST, host_override)
        cls.DATA = json.select_directory(config.DATA, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Bios
###################################################################################################

class Bios(ServerInventoryTest):
    """Tests for Bios Endpoint"""

    ENDPOINT = 'bios'

    def test_json(self):
        """BIOS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Boot
###################################################################################################

class Boot(ServerInventoryTest):
    """Tests for Boot Endpoint"""

    ENDPOINT = 'boot'

    def test_json(self):
        """BOOT JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Callback
###################################################################################################

class Callback(ServerInventoryTest):
    """Tests for Callback Endpoint"""

    ENDPOINT = 'callback'

    def test_json(self):
        """CALLBACK JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# DummyCallback
###################################################################################################

class DummyCallback(ServerInventoryTest):
    """Tests for DummyCallback Endpoint"""

    ENDPOINT = 'dummyCallback'

    def test_json(self):
        """DUMMYCALLBACK JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Hardware
###################################################################################################

class Hardware(ServerInventoryTest):
    """Tests for Hardware Endpoint"""

    ENDPOINT = 'hardware'

    def test_json(self):
        """HARDWARE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Ips
###################################################################################################

class Ips(ServerInventoryTest):
    """Tests for Ips Endpoint"""

    ENDPOINT = 'ips'

    def test_json(self):
        """IPS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Nics
###################################################################################################

class Nics(ServerInventoryTest):
    """Tests for Nics Endpoint"""

    ENDPOINT = 'nics'

    def test_json(self):
        """NICS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Software
###################################################################################################

class Software(ServerInventoryTest):
    """Tests for Software Endpoint"""

    ENDPOINT = 'software'

    def test_json(self):
        """SOFTWARE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Summary
###################################################################################################

class Summary(ServerInventoryTest):
    """Tests for Summary Endpoint"""

    ENDPOINT = 'summary'

    def test_json(self):
        """SUMMARY JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# LogsGetLC
###################################################################################################

class LogsGetLC(ServerInventoryTest):
    """Tests for LogsGetLC Endpoint"""

    ENDPOINT = 'logs_get_lc'

    def test_json(self):
        """LOGSGETLC JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# LogsGetSEL
###################################################################################################

class LogsGetSEL(ServerInventoryTest):
    """Tests for LogsGetSEL Endpoint"""

    ENDPOINT = 'logs_get_sel'

    def test_json(self):
        """LOGSGETSEL JSON TESTS"""
        test.auto_run_json_tests('POST', self)


###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()

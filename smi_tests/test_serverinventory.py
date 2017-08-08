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

# Leave as None to use default host
HOST_OVERRIDE = None

# Leave as None to use default json directory
DATA_OVERRIDE = None

# Leave as None to use default depth
DEPTH_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin Server Inventory Tests")
    ServerInventoryTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE, DEPTH_OVERRIDE)

class ServerInventoryTest(unittest.TestCase):
    """Collection of data to test the server inventory microservice"""

    PORT = '46011'
    JSON_NAME = 'data_serverinventory.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override, depth_override):
        """Initialize base url, json file path, and depth"""
        cls.HOST = test.select_host(config.HOST, host_override)
        cls.DATA = test.select_directory(config.DATA, directory_override)
        cls.DEPTH = test.select_depth(config.DEPTH, depth_override)
        cls.BASE_URL = test.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = test.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Bios 1
###################################################################################################

class Bios1(ServerInventoryTest):
    """Tests for Bios 1 Endpoint"""

    ENDPOINT = 'bios_1'

    def test_json(self):
        """BIOS 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Bios 2
###################################################################################################

class Bios2(ServerInventoryTest):
    """Tests for Bios 2 Endpoint"""

    ENDPOINT = 'bios_2'

    def test_json(self):
        """BIOS 2 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Boot 1
###################################################################################################

class Boot1(ServerInventoryTest):
    """Tests for Boot 1 Endpoint"""

    ENDPOINT = 'boot_1'

    def test_json(self):
        """BOOT 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Boot 2
###################################################################################################

class Boot2(ServerInventoryTest):
    """Tests for Boot 2 Endpoint"""

    ENDPOINT = 'boot_2'

    def test_json(self):
        """BOOT 2 JSON TESTS"""
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
# DCIM Type
###################################################################################################

class DCIMType(ServerInventoryTest):
    """Tests for DCIM Type Endpoint"""

    ENDPOINT = 'dcim_type'

    def test_json(self):
        """DCIM TYPE JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Hardware 1
###################################################################################################

class Hardware1(ServerInventoryTest):
    """Tests for Hardware 1 Endpoint"""

    ENDPOINT = 'hardware_1'

    def test_json(self):
        """HARDWARE 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Hardware 2
###################################################################################################

class Hardware2(ServerInventoryTest):
    """Tests for Hardware 2 Endpoint"""

    ENDPOINT = 'hardware_2'

    def test_json(self):
        """HARDWARE 2 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Manager 1
###################################################################################################

class Manager1(ServerInventoryTest):
    """Tests for Manager 1 Endpoint"""

    ENDPOINT = 'manager_1'

    def test_json(self):
        """MANAGER 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Manager 2
###################################################################################################

class Manager2(ServerInventoryTest):
    """Tests for Manager 2 Endpoint"""

    ENDPOINT = 'manager_2'

    def test_json(self):
        """MANAGER 2 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Nics 1
###################################################################################################

class Nics1(ServerInventoryTest):
    """Tests for Nics 1 Endpoint"""

    ENDPOINT = 'nics_1'

    def test_json(self):
        """NICS 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Nics 2
###################################################################################################

class Nics2(ServerInventoryTest):
    """Tests for Nics 2 Endpoint"""

    ENDPOINT = 'nics_2'

    def test_json(self):
        """NICS 2 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Software 1
###################################################################################################

class Software1(ServerInventoryTest):
    """Tests for Software 1 Endpoint"""

    ENDPOINT = 'software_1'

    def test_json(self):
        """SOFTWARE 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Software 2
###################################################################################################

class Software2(ServerInventoryTest):
    """Tests for Software 2 Endpoint"""

    ENDPOINT = 'software_2'

    def test_json(self):
        """SOFTWARE 2 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Summary 1
###################################################################################################

class Summary1(ServerInventoryTest):
    """Tests for Summary 1 Endpoint"""

    ENDPOINT = 'summary_1'

    def test_json(self):
        """SUMMARY 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Summary 2
###################################################################################################

class Summary2(ServerInventoryTest):
    """Tests for Summary 2 Endpoint"""

    ENDPOINT = 'summary_2'

    def test_json(self):
        """SUMMARY 2 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Logs Get Type 1
###################################################################################################

class LogsGetType1(ServerInventoryTest):
    """Tests for Logs Get Type 1 Endpoint"""

    ENDPOINT = 'logs_get_type_1'

    def test_json(self):
        """LOGS GET TYPE 1 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Logs Get Type 2
###################################################################################################

class LogsGetType2(ServerInventoryTest):
    """Tests for Logs Get Type 2 Endpoint"""

    ENDPOINT = 'logs_get_type_2'

    def test_json(self):
        """LOGS GET TYPE 2 JSON TESTS"""
        test.auto_run_json_tests('POST', self)

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

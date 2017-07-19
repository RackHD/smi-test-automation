# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
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
    LOG.info("Begin Firmware Update Tests")
    FirmwareUpdateTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE)

class FirmwareUpdateTest(unittest.TestCase):
    """Collection of data to test the firmware update microservice"""

    PORT = '46010'
    JSON_NAME = 'data_firmwareupdate.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(config.HOST, host_override)
        cls.DATA = json.select_directory(config.DATA, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Comparer
###################################################################################################

class Comparer(FirmwareUpdateTest):
    """Tests for Comparer Endpoint"""

    ENDPOINT = 'comparer'

    def test_json(self):
        """COMPARER JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Comparer Catalog
###################################################################################################

class ComparerCatalog(FirmwareUpdateTest):
    """Tests for Comparer Catalog Endpoint"""

    ENDPOINT = 'comparer_catalog'

    def test_json(self):
        """COMPARER CATALOG JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Comparer Custom
###################################################################################################

class ComparerCustom(FirmwareUpdateTest):
    """Tests for Comparer Custom Endpoint"""

    ENDPOINT = 'comparer_custom'

    def test_json(self):
        """COMPARER CUSTOM JSON TESTS"""
        test.auto_run_json_tests('POST', self)


###################################################################################################
# Downloader
###################################################################################################

class Downloader(FirmwareUpdateTest):
    """Tests for Downloader Endpoint"""

    ENDPOINT = 'downloader'

    def test_bad_data(self):
        """DOWNLOADER BAD DATA TESTS"""
        test.bad_data('GET', self)
    
    def test_json(self):
        """DOWNLOADER JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# UCI
###################################################################################################

class UCI(FirmwareUpdateTest):
    """Tests for UCI Endpoint"""

    ENDPOINT = 'uci'

    def test_json(self):
        """UCI JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# UCI SI
###################################################################################################

class UCISI(FirmwareUpdateTest):
    """Tests for UCI SI Endpoint"""

    ENDPOINT = 'uci_si'

    def test_json(self):
        """UCI SI JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Updater
###################################################################################################

class Updater(FirmwareUpdateTest):
    """Tests for Updater Endpoint"""

    ENDPOINT = 'updater'

    def test_json(self):
        """UPDATER JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Updater DUP
###################################################################################################

class UpdaterDUP(FirmwareUpdateTest):
    """Tests for Updater DUP Endpoint"""

    ENDPOINT = 'updater_dup'

    def test_json(self):
        """UPDATER DUP JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Updater Status
###################################################################################################

class UpdaterStatus(FirmwareUpdateTest):
    """Tests for Updater Status Endpoint"""

    ENDPOINT = 'updater_status'

    def test_json(self):
        """UPDATER STATUS JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Updater TestCallback
###################################################################################################

class UpdaterTestCallback(FirmwareUpdateTest):
    """Tests for Updater TestCallback Endpoint"""

    ENDPOINT = 'updater_testCallback'

    def test_json(self):
        """UPDATER TESTCALLBACK JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Version
###################################################################################################

class Version(FirmwareUpdateTest):
    """Tests for Version Endpoint"""

    ENDPOINT = 'version'

    def test_json(self):
        """VERSION JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()

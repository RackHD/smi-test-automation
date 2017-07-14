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
@unittest.skip("Not Implemented")
class Comparer(FirmwareUpdateTest):
    """Tests for Comparer Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'comparer'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """COMPARER JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# Comparer Catalog
###################################################################################################
@unittest.skip("Not Implemented")
class ComparerCatalog(FirmwareUpdateTest):
    """Tests for Comparer Catalog Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'comparer_catalog'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """COMPARER CATALOG JSON TESTS"""
        test.run_json('POST', self)
    
    def test_01(self):
        """Compare this catalog to identical catalog in different directory"""
        # First, download a second catalog to use for the comparison
        dl_payload = json.endpoint_load_base_payload(self.JSON_FILE, 'downloader')
        dl_payload["targetLocation"] = "%2F/temp2%2F"
        url = self.BASE_URL + json.endpoint_load_path(self.JSON_FILE, 'downloader')
        http.rest_get(url, dl_payload)
        # Second, get the details for the comparison function
        response = http.rest_post(self.URL, json.get_base_payload(self))

###################################################################################################
# Comparer Custom
###################################################################################################
@unittest.skip("Not Implemented")
class ComparerCustom(FirmwareUpdateTest):
    """Tests for Comparer Custom Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'comparer_custom'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """COMPARER CUSTOM JSON TESTS"""
        test.run_json('POST', self)


###################################################################################################
# Downloader
###################################################################################################
# @unittest.skip("Too Slow")
class Downloader(FirmwareUpdateTest):
    """Tests for Downloader Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'downloader'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_bad_data(self):
        """DOWNLOADER BAD DATA TESTS"""
        test.bad_data('GET', self)
    @unittest.skip("Too Slow")
    def test_json(self):
        """DOWNLOADER JSON TESTS"""
        test.run_json('GET', self)

###################################################################################################
# UCI
###################################################################################################
@unittest.skip("Not Implemented")
class UCI(FirmwareUpdateTest):
    """Tests for UCI Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'uci'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """UCI JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# UCI SI
###################################################################################################
@unittest.skip("Not Implemented")
class UCISI(FirmwareUpdateTest):
    """Tests for UCI SI Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'uci_si'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """UCI SI JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# Updater
###################################################################################################
@unittest.skip("Not Implemented")
class Updater(FirmwareUpdateTest):
    """Tests for Updater Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'updater'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """UPDATER JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# Updater DUP
###################################################################################################
@unittest.skip("Not Implemented")
class UpdaterDUP(FirmwareUpdateTest):
    """Tests for Updater DUP Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'updater_dup'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """UPDATER DUP JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# Updater Status
###################################################################################################
@unittest.skip("Not Implemented")
class UpdaterStatus(FirmwareUpdateTest):
    """Tests for Updater Status Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'updater_status'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """UPDATER STATUS JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# Updater TestCallback
###################################################################################################
@unittest.skip("Not Implemented")
class UpdaterTestCallback(FirmwareUpdateTest):
    """Tests for Updater TestCallback Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'updater_testcallback'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """UPDATER TESTCALLBACK JSON TESTS"""
        test.run_json('POST', self)

###################################################################################################
# Version
###################################################################################################

class Version(FirmwareUpdateTest):
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

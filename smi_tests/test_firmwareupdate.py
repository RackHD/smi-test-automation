# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
'''

import unittest
import sys
import logging
import auto_test
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

    HOST = auto_test.HOST
    PORT = '46010'
    DATA = auto_test.DATA
    JSON_NAME = 'data_firmwareupdate.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(cls.HOST, host_override)
        cls.DATA = json.select_directory(cls.DATA, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DATA, cls.JSON_NAME)

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
        """Run tests specified in JSON"""
        test.get_json(self)

###################################################################################################
# Downloader
###################################################################################################
@unittest.skip("Downloader is broken")
class Downloader(FirmwareUpdateTest):
    """Tests for Downloader Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'downloader'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_bad_data(self):
        """Run tests with missing or empty data, check for failure"""
        test.get_bad_data(self)

    def test_json(self):
        """Run tests specified in JSON"""
        test.get_json(self)

###################################################################################################
# Comparer
###################################################################################################
@unittest.skip("Compare has not been implemented yet")
class Comparer(FirmwareUpdateTest):
    """Tests for Comparer Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'comparer'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    def test_json(self):
        """Run tests specified in JSON"""
        test.post_json(self)

###################################################################################################
# Comparer Catalog
###################################################################################################
@unittest.skip("Compare has not been implemented yet")
class ComparerCatalog(FirmwareUpdateTest):
    """Tests for Comparer Catalog Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'comparer_catalog'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

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
# Placeholder
###################################################################################################

if __name__ == "__main__":
    HOST, DATA = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()

# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
'''

import unittest
import sys
import logging
from toolkit import http, json, log, test

LOG = logging.getLogger(__name__)
# Leave as None to use default Host
HOST_OVERRIDE = '100.68.125.170'
# Leave as None to use default json directory
DIRECTORY_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin Firmware Update Tests")
    FirmwareUpdateTest.initialize_data(HOST_OVERRIDE, DIRECTORY_OVERRIDE)

class FirmwareUpdateTest(unittest.TestCase):
    """Collection of data to test the firmware update microservice"""

    HOST = 'localhost' # will grab default from elsewhere
    PORT = '46010'
    DIRECTORY = 'request_data' # will grab default from elsewhere
    JSON_NAME = 'request_firmwareupdate.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initialize base url and json file path"""
        cls.HOST = http.select_host(cls.HOST, host_override)
        cls.DIRECTORY = json.select_directory(cls.DIRECTORY, directory_override)
        cls.BASE_URL = http.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = json.create_json_reference(cls.DIRECTORY, cls.JSON_NAME)

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

    @log.exception(LOG)
    def test_test(self):
        dicto = {"fileName": "Catalog.xml.gz",
                "fileUrl": "ftp.dell.com%2Fcatalog",
                "targetLocation": "%2Ftemp%2F"}
        print("\n\n")
        for combo in test.bad_parameter_combos(dicto):
            print(combo)
            print("\n")

    @unittest.skip("debugging")
    @log.exception(LOG)
    def test_json(self):
        """Run tests specified in JSON"""
        for test_case in json.get_all_tests(self):
            skip, description, payload, expected = json.parse_test(self, test_case)
            if skip:
                print(skip)
            else:
                response = http.rest_get(self.URL, payload)
                with self.subTest(test=description):
                    self.assertTrue(test.compare_response(response, expected), "Bad Response")

###################################################################################################
# Downloader
###################################################################################################
@unittest.skip("debugging")
class Downloader(FirmwareUpdateTest):
    """Tests for Downloader Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'downloader'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    @log.exception(LOG)
    def test_bad_params(self):
        """Make a request to downloader with missing or empty parameters, check for failure"""
        for combo in test.bad_parameter_combos(json.get_base_payload(self)):
            response = http.rest_get(self.URL, combo)
            with self.subTest(parameters=combo):
                self.assertTrue(test.has_status_code(response, 400), "Expected Response Code : 400")

    @log.exception(LOG)
    def test_json(self):
        """Run tests specified in JSON"""
        for test_case in json.get_all_tests(self):
            skip, description, payload, expected = json.parse_test(self, test_case)
            if skip:
                print(skip)
            else:
                response = http.rest_get(self.URL, payload)
                with self.subTest(test=description):
                    self.assertTrue(test.compare_response(response, expected), "Bad Response")


###################################################################################################
# Comparer
###################################################################################################
@unittest.skip("debugging")
class Comparer(FirmwareUpdateTest):
    """Tests for Comparer Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'comparer'
        cls.URL = cls.BASE_URL + json.endpoint_load_path(cls.JSON_FILE, cls.ENDPOINT)

    @log.exception(LOG)
    def test_json(self):
        """Run tests specified in JSON"""
        for test_case in json.get_all_tests(self):
            skip, description, payload, expected = json.parse_test(self, test_case)
            if skip:
                print(skip)
            else:
                response = http.rest_post(self.URL, payload)
                with self.subTest(test=description):
                    self.assertTrue(test.compare_response(response, expected), "Bad Response")

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

    @log.exception(LOG)
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
    ARGS = sys.argv[1:].copy()
    if ARGS:
        HOST_OVERRIDE = ARGS.pop(0)
        LOG.info("Host Override : %s", HOST_OVERRIDE)
        sys.argv.pop()
        if ARGS:
            DIRECTORY_OVERRIDE = ARGS.pop(0)
            LOG.info("Directory Override : %s", DIRECTORY_OVERRIDE)
            sys.argv.pop()

    log.configure_logger_from_yaml('../logs/logger_config.yml')
    unittest.main()

# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
'''

import unittest
import sys
import logging
from toolkit import http, json, logger, testing

LOG = logging.getLogger(__name__)
# Leave as None to use default Host
HOST_OVERRIDE = '100.68.125.170'
# Leave as None to use default json directory
DIRECTORY_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
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

########################################################################
# Version
########################################################################

class Version(FirmwareUpdateTest):
    """Tests for Version Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'version'
        cls.path, cls.param, cls.payload = json.load_inital_test_data(cls.JSON_FILE, cls.ENDPOINT)
        cls.URL = cls.BASE_URL + cls.path

    @logger.exception(LOG)
    def test_01(self):
        """Make a request to get version, check for success"""
        response = http.rest_get(self.URL)
        LOG.info("Response Status Code: %s", response.status_code)
        self.assertEqual(response.status_code, 200, "Response code should equal 200")

########################################################################
# Downloader
########################################################################

class Downloader(FirmwareUpdateTest):
    """Tests for Downloader Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'downloader'
        cls.path, cls.param, cls.payload = json.load_inital_test_data(cls.JSON_FILE, cls.ENDPOINT)
        cls.URL = cls.BASE_URL + cls.path

    @logger.exception(LOG)
    def test_01(self):
        """Make a request to downloader with valid parameters, check for success"""
        query_url = http.add_query_parameters(self.URL, self.param)
        LOG.info("Query: %s", query_url)
        response = http.rest_get(query_url)
        LOG.info("Response Status Code: %s", response.status_code)
        self.assertEqual(response.status_code, 200, "Response code should equal 200")

    @logger.exception(LOG)
    def test_02(self):
        """Make a request to downloader with missing parameters, check for failure"""
        for param_combo in http.missing_parameter_combinations(self.param):
            query_url = http.add_query_parameters(self.URL, param_combo)
            LOG.info("Query: %s", query_url)
            response = http.rest_get(query_url)
            LOG.info("Response Status Code: %s", response.status_code)
            with self.subTest(parameters=param_combo):
                self.assertEqual(response.status_code, 400, "Response code should equal 400")

    @logger.exception(LOG)
    def test_03(self):
        """Make a request to downloader with empty parameters, check for failure"""
        for param_combo in http.empty_parameter_combinations(self.param):
            query_url = http.add_query_parameters(self.URL, param_combo)
            LOG.info("Query: %s", query_url)
            response = http.rest_get(query_url)
            LOG.info("Response Status Code: %s", response.status_code)
            with self.subTest(parameters=param_combo):
                self.assertEqual(response.status_code, 400, "Response code should equal 400")

########################################################################
# Comparer
########################################################################

class Comparer(FirmwareUpdateTest):
    """Tests for Comparer Endpoint"""
    @classmethod
    def setUpClass(cls):
        """Load initial test data from json"""
        cls.ENDPOINT = 'comparer'
        cls.path, cls.param, cls.payload = json.load_inital_test_data(cls.JSON_FILE, cls.ENDPOINT)
        cls.URL = cls.BASE_URL + cls.path

    @logger.exception(LOG)
    def test_01(self):
        """Make a request to comparer with valid parameters, check for success"""
        response = http.rest_post(self.URL, self.payload)
        LOG.info("Response Status Code: %s", response.status_code)
        self.assertEqual(response.status_code, 200, "Response code should equal 200")

    @logger.exception(LOG)
    def test_02(self):
        """Make a request to comparer with invalid IP, check for failure"""
        bad_payload = json.load_test_payload(self.JSON_FILE, self.ENDPOINT, 1)
        response = http.rest_post(self.URL, bad_payload)
        LOG.info("Response Status Code: %s", response.status_code)
        self.assertEqual(response.status_code, 400, "Response code should equal 400")

    def test_03(self):
        """Make a request to comparer with invalid username and password, check for failure"""
        bad_payload = json.load_test_payload(self.JSON_FILE, self.ENDPOINT, 2)
        response = http.rest_post(self.URL, bad_payload)
        LOG.info("Response Status Code: %s", response.status_code)
        self.assertEqual(response.status_code, 400, "Response code should equal 400")

    def test_04(self):
        """Make a request to comparer with invalid catalog path, check for failure"""
        bad_payload = json.load_test_payload(self.JSON_FILE, self.ENDPOINT, 3)
        response = http.rest_post(self.URL, bad_payload)
        LOG.info("Response Status Code: %s", response.status_code)
        self.assertEqual(response.status_code, 400, "Response code should equal 400")

'''
@unittest.skip("Compare has not been implemented yet")
class CompareCatalogs(FirmwareUpdateTest):
    @classmethod
    def setUpClass(cls):
        """Initalize base url"""
        service_url = '/api/1.0/server/firmware/comparer/catalog'
        cls.URL = cls.BASE_URL + service_url

    def setUp(self):
        print("")
        self.ext, self.param, self.payload = json.load_test_data(self.JSON_FILE, 'compareCatalogs')

    def test0300_CompareSameCatalogs(self):
        try:
            # First, download a second catalog to use for the comparison
            dl_ext, dl_param, dl_payload = json.load_test_data(self.JSON_FILE, 'getDownloader')
            dl_param["targetLocation"] = "%2F/temp2%2F"
            dl_url = self.BASE_URL + dl_ext
            # Tack on query parameters to end of URL
            query_url = http.add_query_parameters(dl_url, dl_param)
            response = http.rest_get(query_url)
            # Second, get the details for the comparison function
            response = http.rest_post(self.URL, self.payload)

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc
'''
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

    logger.configure_logger_from_yaml('../logs/logger_config.yml')
    unittest.main()

# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
'''

import unittest
import sys
import os
import logging
from toolkit import httptools, jsontools, logtools

LOG = logging.getLogger(__name__)
# Leave as None to use default Host
HOST_OVERRIDE = '100.68.125.170'
# Leave as None to use default json directory
DIRECTORY_OVERRIDE = None

def setUpModule():
    FirmwareUpdateTest.initialize_data(HOST_OVERRIDE, DIRECTORY_OVERRIDE)

class FirmwareUpdateTest(unittest.TestCase):
    """Collection of data to test the firmware update microservice"""

    HOST = 'localhost' # will grab default from elsewhere
    PORT = '46010'
    DIRECTORY = '../request_data' # will grab default from elsewhere
    JSON_NAME = 'request_firmwareupdate.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override):
        """Initalize base url"""
        cls.HOST = httptools.select_host(cls.HOST, host_override)
        cls.DIRECTORY = jsontools.select_directory(cls.DIRECTORY, directory_override)
        cls.BASE_URL = httptools.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = jsontools.create_json_reference(cls.DIRECTORY, cls.JSON_NAME)

########################################################################
# Test Get Version

class GetVersion(FirmwareUpdateTest):
    """Get Version Test"""
    @classmethod
    def setUpClass(cls):
        """Initalize base url"""
        service_url = '/api/1.0/server/firmware/version'
        cls.URL = cls.BASE_URL + service_url

    def setUp(self):
        print("")
        self.extention, self.parameters, self.payload = jsontools.load_test_data(self.JSON_FILE, 'getVersion')

    def test0001_GetVersion(self):
        try:
            response = httptools.rest_get(self.URL)
            LOG.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

########################################################################
# Test Get Downloader
class GetDownloader(FirmwareUpdateTest):

    @classmethod
    def setUpClass(cls):
        """Initalize base url"""
        service_url = '/api/1.0/server/firmware/downloader'
        cls.URL = cls.BASE_URL + service_url

    def setUp(self):
        print("")
        self.extention, self.parameters, self.payload = jsontools.load_test_data(self.JSON_FILE, 'getDownloader')

    def test0100_GetDownloaderWithAllParams(self):
        # Positive test case - Test passing in all valid data for the query strings
        try:
            # Tack on query parameters to end of URL
            query_url = httptools.add_query_parameters(self.URL, self.parameters)
            print(query_url)
            response = httptools.rest_get(query_url)
            LOG.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

    def test0101_GetDownloaderWithMissingParameter(self):
        # Negative test case - Remove each parameter one by one and verify a 400 is returned
        try:
            # Loop through each parameter and remove it
            for param_combo in httptools.missing_parameter_combinations(self.parameters):
                # Tack on query parameters to end of URL
                query_url = httptools.add_query_parameters(self.URL, param_combo)
                response = httptools.rest_get(query_url)
                LOG.info("Response Status Code: " + str(response.status_code))
                self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

    def test0102_GetDownloaderWithInvalidParameter(self):
        # Negative test case - Set each parameter to an invalid value and verify a 400 is returned
        try:
            # Loop through each parameter and empty it
            for param_combo in httptools.empty_parameter_combinations(self.parameters):
                # Tack on query parameters to end of URL
                query_url = httptools.add_query_parameters(self.URL, param_combo)
                response = httptools.rest_get(query_url)
                LOG.info("Response Status Code: " + str(response.status_code))
                self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc


class GetApplicableUpdates(FirmwareUpdateTest):

    @classmethod
    def setUpClass(cls):
        """Initalize base url"""
        service_url = '/api/1.0/server/firmware/comparer'
        cls.URL = cls.BASE_URL + service_url

    def setUp(self):
        print("")
        self.extention, self.parameters, self.payload = jsontools.load_test_data(self.JSON_FILE, 'getApplicableUpdates')

    def test0200_GetApplicableUpdatesWithValidPayload(self):
        try:
            # Positive test case - Test passing in all valid data for payload
            response = httptools.rest_post(self.URL, self.payload)
            LOG.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

    def test0201_GetApplicableUpdatesWithInvalidIP(self):
        try:
            # Negative test case - Test passing invalid system IP for the payload
            bad_payload = self.payload.copy()
            bad_payload["serverAddress"] = "100.100.100.100"
            response = httptools.rest_post(self.URL, bad_payload)
            LOG.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

    def test0202_GetApplicableUpdatesWithBadCredentials(self):
        try:
            # Negative test case - Test passing invalid credentials for the payload
            bad_payload = self.payload.copy()
            bad_payload["userName"] = "foo"
            bad_payload["password"] = "bar"
            response = httptools.rest_post(self.URL, bad_payload)
            LOG.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

    def test0203_GetApplicableUpdatesWithBadCatalog(self):
        try:
            # Negative test case - Test passing invalid catalog for the payload
            bad_payload = self.payload.copy()
            bad_payload["catalogPath"] = "/foo/cat.xml"
            response = httptools.rest_post(self.URL, bad_payload)
            LOG.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

@unittest.skip("Compare has not been implemented yet")
class CompareCatalogs(FirmwareUpdateTest):
    @classmethod
    def setUpClass(cls):
        """Initalize base url"""
        service_url = '/api/1.0/server/firmware/comparer/catalog'
        cls.URL = cls.BASE_URL + service_url

    def setUp(self):
        print("")
        self.extention, self.parameters, self.payload = jsontools.load_test_data(self.JSON_FILE, 'compareCatalogs')

    def test0300_CompareSameCatalogs(self):
        try:
            # First, download a second catalog to use for the comparison
            dl_extention, dl_parameters, dl_payload = jsontools.load_test_data(self.JSON_FILE, 'getDownloader')
            dl_parameters["targetLocation"] = "%2F/temp2%2F"
            dl_url = self.BASE_URL + dl_extention
            # Tack on query parameters to end of URL
            query_url = httptools.add_query_parameters(dl_url, dl_parameters)
            response = httptools.rest_get(query_url)
            # Second, get the details for the comparison function
            response = httptools.rest_post(self.URL, self.payload)

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

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

    logtools.configure_logger_from_yaml('../logs/logger_config.yml')
    unittest.main()

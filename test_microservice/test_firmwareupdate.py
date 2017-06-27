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


class GetVersion(FirmwareUpdateTest):
    """Get Version Test"""
    @classmethod
    def setUpClass(cls):
        """Initalize base url"""
        service_url = '/api/1.0/server/firmware/version'
        cls.URL = cls.BASE_URL + service_url

    def setUp(self):
        print("")

    ########################################################################
    # Test GET Version

    def test0001_GetVersion(self):
        try:
            extention, parameters, payload = jsontools.load_test_data(self.JSON_FILE, 'getVersion')
            response = httptools.rest_get(self.BASE_URL + extention)
            LOG.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as exc:
            LOG.error("Exception: " + str(exc))
            raise exc

"""
class GetDownloader(FirmwareUpdateTest):

    def setUp(self):
        print("")

    ########################################################################
    # Test GET Downloader
    def test0100_GetDownloaderWithAllParams(self):
        try:
            # Positive test case - Test passing in all valid data for the query strings
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            # Tack on query parameters to end of URL
            url = FirmwareUpdateHandler().addQueryParameters(url, parameters)
            response = FirmwareUpdateHandler().makeGetRestCall(url)
            logger.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1
    
    def test0101_GetDownloaderWithMissingParameter(self):
        try:
            # Negative test case - Remove each parameter one by one and verify a 400 is returned
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            origUrl = url
            origParams = dict.copy(parameters)
            
            # Loop through each parameter and remove it
            for index, key in enumerate(origParams):
                del parameters[key]
                # Tack on query parameters to end of URL
                url = FirmwareUpdateHandler().addQueryParameters(url, parameters)
                response = FirmwareUpdateHandler().makeGetRestCall(url)
                logger.info("Response Status Code: " + str(response.status_code))
                self.assertEqual(response.status_code, 400, "Response code should equal 400")
                # reset for next run
                url = origUrl
                parameters = dict.copy(origParams)

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1

    def test0102_GetDownloaderWithInvalidParameter(self):
        try:
            # Negative test case - Set each parameter to an invalid value and verify a 400 is returned
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            origUrl = url
            origParams = dict.copy(parameters)
            
            # Loop through each parameter and make it an empty string
            for index, key in enumerate(origParams):
                parameters[key] = " "
                # Tack on query parameters to end of URL
                url = FirmwareUpdateHandler().addQueryParameters(url, parameters)
                response = FirmwareUpdateHandler().makeGetRestCall(url)
                logger.info("Response Status Code: " + str(response.status_code))
                self.assertEqual(response.status_code, 400, "Response code should equal 400")
                # reset for next run
                url = origUrl
                parameters = dict.copy(origParams)  

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1
class GetApplicableUpdates(FirmwareUpdateTest):

    def setUp(self):
        print("")

    def test0200_GetApplicableUpdatesWithValidPayload(self):
        try:
            # Positive test case - Test passing in all valid data for payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getApplicableUpdates")
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1

    def test0201_GetApplicableUpdatesWithInvalidIP(self):
        try:
            # Negative test case - Test passing invalid system IP for the payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getApplicableUpdates")
            payload["serverAddress"] = "100.100.100.100"
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1

    def test0202_GetApplicableUpdatesWithBadCredentials(self):
        try:
            # Negative test case - Test passing invalid credentials for the payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getApplicableUpdates")
            payload["userName"] = "foo"
            payload["password"] = "bar"
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1

    def test0203_GetApplicableUpdatesWithBadCatalog(self):
        try:
            # Negative test case - Test passing invalid catalog for the payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getApplicableUpdates")
            payload["catalogPath"] = "/foo/cat.xml"
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1

@unittest.skip("Compare has not been implemented yet")
class CompareCatalogs(FirmwareUpdateTest):
    def setUp(self):
        print("")

    def test0300_CompareSameCatalogs(self):
        try:
            # First, download a second catalog to use for the comparison
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            parameters["targetLocation"] = "%2F/temp2%2F"
            # Tack on query parameters to end of URL
            url = FirmwareUpdateHandler().addQueryParameters(url, parameters)
            response = FirmwareUpdateHandler().makeGetRestCall(url)

            # Second, get the details for the comparison function
            url, parameters, payload = FirmwareUpdateHandler().getTestData("compareCatalogs")
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1
"""
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

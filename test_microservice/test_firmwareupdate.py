# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
'''

import json
import unittest
import sys
import os
import logging
from .handlers import 

logger = logging.getLogger(__name__)

class FirmwareUpdateTest(unittest.TestCase):

    def setUp(self):
        print("")

    ########################################################################
    # Test GET Version
    
    def test0001_GetVersion(self):
        try:
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getVersion")
            response = FirmwareUpdateHandler().makeGetRestCall(url)
            logger.info("Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1

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
    '''
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
    '''

if __name__=="__main__":
    if len(sys.argv) > 1:
        FirmwareUpdateHandler.host = sys.argv.pop()
        FirmwareUpdateHandler.directory = sys.argv.pop() + "/"
    else:
        # FirmwareUpdateHandler.host = "http://100.68.123.238:46010"
        FirmwareUpdateHandler.host = "http://localhost:46010"

        FirmwareUpdateHandler.directory = "../requestdata/"

    from test_manager import run_tests
    run_tests('FWUP')

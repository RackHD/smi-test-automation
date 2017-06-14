'''
Created on June 5, 2017
@author: Michael Regert
'''

import json
import unittest
import sys
import os
import sys
run_dir=os.path.abspath(os.path.dirname(__file__))
current_dir = os.getcwd()
os.chdir(run_dir)
sys.path.insert(0,os.path.abspath('../utility'))
sys.path.append(os.path.abspath('../handlers'))

from UtilBase import Utility
from FirmwareUpdateMicroservice import FirmwareUpdateHandler

class FirmwareUpdateTest(unittest.TestCase):
    global logger
    logger = Utility().getLoggerInstance()

    ########################################################################
    # Test GET Version
    def test0001_GetVersion(self):
        try:
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getVersion")
            response = FirmwareUpdateHandler().makeGetRestCall(url)
            logger.info("FirmwareUpdateTest: test001_GetVersion(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("FirmwareUpdateTest: test001_GetVersion():  Exception: " + str(e1))
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
            logger.info("FirmwareUpdateTest: test0100_GetDownloaderWithAllParams(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("FirmwareUpdateTest: test0100_GetDownloaderWithAllParams():  Exception: " + str(e1))
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
                logger.info("FirmwareUpdateTest: test0101_GetDownloaderWithMissingParameter(): Response Status Code: " + str(response.status_code))
                self.assertEqual(response.status_code, 400, "Response code should equal 400")
                # reset for next run
                url = origUrl
                parameters = dict.copy(origParams)

        except Exception as e1:
            logger.error("FirmwareUpdateTest: test0101_GetDownloaderWithMissingParameter():  Exception: " + str(e1))
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
                logger.info("FirmwareUpdateTest: test0102_GetDownloaderWithInvalidParameter(): Response Status Code: " + str(response.status_code))
                self.assertEqual(response.status_code, 400, "Response code should equal 400")
                # reset for next run
                url = origUrl
                parameters = dict.copy(origParams)  

        except Exception as e1:
            logger.error("FirmwareUpdateTest: test0102_GetDownloaderWithInvalidParameter():  Exception: " + str(e1))
            raise e1

    def test 0200_GetApplicableUpdatesWithValidPayload(self):
        try:
            # Positive test case - Test passing in all valid data for payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("FirmwareUpdateTest: 0200_GetApplicableUpdatesWithValidPayload(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("FirmwareUpdateTest: 0200_GetApplicableUpdatesWithValidPayload():  Exception: " + str(e1))
            raise e1

    def test 0201_GetApplicableUpdatesWithInvalidIP(self):
        try:
            # Negative test case - Test passing invalid system IP for the payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            payload["serverAddress"] = "100.100.100.100"
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("FirmwareUpdateTest: 0201_GetApplicableUpdatesWithInvalidIP(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as e1:
            logger.error("FirmwareUpdateTest: 0201_GetApplicableUpdatesWithInvalidIP():  Exception: " + str(e1))
            raise e1

    def test 0202_GetApplicableUpdatesWithBadCredentials(self):
        try:
            # Negative test case - Test passing invalid credentials for the payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            payload["userName"] = "foo"
            payload["password"] = "bar"
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("FirmwareUpdateTest: 0202_GetApplicableUpdatesWithBadCredentials(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as e1:
            logger.error("FirmwareUpdateTest: 0202_GetApplicableUpdatesWithBadCredentials():  Exception: " + str(e1))
            raise e1

    def test 0203_GetApplicableUpdatesWithBadCatalog(self):
        try:
            # Negative test case - Test passing invalid catalog for the payload
            url, parameters, payload = FirmwareUpdateHandler().getTestData("getDownloader")
            payload["catalogPath"] = "/foo/cat.xml"
            response = FirmwareUpdateHandler().makePostRestCall(url, payload)
            logger.info("FirmwareUpdateTest: 0203_GetApplicableUpdatesWithBadCatalog(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as e1:
            logger.error("FirmwareUpdateTest: 0202_GetApplicableUpdatesWithBadCredentials():  Exception: " + str(e1))
            raise e1

if __name__=="__main__":
    if len(sys.argv) > 1:
        FirmwareUpdateHandler.host = sys.argv.pop()
        FirmwareUpdateHandler.directory = sys.argv.pop() + "/"
    else:
        FirmwareUpdateHandler.host = "http://100.68.123.238:46010"
        #FirmwareUpdateHandler.host = "http://localhost:46010"

        FirmwareUpdateHandler.directory = "../requestdata/"

    unittest.main()

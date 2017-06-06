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
    # Test Get Version
    def test001_GetVersion(self):
        try:
            response = FirmwareUpdateHandler().getVersion()
            logger.info("FirmwareUpdateTest: test001_GetVersion(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("FirmwareUpdateTest: test001_GetVersion():  Exception: " + str(e1))
            raise e1

    ########################################################################
    # Test Get Catalog
    def test002_GetCatalog(self):
        try:
            fileName  = 'Catalog.xml.gz'
            fileUrl   = 'ftp.dell.com/catalog'
            targetLoc = '/temp/'
            response  = FirmwareUpdateHandler().getCatalog([fileName, fileUrl, targetLoc])
            logger.info("FirmwareUpdateTest: test002_GetCatalog(): Response Status Code: " + str(response.status_code))           
            logger.info("FirmwareUpdateTest: test002_GetCatalog(): Response Text: " + response.text)

            # Check that the call returns a 200 (Success)
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

            # Check that the file name returned is what we passed in
            responseJson = json.loads(response.text)
            self.assertEqual(responseJson["name"], fileName, "Returned filename should match what was passed in")


        except Exception as e1:
            logger.error("FirmwareUpdateTest: test002_GetCatalog():  Exception: " + str(e1))
            raise e1

if __name__=="__main__":
    if len(sys.argv) > 1:
        FirmwareUpdateHandler.host = sys.argv.pop()
    else:
        FirmwareUpdateHandler.host = "http://localhost:46010"

    unittest.main()

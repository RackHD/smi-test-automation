# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 4, 2017

@author: Michael Regert, Michael Hepfer
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
from VirtualIdentityMicroservice import VirtualIdentityHandler

class VirtualIdentityTest(unittest.TestCase):
    
    global logger
    logger = Utility().getLoggerInstance()
    global networkId
    networkId = 0
    networkJson = ""

    ########################################################################
    # Test that Get Virtual Identities returns an empty list when empty
    def test001_GetVirtualIdentitiesEmpty(self):
        try:
            response = VirtualIdentityHandler().getVirtualIdentities()
            logger.info("VirtualIdentitiesTest: test001_GetVirtualIdentitiesEmpty(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

            logger.info("VirtualIdentitiesTest: test001_GetVirtualIdentitiesEmpty(): Response Text: " + response.text)
            responseJson = json.loads(response.text)
            #assert here
            self.assertEqual(responseJson["pagination"]["total"], 0, "Pagination total count should be 0")
            self.assertEqual(responseJson["pages"]["total"], 0, "Pages total count should be 0")

        except Exception as e1:
            logger.error("VirtualIdentitiesTest: test001_GetVirtualIdentitiesEmpty():  Exception: " + str(e1))
            raise e1



if __name__=="__main__":
    if len(sys.argv) > 1:
        VirtualIdentityHandler.host = sys.argv.pop()
    else:
        VirtualIdentityHandler.host = "http://localhost:46015"

    from run_tests import run_tests
    run_tests('VID')
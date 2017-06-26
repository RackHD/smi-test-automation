# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: mkowkab
'''
import json
import os
import unittest
import sys
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handlers.SCPMicroservice import SCPHandler
from utility.UtilBase import Utility

logger = logging.getLogger(__name__)

#from scripts.SMI.utility.UtilBase import Utility
#from scripts.SMI.handlers.SCPMicroservice import SCPHandler
#run_dir=os.path.abspath(os.path.dirname(__file__))
#current_dir = os.getcwd()
#os.chdir(run_dir)
#sys.path.insert(0,os.path.abspath('../utility'))
#sys.path.append(os.path.abspath('../handlers'))
class SCPTest(unittest.TestCase):    

    def setUp(self):
        print("")

    def test_exportSCP(self):        
        try:
            response = SCPHandler().exportSCP()
            logger.info("Response: " + response.text)
             
            task = "export"
             
            requestData, url = SCPHandler().getRequestData(task)
             
            shareIPAddress = requestData["shareAddress"]
            shareName = requestData["shareName"]
            fileName = requestData["fileName"]
             
            logger.info("shareIPAdress: " + shareIPAddress + "  shareName: " + shareName + " fileName: " + fileName)
             
            output = os.path.isfile(shareName+"/"+fileName)
             
            self.assertTrue(output, "Failed to export SCP File from Server " + fileName)
             
             
        except Exception as e:
            logger.error("Exception: " + str(e))
            raise e
        
    def test_importSCP(self):
        try:
            response = SCPHandler().importSCP()
            logger.info("Response: " + response.text)
            jsonResponse = json.loads(response.text)
            idracResponseMessage = jsonResponse["xmlConfig"]["message"]
            expectedMessage = "No changes occurred. Current component configuration matched the requested configuration."
            self.assertEqual(idracResponseMessage, expectedMessage, "IDRAC Message didn't match with the Expected message")
            
            idracJobID = jsonResponse["xmlConfig"]["jobID"]
            self.assertIsNotNone(idracJobID, "No IDRAC JOBID returned for Import SCP task.")
            
            responseSuccess = jsonResponse["xmlConfig"]["result"]  
            self.assertEqual(responseSuccess, "SUCCESS", "Response is not SUCCESS for Import SCP task.")   
            
        except Exception as e:
            logger.error("Exception: " + str(e))
            raise e
        
    def test_getComponents(self):
        try:
            response = SCPHandler().getComponents()
            logger.info("Response: " + response.text)
            jsonResponse = json.loads(response.text)
            
            responseComponentName = jsonResponse["serverComponents"][0]["fqdd"]
            
            task = "getComponents"             
            requestData, url = SCPHandler().getRequestData(task)
            expectedComponentName = requestData["componentNames"][0]
            
            self.assertEqual(responseComponentName, expectedComponentName, "ComponentName retunred from the IDRAC didn't match")
            
        except Exception as e:
            raise e
            
        
if __name__=="__main__":
    if len(sys.argv) > 1:
        SCPMicroserviceTest.host = sys.argv.pop()
    else:
        SCPMicroserviceTest.host = "http://localhost:46018"
    from test_manager import run_tests
    run_tests('SCP')

    
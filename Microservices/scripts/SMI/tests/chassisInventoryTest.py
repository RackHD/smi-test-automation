# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 4, 2017

@author: Prashanth_L_Gowda, Dan_Phelps
'''
import json
import unittest
import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handlers.ChassisInventoryMicroservice import ChassisInventoryHandler
from utility.UtilBase import Utility

logger = logging.getLogger(__name__)

class ChassisInventoryMicroserviceTest(unittest.TestCase):
    

    def testChassisDetail(self):
        try :
            response = ChassisInventoryHandler().Inventory("summary")
            logger.info("ChassisInventoryMicroserviceTest: testChassisDetail: Response: " + response.text)
            responseJson = json.loads(response.text)

            value = "9XLTW52"
            
            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))
            
            if("serviceTag" in responseJson):
                self.assertEqual(responseJson["serviceTag"], value, "CHASSIS summary missing/incomplete in response from Inventory Microservice")
            else:
                self.assertFalse(True, "CHASSIS summary missing/incomplete in response from Inventory Microservice")
            
            
        except Exception as e1:
            logger.error("ChassisInventoryMicroserviceTest: testChassisDetail:  Exception: " + str(e1))
            raise e1      


    def testDetails(self):
        try :
            response = ChassisInventoryHandler().Inventory("details")
            logger.info("ChassisInventoryMicroserviceTest: testChassisSummary: Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))
               
            if("chassisControllers" in responseJson):
                self.assertTrue(len(responseJson["chassisControllers"]) > 0, "CHASSIS details missing/incomplete in response from Inventory Microservice")
            else:
                self.assertFalse(True, "CHASSIS details missing/incomplete in response from Inventory Microservice")

            
        except Exception as e1:
            logger.error("ChassisInventoryMicroserviceTest: testChassisSummary:  Exception: " + str(e1))
            raise e1      
 
if __name__=="__main__":
    if len(sys.argv) > 1:
        ChassisInventoryHandler.host = sys.argv.pop()
    else:
        ChassisInventoryHandler.host = "http://localhost:46001"
    from run_tests import run_tests
    run_tests('CHIN')


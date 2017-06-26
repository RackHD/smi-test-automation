# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 4, 2017

@author: Prashanth_L_Gowda, Dan_Phelps
'''
import json
import unittest
import sys, os
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handlers.ServerInventoryMicroservice import ServerInventoryHandler
from utility.UtilBase import Utility

logger = logging.getLogger(__name__)

class ServerInventoryTest(unittest.TestCase):
    
    def setUp(self):
        print("")

    def testHardware(self):
        try :
            response = ServerInventoryHandler().Inventory("hardware")
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            serviceTag = "17M0D42"
            
            if("system" in responseJson and "serviceTag" in responseJson["system"]):
                self.assertEqual(responseJson["system"]["serviceTag"], serviceTag, "Service Tag doesn't match response returned from Inventory Microservice")
            else:
                self.assertFalse(True, "Service Tag missing in response from Inventory Microservice")
            
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      


    def testSoftware(self):
        try :
            response = ServerInventoryHandler().Inventory("software")
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            value = "Integrated Dell Remote Access Controller"
            
            for obj in responseJson:
                if(obj["elementName"]["value"] == value):
                    return

            self.assertFalse(True, "iDRAC details missing / incomplete in response from Inventory Microservice")
            
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      
            

    def testNics(self):
        try :
            response = ServerInventoryHandler().Inventory("nics")
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            fqdd = "NIC.Integrated.1-1-1"
            
            for obj in responseJson:
                if(obj["fqdd"] == fqdd):
                    return

            self.assertFalse(True, "NIC details missing / incomplete in response from Inventory Microservice")
            
        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      
            

    def testBios(self):
        try :
            response = ServerInventoryHandler().Inventory("bios")
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            if("dcimBIOSEnumerationTypeList" in responseJson and "dcimBIOSIntegerType" in responseJson and "dcimbiosstringType" in responseJson):
                if 0 in (len(responseJson["dcimBIOSEnumerationTypeList"]), len(responseJson["dcimBIOSIntegerType"]), len(responseJson["dcimbiosstringType"])):
                    self.assertFalse(True, "BIOS details missing/incomplete in response from Inventory Microservice")
            else:
                self.assertFalse(True, "BIOS details missing/incomplete in response from Inventory Microservice")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      
            

    def testBoot(self):
        try :
            response = ServerInventoryHandler().Inventory("boot")
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            if("bootSourcesByBootModes" in responseJson and "bootSourcesByBootMode" in responseJson["bootSourcesByBootModes"]):
                if(len(responseJson["bootSourcesByBootModes"]["bootSourcesByBootMode"]) == 0):
                    self.assertFalse(True, "BOOT details missing/incomplete in response from Inventory Microservice")
            else:
                self.assertFalse(True, "BOOT details missing/incomplete in response from Inventory Microservice")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      


    def testLC(self):
        try :
            response = ServerInventoryHandler().Inventory("lc")
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            value = "LifeCycle Log"

            if(len(responseJson) != 0):
                self.assertEqual(responseJson[0]["logName"], value, "LC log details missing/incomplete in response from Inventory Microservice")
            else:
                logger.info("LC log is EMPTY.")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      


    def testSEL(self):
        try :
            response = ServerInventoryHandler().Inventory("sel")
            logger.info("Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            value = "System Event Log Entry"

            if(len(responseJson) != 0):
                self.assertEqual(responseJson[0]["elementName"], value, "SEL log details missing/incomplete in response from Inventory Microservice")
            else:
                logger.info("SEL log is EMPTY.")

        except Exception as e1:
            logger.error("Exception: " + str(e1))
            raise e1      

            
if __name__=="__main__":
    if len(sys.argv) > 1:
        ServerInventoryHandler.host = sys.argv.pop()
    else:
        ServerInventoryHandler.host = "http://localhost:46011"

    unittest.main()

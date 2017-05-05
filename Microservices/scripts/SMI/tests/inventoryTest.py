import json
import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handlers.InventoryMicroservice import InventoryHandler
from utility.UtilBase import Utility


class InventoryMicroserviceTest(unittest.TestCase):
    
    global logger 
    logger = Utility().getLoggerInstance()

    def testHardware(self):
        try :
            response = InventoryHandler().Inventory("hardware")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
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
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      


    def testSoftware(self):
        try :
            response = InventoryHandler().Inventory("software")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
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
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      
            

    def testNics(self):
        try :
            response = InventoryHandler().Inventory("nics")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
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
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      
            

    def testBios(self):
        try :
            response = InventoryHandler().Inventory("bios")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
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
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      
            

    def testBoot(self):
        try :
            response = InventoryHandler().Inventory("boot")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
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
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      


    def testLC(self):
        try :
            response = InventoryHandler().Inventory("lc")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
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
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      


    def testSEL(self):
        try :
            response = InventoryHandler().Inventory("sel")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
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
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      


    def testChassisDetail(self):
        try :
            response = InventoryHandler().Inventory("chassisDetail")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))
               
            if("chassisControllers" in responseJson):
                self.assertTrue(len(responseJson["chassisControllers"]) > 0, "CHASSIS details missing/incomplete in response from Inventory Microservice")
            else:
                self.assertFalse(True, "CHASSIS details missing/incomplete in response from Inventory Microservice")

        except Exception as e1:
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      


    def testChassisSummary(self):
        try :
            response = InventoryHandler().Inventory("chassisSummary")
            logger.info("InventoryMicroserviceTest: testInventory: Response: " + response.text)
            responseJson = json.loads(response.text)

            if("error" in responseJson):
                if(int(responseJson["status"]) > 206):
                    self.assertFalse(True, str(responseJson))

            value = "17JYC42"

            if("serviceTag" in responseJson):
                self.assertEqual(responseJson["serviceTag"], value, "CHASSIS summary missing/incomplete in response from Inventory Microservice")
            else:
                self.assertFalse(True, "CHASSIS summary missing/incomplete in response from Inventory Microservice")

        except Exception as e1:
            logger.error("InventoryMicroserviceTest: testInventory:  Exception: " + str(e1))
            raise e1      
            
            
if __name__=="__main__":
    unittest.main()

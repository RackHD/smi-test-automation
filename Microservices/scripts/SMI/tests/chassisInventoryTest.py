import json
import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handlers.ChassisInventoryMicroservice import ChassisInventoryHandler
from utility.UtilBase import Utility


class ChassisInventoryMicroserviceTest(unittest.TestCase):
    
    global logger 
    logger = Utility().getLoggerInstance()

    def testSummary(self):
        try :
            response = ChassisInventoryHandler().Inventory("summary")
            logger.info("ChassisInventoryMicroserviceTest: testSummary: Response: " + response.text)
            responseJson = json.loads(response.text)

            model = "PowerEdge FX2s"
            serviceTag = "9XLTW52"
            
            self.assertEqual(responseJson["model"], model, "Model doesn't match response returned from Chassis Inventory Microservice")
            self.assertEqual(responseJson["serviceTag"], serviceTag, "Service Tag doesn't match response returned from Chassis Inventory Microservice")
            
        except Exception as e1:
            logger.error("ChassisInventoryMicroserviceTest: testSummary:  Exception: " + str(e1))
            raise e1      


    def testDetails(self):
        try :
            response = ChassisInventoryHandler().Inventory("details")
            logger.info("ChassisInventoryMicroserviceTest: testDetails: Response: " + response.text)
            responseJson = json.loads(response.text)

            value = "CMC-9XLTW52"
            
            self.assertEqual(responseJson["chassisControllers"][0]["name"], value, "Controller name value doesn't match response returned from Chassis Inventory Microservice")
            
        except Exception as e1:
            logger.error("ChassisInventoryMicroserviceTest: testDetails:  Exception: " + str(e1))
            raise e1      
 
if __name__=="__main__":
    unittest.main()

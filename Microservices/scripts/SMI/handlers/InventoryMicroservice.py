import json
import sys

from utility.UtilBase import Utility

class InventoryHandler(Utility):    
    
    def __init__(self):
        global logger
        logger = self.getLoggerInstance()
        global host 
        host = "http://localhost:46011"
        if(len(sys.argv) > 1):
            host = sys.argv[1]
    
    def Inventory(self, task):
        logger.info("InventoryHandler: Inventory")
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result from the Inventory Microservice: \n" + result.text)        
        return result
        
    def getRequestData(self, task):
        logger.info("InventoryTestCase: getRequestData")
        
        with open("../requestdata/inventoryRequestPayload.json") as data_file:
            data = json.load(data_file)
            
            requestData = data["services"][task]["credential"]
            url = host + data["services"][task]["url"]
            return requestData, url
        
if __name__ == "__main__":    
    test = InventoryHandler()
    test.Inventory()            
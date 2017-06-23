# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 4, 2017

@author: Prashanth_L_Gowda, Dan_Phelps
'''
import json
import sys
import logging

from utility.UtilBase import Utility

logger = logging.getLogger(__name__)

class ChassisInventoryHandler(Utility):    
    
    def __init__(self):
        host = "" 
    
    def Inventory(self, task):
        logger.info("ChassisInventoryHandler: ChassisInventory")
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result from the ChassisInventory Microservice: \n" + result.text)        
        return result
        
    def getRequestData(self, task):
        logger.info("ChassisInventoryTestCase: getRequestData")
        
        with open("../requestdata/chassisInventoryRequestPayload.json") as data_file:
            data = json.load(data_file)
            
            requestData = data["services"][task]["credential"]
            url = self.__class__.host + data["services"][task]["url"]
            return requestData, url
        
if __name__ == "__main__":    
    test = ChassisInventoryHandler()
    test.Inventory("summary")
    
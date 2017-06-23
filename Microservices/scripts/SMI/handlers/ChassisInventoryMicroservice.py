# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 4, 2017

@author: Prashanth_L_Gowda, Dan_Phelps
'''
import json
import sys

from utility.UtilBase import Utility

class ChassisInventoryHandler(Utility):    
    
    def __init__(self):
        global logger
        logger = self.getLoggerInstance()
        host = "" 
    
    def Inventory(self, task):
        logger.info("Inventory")
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result " + result.text)        
        return result
        
    def getRequestData(self, task):
        logger.info("getRequestData")
        
        with open("../requestdata/chassisInventoryRequestPayload.json") as data_file:
            data = json.load(data_file)
            
            requestData = data["services"][task]["credential"]
            url = self.__class__.host + data["services"][task]["url"]
            return requestData, url
        
if __name__ == "__main__":    
    test = ChassisInventoryHandler()
    test.Inventory("summary")
    
# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 4, 2017

@author: Prashanth_L_Gowda, Dan_Phelps
'''
import json
import sys
import logging
from . import handler_tools as tools

logger = logging.getLogger(__name__)

class ServerInventoryHandler(Utility):    

    def __init__(self):
        global host

    def Inventory(self, task):
        logger.info("Inventory")
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = get_response(action, url, requestData, headers)
        logger.info("Result " + result.text)
        return result

    def getRequestData(self, task):
        logger.info("getRequestData")

        with open("../requestdata/serverInventoryRequestPayload.json") as data_file:
            data = json.load(data_file)

            requestData = data["services"][task]["credential"]
            url = self.__class__.host + data["services"][task]["url"]
            return requestData, url
        
if __name__ == "__main__":    
    test = ServerInventoryHandler()
    test.Inventory("hardware")
    test.Inventory("software")
    
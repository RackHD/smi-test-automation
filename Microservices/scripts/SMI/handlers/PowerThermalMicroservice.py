# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Rahman Muhammad
'''
import json
import logging

from utility.UtilBase import Utility

logger = logging.getLogger(__name__)

class PowerThermalHandler(Utility):
    
    
    def __init__(self):
        global apiHost
        apiHost = "http://localhost:46019"
        # apiHost = "http://100.68.124.118:46019"
        
    def getAPIVersion(self):
        logger.info("getAPIVersion()")
        task = "getVersion"
        url = apiHost+"/api/1.0/version" 
        #self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "GET"
        result = self.getResponse(action, url,"", headers)
        logger.info("Result " + result.text)        
        return result
    
    
    def getPowerThermal(self):
        logger.info("getPowerThermal() ")
        task = "getPowerThermal"
        #requestData, url = self.getRequestDataWithPayload(task)
        url = apiHost+"/api/1.0/powerthermal"
        
        requestData =  {
                      
                        "serverAddress" : "100.68.124.121",
                        "userName" : "root",
                        "password" : "calvin"
                        } 
        
        headers = {'Content-Type': 'application/json'}
        action ="POST"
        result = self.getResponse(action, url, requestData, headers)
        return result
    
    
    def getRequestDataWithPayload(self, task):
        logger.info("getRequestDataWithPayload")
        
        with open("../requestdata/powerThermalRequestPayload.json") as data_file:
          data = json.load(data_file)
          requestData = data["dell"]["services"][task]["payload"]
          url = data["dell"]["services"][task]["microserviceURL"]
          return requestData, url
       
    def getRequestData(self, task):
        logger.info("getRequestData")
        
        with open("../requestdata/powerThermalRequestPayload.json") as data_file:
            data = json.load(data_file)
            url = data["dell"]["services"][task]["microserviceURL"]
            return url
                  
    
    
       
        
if __name__ == "__main__":
    test = PowerThermalHandler()
    test.getAPIVersion();
    test.getPowerThermal();
            
        

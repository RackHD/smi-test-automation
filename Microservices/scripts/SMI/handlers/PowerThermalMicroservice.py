# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Rahman Muhammad
'''
import json

from utility.UtilBase import Utility


class PowerThermalHandler(Utility):
    
    
    def __init__(self):
        global logger
        global apiHost
        apiHost = "http://localhost:46019"
        # apiHost = "http://100.68.124.118:46019"
        logger = self.getLoggerInstance()
        
    def getAPIVersion(self):
        logger.info("PowerThermalHandler -  getAPIVersion()")
        task = "getVersion"
        url = apiHost+"/api/1.0/version" 
        #self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "GET"
        result = self.getResponse(action, url,"", headers)
        logger.info("Result from getVersion\n" + result.text)        
        return result
    
    
    def getPowerThermal(self):
        logger.info("PowerThermalHandler - getPowerThermal() ")
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
        logger.info("PowerThermalHandler: getRequestDataWithPayload")
        
        with open("../requestdata/powerThermalRequestPayload.json") as data_file:
          data = json.load(data_file)
          requestData = data["dell"]["services"][task]["payload"]
          url = data["dell"]["services"][task]["microserviceURL"]
          return requestData, url
       
    def getRequestData(self, task):
        logger.info("PowerThermalHandler: getRequestData")
        
        with open("../requestdata/powerThermalRequestPayload.json") as data_file:
            data = json.load(data_file)
            url = data["dell"]["services"][task]["microserviceURL"]
            return url
                  
    
    
       
        
if __name__ == "__main__":
    test = PowerThermalHandler()
    test.getAPIVersion();
    test.getPowerThermal();
            
        

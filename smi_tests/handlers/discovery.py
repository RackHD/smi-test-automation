# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Prashanth_L_Gowda
'''
import json
import logging
from . import handler_tools as tools

logger = logging.getLogger(__name__)

class DiscoveryHandler(Utility):    
    
    def __init__(self):
        hots = ""
    
    def discoveryByIPS(self,index):
        logger.info("discoveryByIPS")
        requestData, url = self.getByIpsRequestData()
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        request_json = requestData[index]
        result = get_response(action, url, request_json, headers)
        logger.info("Result from the Discovery Microservice: \n" + result.text)        
        return result

    def discoveryByRange(self,index):
        logger.info("discoverByRange")
        requestData, url = self.getByRangeRequestData()
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        request_json = requestData[index]
        result = get_response(action, url, request_json, headers)
        logger.info("Result from the Discovery Microservice: \n" + result.text)        
        return result

    def getByIpsRequestData(self):
        logger.info("getByIpsRequestData")

        with open("../requestdata/discoveryRequestPayload.json") as data_file:
            data = json.load(data_file)
            
            requestData = data["dell"]["services"]["discoverByIPS"]["payload"]
            url = self.__class__.host + data["dell"]["services"]["discoverByIPS"]["microserviceURL"]
            return requestData, url
    
    def getByRangeRequestData(self):
        logger.info("getByRangeRequestData")
        
        with open("../requestdata/discoveryRequestPayload.json") as data_file:
            data = json.load(data_file)
            
            requestData = data["dell"]["services"]["discoverByRange"]["payload"]
            url = self.__class__.host + data["dell"]["services"]["discoverByRange"]["microserviceURL"]
            return requestData, url
    
        
if __name__ == "__main__":    
    test = DiscoveryHandler()
    test.discoveryByIPS(0) 
    test.discoveryByRange(0)           
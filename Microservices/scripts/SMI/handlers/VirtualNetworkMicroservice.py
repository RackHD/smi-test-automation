# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Michael Regert, Michael Hepfer
'''

import json
import os
import sys

run_dir=os.path.abspath(os.path.dirname(__file__))
current_dir = os.getcwd()
os.chdir(run_dir)
sys.path.insert(0,os.path.abspath('../utility'))

from UtilBase import Utility

class VirtualNetworkHandler(Utility):

    def __init__(self):
        global logger
        logger = self.getLoggerInstance()
        #global host
        #host = ""
        host = ""
        #if(len(sys.argv) > 1):
        #   host = sys.argv[1]
    
    def getNetworks(self): 
        logger.info("getNetworks()")
        requestData, url = self.getRequestData("getNetworks")
        headers = {'Content-Type': 'application/json'}
        action = "GET"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result " + result.text)
        return result

    def getNetwork(self, networkId): 
        logger.info("getNetwork("+ str(networkId) + ")")
        requestData, url = self.getRequestData("getNetworks")
        headers = {'Content-Type': 'application/json'}
        action="GET"
        url = url + "/" + str(networkId)
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result " + result.text)
        return result
    
    def createNetwork(self):
        logger.info("createNetwork()")
        requestData, url = self.getRequestData("createNetwork")
        headers = {'Content-Type': 'application/json'}
        action="POST"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result " + result.text)
        return result

    def deleteNetwork(self, networkId):
        logger.info("deleteNetwork(" + str(networkId) + ")")
        requestData, url = self.getRequestData("deleteNetwork")
        headers = {'Content-Type': 'application/json'}
        action="DELETE"
        url = url + "/" + str(networkId)
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result ("+ str(networkId) + "): " + result.text)
        return result

    def updateNetwork(self, networkId):
        logger.info("updateNetwork()")
        requestData, url = self.getRequestData("updateNetwork")
        headers = {'Content-Type': 'application/json'}
        action="PUT"
        url = url + "/" + str(networkId)
        requestData["id"] = str(networkId)
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result  \n" + result.text)
        return result

    def getIpAddressPools(self, networkId):
        logger.info("getIpAddressPools("+ str(networkId) + ")")
        requestData, url = self.getRequestData("getIpAddressPools")
        headers = {'Content-Type': 'application/json'}
        action="GET"
        url = url.replace("{0}", str(networkId))
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result " + result.text)
        return result

    def getRequestData(self, task):
        logger.info("getRequestData()")

        with open("../requestdata/virtualNetworkRequestPayload.json") as data_file:
            data = json.load(data_file)
            requestData = data["services"][task]["data"]
            url = self.__class__.host + data["services"][task]["url"]
            return requestData, url

if __name__ == "__main__":  
    test = VirtualNetworkHandler()
    test.getNetworks()


    
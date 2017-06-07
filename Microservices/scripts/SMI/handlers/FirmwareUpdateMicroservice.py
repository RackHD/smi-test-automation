'''
Created on June 5, 2017
@author: Michael Regert
'''
 
import json
import os
import sys

run_dir=os.path.abspath(os.path.dirname(__file__))
current_dir = os.getcwd()
os.chdir(run_dir)
sys.path.insert(0,os.path.abspath('../utility'))

from UtilBase import Utility

class FirmwareUpdateHandler(Utility):
    def __init__(self):
        global logger
        logger = self.getLoggerInstance()
    
    def getVersion(self):
        logger.info("FirmwareUpdateHandler: getVersion()")
        requestData, url = self.getRequestData("getVersion")
        headers = {'Content-Type': 'application/json'}
        action="GET"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Results from FirmwareUpdateHandler: getVersion(): \n" + result.text)
        return result

    def getCatalog(self, parameter_list):
        logger.info("FirmwareUpdateHandler: getCatalog()")
        requestData, url = self.getRequestData("getCatalog")
        headers = {'Content-Type': 'application/json'}
        action="GET"
        for index, param in enumerate(parameter_list):
            sub = "{" + str(index) + "}"
            url = url.replace(sub, param)
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Results from FirmwareUpdateHandler getCatalog(): \n" + result.text)
        return result
        
    def getApplicableUpdates(self):
        logger.info("FirmwareUpdateHandler: getApplicableUpdates()")
        requestData, url = self.getRequestData("getApplicableUpdates")
        headers = {'Content-Type': 'application/json'}
        action="POST"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Results from FirmwareUpdateHandler: getApplicableUpdates(): \n" + result.text)
        return result

    def getRequestData(self, task):
        logger.info("FirmwareUpdateHandler: getRequestData()")
        with open("../requestdata/firmwareUpdateRequestPayload.json") as data_file:
            data = json.load(data_file)
            requestData = data["services"][task]["data"]
            url = self.__class__.host + data["services"][task]["url"]
            return requestData, url
        

if __name__ == "__main__":  
    test = FirmwareUpdateHandler()

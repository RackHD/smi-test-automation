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
    
    def getTestData(self, task):
        logger.info("FirmwareUpdateHandler: getRequestData()")
        with open(self.__class__.directory + "firmwareUpdateRequestPayload.json") as data_file:
            data = json.load(data_file)
            url = self.__class__.host + data["services"][task]["url"]
            parameters = data["services"][task]["parameters"]
            payload = data["services"][task]["payload"]
            return url, parameters, payload
    
    def addQueryParameters(self, url, parameters):
        url += "?"
        for index, key in enumerate(parameters):
            value = parameters[key]
            url += "{}={}".format(key, value)
            if (index < len(parameters)-1):
                url += "&"
        return url
    
    def makeGetRestCall(self, url):
        logger.info("Calling GET: {}".format(url))
        headers = {'Content-Type': 'application/json'}
        action="GET"
        result = self.getResponse(action, url, None , headers)
        logger.info("Results from GET: {}\n".format(result))
        return result        

    def makePostRestCall(self, url, payload):
        logger.info("Calling POST: {}".format(url))
        headers = {'Content-Type': 'application/json'}
        action="POST"
        result = self.getResponse(action, url, payload , headers)
        logger.info("Results from POST: {}\n".format(result))
        return result        
        

if __name__ == "__main__":  
    test = FirmwareUpdateHandler()

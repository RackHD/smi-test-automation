'''
Created on May 2, 2017

@author: mkowkab
'''
import json

from utility.UtilBase import Utility


#import os
#import sys
#from scripts.SMI.utility.UtilBase import Utility
#run_dir=os.path.abspath(os.path.dirname(__file__))
#current_dir = os.getcwd()
#os.chdir(run_dir)
#sys.path.insert(0,os.path.abspath('../utility'))
class SCPHandler(Utility):
    
    def __init__(self):
        global logger
        logger = self.getLoggerInstance()
        
    def exportSCP(self):
        logger.info("SCPHandler: export")
        task = "export"
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = self.getResponse(action, url, requestData, headers)
        logger.info("Result from the SCP Microservice for Export Task: \n" + result.text)        
        return result
    
    def importSCP(self):
        logger.info("SCPHandler: Import")
        task = "import"
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action ="POST"
        result = self.getResponse(action, url, requestData, headers)
        return result
    
    def getComponents(self):
        logger.info("SCPHandler: getComponents")
        task = "getComponents"
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action ="POST"
        result = self.getResponse(action, url, requestData, headers)
        return result
    

    def getRequestData(self, task):
        logger.info("SCPHandler: getRequestData")
        
        with open("../requestdata/scpRequestPayload.json") as data_file:
            data = json.load(data_file)
            requestData = data["dell"]["services"][task]["payload"]
            url = data["dell"]["services"][task]["microserviceURL"]
            return requestData, url
    
        
if __name__ == "__main__":
    test = SCPHandler()
    test.exportSCP()
            
        

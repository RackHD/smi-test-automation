# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: mkowkab
'''
import json
from . import handler_tools as tools

import logging

logger = logging.getLogger(__name__)
#import os
#import sys
#from scripts.SMI.utility.UtilBase import Utility
#run_dir=os.path.abspath(os.path.dirname(__file__))
#current_dir = os.getcwd()
#os.chdir(run_dir)
#sys.path.insert(0,os.path.abspath('../utility'))
class SCPHandler(Utility):

    def __init__(self):
        pass
        
    def exportSCP(self):
        logger.info("export")
        task = "export"
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = get_response(action, url, requestData, headers)
        logger.info("Result " + result.text)
        return result

    def importSCP(self):
        logger.info("Import")
        task = "import"
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = get_response(action, url, requestData, headers)
        return result

    def getComponents(self):
        logger.info("getComponents")
        task = "getComponents"
        requestData, url = self.getRequestData(task)
        headers = {'Content-Type': 'application/json'}
        action = "POST"
        result = get_response(action, url, requestData, headers)
        return result

    def getRequestData(self, task):
        logger.info("getRequestData")

        with open("../requestdata/scpRequestPayload.json") as data_file:
            data = json.load(data_file)
            requestData = data["dell"]["services"][task]["payload"]
            url = data["dell"]["services"][task]["microserviceURL"]
            return requestData, url


if __name__ == "__main__":
    test = SCPHandler()
    test.exportSCP()
    
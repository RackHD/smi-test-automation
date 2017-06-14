# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: mkowkab
'''
import logging.config
import requests

class Utility(object):
    
    def __init__(self):
        print ("Initializing.. ")
        
    def getLoggerInstance(self):
        logging.config.fileConfig("../logs/logging_config.ini")
        logger = logging.getLogger('DellSMI')
        return logger
    
    def getResponse(self, action, url, jsonData, headers):
        logger = self.getLoggerInstance()
        logger.info("UtilBase: getResponse")
        
        headers = {'Content-Type': 'application/json'}
        
        if action == "POST":
            logger.info("Utility: Action POST")
            response = requests.post(url, json=jsonData, headers=headers)
        elif action == "GET":
            logger.info("Utility: Action GET")
            response = requests.get(url, json=jsonData, headers=headers)
        elif action == "PUT":
            logger.info("Utility: Action PUT")
            response = requests.put(url, json=jsonData, headers=headers)
        elif action == "DELETE":
            logger.info("Utility: Action DELETE")
            response = requests.delete(url, json=jsonData, headers=headers)
            
        else: 
            raise Exception("Utility: Invalid Action " + action)
            
        return response    
        
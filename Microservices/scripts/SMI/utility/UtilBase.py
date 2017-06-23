# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: mkowkab
'''
import logging
import requests

logger = logging.getLogger(__name__)

class Utility(object):

    def __init__(self):
        pass

    def getLoggerInstance(self):
        pass

    def getResponse(self, action, url, jsonData, headers):
        logger = self.getLoggerInstance()
        logger.info("getResponse")

        headers = {'Content-Type': 'application/json'}

        if action == "POST":
            logger.info("POST")
            response = requests.post(url, json=jsonData, headers=headers)
        elif action == "GET":
            logger.info("GET")
            response = requests.get(url, json=jsonData, headers=headers)
        elif action == "PUT":
            logger.info("PUT")
            response = requests.put(url, json=jsonData, headers=headers)
        elif action == "DELETE":
            logger.info("DELETE")
            response = requests.delete(url, json=jsonData, headers=headers)

        else:
            raise Exception("Invalid Action : " + action)

        return response

        
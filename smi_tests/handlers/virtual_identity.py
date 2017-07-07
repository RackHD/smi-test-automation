# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 4, 2017

@author: Michael Regert, Michael Hepfer
'''

import json
import os
import sys
import logging
from . import handler_tools as tools

logger = logging.getLogger(__name__)

class VirtualIdentityHandler(Utility):

    def __init__(self):
        host = ""

    def getVirtualIdentities(self): 
        logger.info("getVirtualIdentities()")
        requestData, url = self.getRequestData("getVirtualIdentities")
        headers = {'Content-Type': 'application/json'}
        action="GET"
        result = get_response(action, url, requestData, headers)
        logger.info("Result " + result.text)
        return result

    def getRequestData(self, task):
        logger.info("getRequestData()")

        with open("../requestdata/virtualIdentityRequestPayload.json") as data_file:
            data = json.load(data_file)
            requestData = data["services"][task]["data"]
            url = self.__class__.host + data["services"][task]["url"]
            return requestData, url

if __name__ == "__main__":  
    test = VirtualIdentityHandler()

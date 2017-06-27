# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 5, 2017
@author: Michael Regert
'''

import json
import os
import sys
import logging
from . import handler_tools as tools

logger = logging.getLogger(__name__)

def getTestData(self, task):
    logger.info("getRequestData()")
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
    result = get_response(action, url, None , headers)
    logger.info("Results from GET: {}\n".format(result))
    return result

def makePostRestCall(self, url, payload):
    logger.info("Calling POST: {}".format(url))
    headers = {'Content-Type': 'application/json'}
    action="POST"
    result = get_response(action, url, payload , headers)
    logger.info("Results from POST: {}\n".format(result))
    return result


if __name__ == "__main__":  
    test = FirmwareUpdateHandler()

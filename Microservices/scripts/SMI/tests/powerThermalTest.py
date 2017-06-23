# -*- coding: utf-8 -*-
'''
Copyright © 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on May 2, 2017

@author: Rahman Muhammad
'''
import json
import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handlers.PowerThermalMicroservice import PowerThermalHandler
from utility.UtilBase import Utility



class PowerThermalMicroserviceTest(unittest.TestCase):    
    global logger
    logger = Utility().getLoggerInstance()
    
    def test_getVersion(self):        
                
        try:
           logger.info("Running")
           response = PowerThermalHandler().getAPIVersion()
           logger.info("Response: " + response.text)
                      
             
        except Exception as e:
            logger.error("Exception: " + str(e))
            raise e
        
    def test_getPowerThermal(self):
           
        
        try:
            logger.info("Running")
            response = PowerThermalHandler().getPowerThermal()
            logger.info("Response: " + response.text)
           
             
        except Exception as e:
            logger.error("Exception: " + str(e))
            raise e
        
           
        
if __name__=="__main__":
    if len(sys.argv) > 1:
        host = sys.argv.pop()
    else:
        host = "http://localhost:46019"
    from run_tests import run_tests
    run_tests('PWTH')

    
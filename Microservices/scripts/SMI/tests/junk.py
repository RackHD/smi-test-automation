'''
Created on June 5, 2017
@author: Michael Regert
'''

import json
import unittest
import sys
import os
import getopt
run_dir=os.path.abspath(os.path.dirname(__file__))
current_dir = os.getcwd()
os.chdir(run_dir)
sys.path.insert(0,os.path.abspath('../utility'))
sys.path.append(os.path.abspath('../handlers'))

from UtilBase import Utility
from FirmwareUpdateMicroservice import FirmwareUpdateHandler

class Junk(unittest.TestCase):
    global logger
    logger = Utility().getLoggerInstance()

if __name__=="__main__":
    print( "" )
# -*- coding: utf-8 -*-

#   __      ___  ___ _  __ ___          ___ _           ___ ___  _
#  (_  |\/|  |    | |_ (_   |    /\  | | | / \ |\/|  /\  |   |  / \ |\ |
#  __) |  | _|_   | |_ __)  |   /--\ |_| | \_/ |  | /--\ |  _|_ \_/ | \|

'''
SMI TEST AUTOMATION
~~~~~~~~~~~~~~~~~~~

Run specified microservice tests on specified host.
Tests run in no particular order.

-- Structure --
The default host is 'localhost'
Each microservice is assigned a 1 character ID
Each microservice ID is associated with an alias

-- Reference (ID:ALIAS) --
1:DISC 2:CHIN 3:SVIN 4:PWTH 5:SCP 6:VID 7:VNW 8:FWUP

-- Input --
Enter an IP address to assign it as host [100.68.125.170]
Use the prefix 'host:' to set a named host [host:node-example]
Enter a directory path to assign it as data directory [./test_data]
Use the prefix 'data:' to set a data directory [data:test_data]
If no tests are specified, all will run by default
Microservice IDs can be separated with or without a space [123 or 1 2 3]
Microservice Aliases are case insensitive [DISC or disc]
Use the modifier '^' or '!' to skip a test
Host, Aliases, and IDs can be passed as parameters in any order
[host:node-example CHIN svin 1 56 !2]

Argument format examples:
==================================================================================

>>> auto_test - Run all tests
>>> auto_test 4 - Run test with ID 4
>>> auto_test 7451725 - Run tests with ID 7, 4, 1, 2, and 5
>>> auto_test SVIN - Run test with ID 4
>>> auto_test DISC SCP CHIN - Run tests with ID 1, 6, and 3
>>> auto_test 24 vNw 314 ScP - Run tests with ID 2, 4, 7, 3, 1, and 6
>>> auto_test ^345 - Run all tests except those with ID 3, 4, and 5
>>> auto_test 100.68.125.170 ./test_data 5! - Run all tests from test_data on specified host except test 5
>>> auto_test host:node-example 345 - Run tests with ID 3, 4, 5 on specified host
>>> auto_test host:node-example 345 data:test_data - Run tests with ID 3, 4, 5 from test_data on specified host

==================================================================================
:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.

Created on June 20, 2017

'''
__title__ = 'SMI Test Automation'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

import sys
import unittest
import logging
import config
from resttestms import log, parse

import test_discovery as disc
import test_chassisinventory as chin
import test_serverinventory as svin
import test_powerthermal as pwth
import test_scp as scp
import test_virtualidentity as vid
import test_virtualnetwork as vnw
import test_firmwareupdate as fwup

log.configure_logger_from_yaml('logs/logger_config.yml')
LOG = logging.getLogger(__name__)

# ------------ ARGUMENT CONFIGURATION PROFILE ------------
##########################################################

# Microservice ID
M_ID = {

    '1' : disc,
    '2' : chin,
    '3' : svin,
    '4' : pwth,
    '5' : scp,
    '6' : vid,
    '7' : vnw,
    '8' : fwup

}

# Microservice ID Reversed
M_ID_R = {m_id: mservice for mservice, m_id in M_ID.items()}

# Microservice Alias
ALIAS = {

    'DISC' : M_ID_R[disc],
    'CHIN' : M_ID_R[chin],
    'SVIN' : M_ID_R[svin],
    'PWTH' : M_ID_R[pwth],
    'SCP' : M_ID_R[scp],
    'VID' : M_ID_R[vid],
    'VNW' : M_ID_R[vnw],
    'FWUP' : M_ID_R[fwup]

}

##########################################################

def _load_tests(test_keys):
    """Load tests into suite for each of the test keys passed in"""
    test_suite = []
    for key in test_keys:
        test_suite.append(unittest.TestLoader().loadTestsFromModule(M_ID[key]))
    return unittest.TestSuite(test_suite)

def run_tests(keys):
    """Run specified tests using key set"""
    LOG.info("Host: %s", config.HOST)
    LOG.info("Data Directory: %s", config.DATA)
    LOG.info("Depth: %s", config.DEPTH)
    LOG.info("Test Keys: %s", keys)
    test_suite = _load_tests(keys)
    LOG.debug("Loaded Tests: %s", test_suite)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

def parse_keys_tester():
    """Unit test cases to make sure correct keys are parsed from given arguments"""
    test_cases = [[], [123], ['SCP'], ['chin', 2, 'DIsc'], [13, 'vnw', 455],
                  ['^5'], ['host:node-wright'], ['!chin'], ['192.168.0.1'],
                  ['localhost', 32, 'SCP', '^3', '!2', '100.0.0.255'],
                  ['host:node-example', '5!'], ['^1237'], ['./test_data'],
                  ['localhost', 32, 'SCP', '^3', '!2', './sample_data'],
                  ['data:node-example', '5!', 'host:testing']]
    print("\nBegin Testing\n\nID : ALIAS\n")
    for alias in ALIAS:
        print("{} : {}".format(ALIAS[alias], alias))
    print("\n")
    for index, case in enumerate(test_cases):
        LOG.info("Running test %s", (index + 1))
        print("\n--Test {}--\n Args:{}".format(index + 1, case))
        try:
            host, data, depth, keys = parse.auto_test_args(M_ID, ALIAS, *case)
            print("Host: {}".format(host))
            print("Data Directory: {}".format(data))
            print("Depth: {}".format(data))
            print("Parsed Keys: {}".format(keys))
        except Exception:
            print("TEST FAILED")
            LOG.exception("Test failed with args {}".format(case))

if __name__ == '__main__':
    PARSED_HOST, PARSED_DATA, PARSED_DEPTH, KEYS = parse.auto_test_args(M_ID, ALIAS, *sys.argv[1:])
    config.HOST = PARSED_HOST if PARSED_HOST else config.HOST
    config.DATA = PARSED_DATA if PARSED_DATA else config.DATA
    config.DEPTH = PARSED_DEPTH if PARSED_DEPTH else config.DEPTH
    run_tests(KEYS)

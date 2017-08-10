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
Defaults are configured in "config.py"
The default host is 'localhost'
The default data directory is 'test_data'
The default depth is 1

Each microservice is assigned a 1 character ID
Each microservice ID is associated with an alias

-- Reference (ID : ALIAS : MICROSERVICE) --
1 : DISC : Device Discovery
2 : CHIN : Chassis Inventory
3 : SVIN : Server Inventory
4 : PWTH : Power Thermal
5 : SCP : Server Configuration Profile
6 : VRID : Virtual Identity
7 : VRNW : Virtual Network
8 : FWUP : Firmware Update
9 : OSDP : OS Deployment

-- Input --
HOST
The address of the host running the microservices
Enter an IP address to assign it as host [100.68.125.170]
Use the prefix 'host:' to set a named host [host:node-example]

DATA DIRECTORY
The folder containing JSON defined test cases
Enter a directory path to assign it as data directory [./test_data]
Use the prefix 'data:' to set a data directory [data:test_data]

DEPTH
The extent to which error handling will be tested
Higher depth takes longer to run
    Depth 1 - Send Empty Data
    Depth 2 - Iterate through data with bad values
    Depth 3 - Generate all combinations of data with bad values
Use the prefix 'depth:' to set depth 1-3 [depth:2]

If no tests are specified, all will run by default
Microservice IDs can be separated with or without a space [123 or 1 2 3]
Microservice Aliases are case insensitive [DISC or disc]
Use the modifier '^' or '!' to skip a microservice
Host, Aliases, and IDs can be passed as parameters in any order
[host:node-example CHIN svin 1 56 !2]

Argument format examples:
==================================================================================

>>> auto_test - Run all tests
>>> auto_test 4 - Run test with ID 4
>>> auto_test 7451725 - Run tests with ID 7, 4, 1, 2, and 5
>>> auto_test SVIN - Run test with ID 4
>>> auto_test DISC SCP CHIN depth:3 - Run tests with ID 1, 6, and 3 with depth:3
>>> auto_test 24 vrnw 314 Scp - Run tests with ID 2, 4, 7, 3, 1, and 6
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
import test_virtualidentity as vrid
import test_virtualnetwork as vrnw
import test_firmwareupdate as fwup
import test_osdeployment as osdp

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
    '6' : vrid,
    '7' : vrnw,
    '8' : fwup,
    '9' : osdp

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
    'VRID' : M_ID_R[vrid],
    'VRNW' : M_ID_R[vrnw],
    'FWUP' : M_ID_R[fwup],
    'OSDP' : M_ID_R[osdp]

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

if __name__ == '__main__':
    PARSED_HOST, PARSED_DATA, PARSED_DEPTH, KEYS = parse.auto_test_args(M_ID, ALIAS, *sys.argv[1:])
    config.HOST = PARSED_HOST if PARSED_HOST else config.HOST
    config.DATA = PARSED_DATA if PARSED_DATA else config.DATA
    config.DEPTH = PARSED_DEPTH if PARSED_DEPTH else config.DEPTH
    run_tests(KEYS)

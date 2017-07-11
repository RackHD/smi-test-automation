# -*- coding: utf-8 -*-
"""
Default configuration data for SMI-TEST-AUTOMATION
"""

#-------------- DEFAULT TEST CONFIGURATION ---------------
##########################################################

HOST = '100.68.125.170'

DATA = 'test_data'

##########################################################

from resttestms import parse
import re

print(parse.get_list_mod("INSERT : ALL"))
"""
Path context for handlers

"""

import sys
from os.path import abspath, dirname
import logging
sys.path.append(dirname(dirname(abspath(__file__))))
from toolkit import httptools

LOG = logging.getLogger(__name__)
LOG.debug(dirname(dirname(abspath(__file__))))

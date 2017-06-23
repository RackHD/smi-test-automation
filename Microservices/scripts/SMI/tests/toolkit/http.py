# -*- coding: utf-8 -*-

#   __      ___  ___ _  __ ___          ___ _           ___ ___  _
#  (_  |\/|  | __ | |_ (_   | __ /\  | | | / \ |\/|  /\  |   |  / \ |\ |
#  __) |  | _|_   | |_ __)  |   /--\ |_| | \_/ |  | /--\ |  _|_ \_/ | \|

"""
HTTP Toolkit
~~~~~~~~~~~~
Series of tools designed to manipulate HTTP requests

Copyright (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 23, 2017
"""
__title__ = 'toolkit.http'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

def get_host_url(default_host, override, port):
    """Grab the host and port, generate a url"""
    host = override if override else default_host
    return "http://{}:{}".format(host, port)

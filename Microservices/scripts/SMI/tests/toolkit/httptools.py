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
__title__ = 'httptools'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

def select_host(default_host, override):
    """Compare default host and override to determine host"""
    host = override if override else default_host
    return host

def create_host_url(host, port):
    """Use the host and port, generate a url"""
    formatted_host = "http://{}:{}".format(host, port)
    return formatted_host

'''
Created on May 2, 2017

@author: mkowkab
'''
import logging.config
import requests
import getopt
import sys

class Utility(object):
    
        # host ip and directory defaults
    ip = "http://localhost"
    directory  = "../requestdata"

    def __init__(self):
        print ("Initializing.. ")
        
        self.getCommandArguments()

        print( "USING: host = {}".format(Utility.ip))
        print( "USING: directory = {}".format(Utility.directory))
    
    def getCommandArguments(self):
        try:
            options, remainder = getopt.getopt(sys.argv[1:], "hi:d:", ["help","ip=","directory="])
    
        except getopt.GetoptError:
            print ("\nUsage: python {} [arguments]".format(__file__))
            print ("\nArguments:\n")
            print ("\t-h or --help\tHelp")
            print ("\t-i or --ip\tIP and port (e.g. 192.168.0.1)")
            print ("\t-d or --dir\tDirectory of test JSON files")
            sys.exit(2)
    
        for opt, arg in options:
            if opt in ("-h", "--help"):
                print ("Usage: python {} [arguments]".format(__file__))
                print ("\nArguments:\n")
                print ("\t-h or --help\tHelp")
                print ("\t-i or --ip\tIP and port (e.g. 192.168.0.1)")
                print ("\t-d or --dir\tDirectory of test JSON files")
                sys.exit()
            elif opt in ("-i", "--ip"):
                Utility.ip = "http://{}".format(arg)
            elif opt in ("-d", "--dir"):
                Utility.directory = arg

    def getLoggerInstance(self):
        logging.config.fileConfig("../logs/logging_config.ini")
        logger = logging.getLogger('DellSMI')
        return logger
    
    def getResponse(self, action, url, jsonData, headers):
        logger = self.getLoggerInstance()
        logger.info("UtilBase: getResponse")
        
        headers = {'Content-Type': 'application/json'}
        
        if action == "POST":
            logger.info("Utility: Action POST")
            response = requests.post(url, json=jsonData, headers=headers)
        elif action == "GET":
            logger.info("Utility: Action GET")
            response = requests.get(url, json=jsonData, headers=headers)
        elif action == "PUT":
            logger.info("Utility: Action PUT")
            response = requests.put(url, json=jsonData, headers=headers)
        elif action == "DELETE":
            logger.info("Utility: Action DELETE")
            response = requests.delete(url, json=jsonData, headers=headers)
            
        else: 
            raise Exception("Utility: Invalid Action " + action)
            
        return response    
        
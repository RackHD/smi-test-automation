'''
Created on May 2, 2017

@author: Michael Regert, Michael Hepfer
'''
import json
import unittest
import sys
import os
import sys
run_dir=os.path.abspath(os.path.dirname(__file__))
current_dir = os.getcwd()
os.chdir(run_dir)
sys.path.insert(0,os.path.abspath('../utility'))
sys.path.append(os.path.abspath('../handlers'))

from UtilBase import Utility
from VirtualNetworkMicroservice import VirtualNetworkHandler

class VirtualNetworkTest(unittest.TestCase):
    
    global logger
    logger = Utility().getLoggerInstance()
    global networkId
    networkId = 0
    networkJson = ""

    ########################################################################
    # Test Get Networks returns an empty list
    def test001_GetNetworksEmpty(self):
        try:
            response = VirtualNetworkHandler().getNetworks()
            logger.info("VirtualNetworkTest: testCreateNetwork(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

            logger.info("VirtualNetworkTest: testGetNetworksEmpty(): Response Text: " + response.text)
            responseJson = json.loads(response.text)
            #assert here
            self.assertEqual(responseJson["pagination"]["total"], 0, "Pagination total count should be 0")
            self.assertEqual(responseJson["pages"]["total"], 0, "Pages total count should be 0")

        except Exception as e1:
            logger.error("VirtualNetworkTest: testGetNetworksEmpty():  Exception: " + str(e1))
            raise e1

    ########################################################################
    # Test Create Network works
    def test002_CreateNetwork(self):
        try:
            response = VirtualNetworkHandler().createNetwork()
            logger.info("VirtualNetworkTest: test002_CreateNetwork(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 201, "Response code should equal 201")

            logger.info("VirtualNetworkTest: test002_CreateNetwork(): Response Text: " + response.text)
            responseJson = json.loads(response.text)
            self.assertGreater(responseJson["id"], 0, "Network id should be greater than 0")

            # set the network id as instance variable for subsequent tests 
            self.__class__.networkId = responseJson["id"]

        except Exception as e1:
            logger.error("VirtualNetworkTest: test002_CreateNetwork():  Exception: " + str(e1))
            raise e1

    ########################################################################
    # Test Get Networks returns a network
    def test003_GetNetwork(self):
        try:
            response = VirtualNetworkHandler().getNetwork(self.__class__.networkId)
            logger.info("VirtualNetworkTest: test003_GetNetwork(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

            logger.info("VirtualNetworkTest: test003_GetNetwork(): Response Text: " + response.text)
            responseJson = json.loads(response.text)
            self.assertGreater(responseJson["id"], 0, "Network id should be greater than 0")

            # set the network JSON as instance variable for subsequent tests 
            self.__class__.networkJson = responseJson

        except Exception as e1:
            logger.error("VirtualNetworkTest: test003_GetNetwork():  Exception: " + str(e1))
            raise e1

    ########################################################################
    # Test Push Networks updates a network
    def test004_UpdateNetwork(self):
        try:
            response = VirtualNetworkHandler().updateNetwork(self.__class__.networkId)
            logger.info("VirtualNetworkTest: test004_UpdateNetwork(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 204, "Response code should equal 204")

        except Exception as e1:
            logger.error("VirtualNetworkTest: test004_UpdateNetwork():  Exception: " + str(e1))
            raise e1

    #######################################################################
    # Test Delete Network deletes a network
    def test005_DeleteNetwork(self):
        try:
            response = VirtualNetworkHandler().deleteNetwork(self.__class__.networkId)
            logger.info("VirtualNetworkTest: test005_DeleteNetwork(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 204, "Response code should equal 204")
    
        except Exception as e1:
            logger.error("VirtualNetworkTest: test005_DeleteNetwork():  Exception: " + str(e1))
            raise e1
            
    ########################################################################
    # Test Create duplicate network fails
    def test006_CreateDuplicateNetworks(self):
        try:
            response = VirtualNetworkHandler().createNetwork()
            logger.info("VirtualNetworkTest: test006_CreateDuplicateNetworks(0): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 201, "Response code should equal 201")

            # set the network id as instance variable for subsequent tests 
            responseJson = json.loads(response.text)
            self.__class__.networkId = responseJson["id"]

            response = VirtualNetworkHandler().createNetwork()
            logger.info("VirtualNetworkTest: test006_CreateDuplicateNetworks(1): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 400, "Response code should equal 400")

        except Exception as e1:
            logger.error("VirtualNetworkTest: test006_CreateDuplicateNetworks():  Exception: " + str(e1))
            raise e1

    ########################################################################
    # Test Get IpAddressPools
    def test007_GetIpAddressPools(self):
        try:
            response = VirtualNetworkHandler().getIpAddressPools(self.__class__.networkId)
            logger.info("VirtualNetworkTest: test007_GetIpAddressPools(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 200, "Response code should equal 200")

        except Exception as e1:
            logger.error("VirtualNetworkTest: test006_CreateDuplicateNetworks():  Exception: " + str(e1))
            raise e1

    ########################################################################
    # Test Delete Network deletes a network
    def test008_DeleteNetwork(self):
        try:
            response = VirtualNetworkHandler().deleteNetwork(self.__class__.networkId)
            logger.info("VirtualNetworkTest: test008_DeleteNetwork(): Response Status Code: " + str(response.status_code))
            self.assertEqual(response.status_code, 204, "Response code should equal 204")
    
        except Exception as e1:
            logger.error("VirtualNetworkTest: test008_DeleteNetwork():  Exception: " + str(e1))
            raise e1

if __name__=="__main__":
    if len(sys.argv) > 1:
        VirtualNetworkHandler.host = sys.argv.pop()
    else:
        VirtualNetworkHandler.host = "http://localhost:46016"

    unittest.main()

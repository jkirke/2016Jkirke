#!/usr/bin/python3

import sys
import logging
import subprocess 
import http.client
import time

#'''
#zBC - Basic Function
#'''

url = '507271b6-fc10-4f58-98f7-03252c319ad1_vp0-api.zone.blockchain.ibm.com:443'

'''
logging.basicConfig(format= '%(asctime)-12s [%(filename)-10s] %(levelname)s %(message)s', level=logging.DEBUG)
'''

subprocess.call(["mkdir", "logs"])
logger = logging.getLogger(__name__)
logfile = 'logs/'+ ((__file__.upper())[(__file__.rfind('/')+1):]).replace('.PY', '.log')
logging.basicConfig(format= '%(asctime)-12s [%(filename)-10s] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename=logfile, filemode='w', level=logging.DEBUG) 

#'''
#List peers, check output to confirm all peers are available
#'''					
					
logger.info(">>>STEP 1: Executing list peers.\n")					
print ("Executing list peers.")
					
conn = http.client.HTTPSConnection(url)

conn.request("GET", "/network/peers")	

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))		

#'''
#Register user with vp0
#'''	

logger.info(">>>STEP 2: Register user with vp0.\n")					
print ("Register user with vp0.")				

conn = http.client.HTTPSConnection(url)

payload = "{\r\n\"enrollId\":\"user_type1_fac0acf57b\",\r\n\"enrollSecret\":\"7d0763e03a\"\r\n}"

conn.request("POST", "/registrar", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

logger.info(">>>STEP 2: Confirm that user is successfully registered.\n")					
print ("Confirm that user is successfully registered.")	

conn = http.client.HTTPSConnection(url)

payload = "{\r\n\"enrollId\":\"test_user0\",\r\n\"enrollSecret\":\"MS9qrN8hFjlE\"\r\n}"

conn.request("GET", "/registrar/user_type1_fac0acf57b", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#'''
#Deploy chaincode example02
#'''	

logger.info(">>>STEP 3: Deploy chaincode example02.\n")					
print ("Deploy chaincode example02.")

conn = http.client.HTTPSConnection(url)

payload = "{\r\n  \"jsonrpc\": \"2.0\",\r\n  \"method\": \"deploy\",\r\n  \"params\": {\r\n    \"type\": 1,\r\n    \"chaincodeID\":{\r\n        \"path\":\"github.com/hyperledger/fabric/examples/chaincode/go/chaincode_example02\"\r\n    },\r\n    \"ctorMsg\": {\r\n        \"function\":\"init\",\r\n        \"args\":[\"a\", \"5000\", \"b\", \"5000\"]\r\n    },\r\n    \"secureContext\": \"user_type1_fac0acf57b\"\r\n  },\r\n  \"id\": 1\r\n}"

conn.request("POST", "/chaincode/", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))	

time.sleep(120)

#'''
#Invoke chaincode to transfer 500 from a to b
#'''

logger.info(">>>STEP 4: Invoking chaincode to transfer 500 from a to b.\n")		
print ("Invoking chaincode to transfer 500 from a to b.")
	
conn = http.client.HTTPSConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"invoke\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"70dfc8e6aab1d13428f8732f4013af116dd588b76ab813734aaca5d9e2903b668b902420477d382f8dc234b4c30f5587addea8a5bf2e25c470ec46d9b27cbabc\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"invoke\",\r\n            \"args\": [\r\n                \"a\",\r\n                \"b\",\r\n                \"500\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_fac0acf57b\"\r\n    },\r\n    \"id\": 3\r\n}"

conn.request("POST", "/chaincode/", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

time.sleep(20)

#'''
#Query chaincode to verify successful invoke
#'''

logger.info(">>>STEP 5: Query chaincode to verify values.\n")	
print ("Query chaincode to verify values.")	

conn = http.client.HTTPSConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"query\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"70dfc8e6aab1d13428f8732f4013af116dd588b76ab813734aaca5d9e2903b668b902420477d382f8dc234b4c30f5587addea8a5bf2e25c470ec46d9b27cbabc\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"query\",\r\n            \"args\": [\r\n                \"a\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_fac0acf57b\"\r\n    },\r\n    \"id\": 5\r\n}"

conn.request("POST", "/chaincode", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#'''
#Complete execution
#'''
	
logger.info(">>>Completed test execution.\n")
print ("Completed test execution")
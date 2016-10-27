#!/usr/bin/python3

import sys
import logging
import subprocess
import http.client
import time

#'''
#zBC - Basic Function
#'''

url = '9.2.98.113:20000'

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

conn = http.client.HTTPConnection(url)

conn.request("GET", "/network/peers")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#'''
#Register user with vp3
#'''

logger.info(">>>STEP 2: Register user with vp0.\n")
print ("Register user with vp0.")

conn = http.client.HTTPConnection(url)

payload = "{\r\n\"enrollId\":\"user_type1_063f1266b6\",\r\n\"enrollSecret\":\"1499234092\"\r\n}"

conn.request("POST", "/registrar", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

logger.info(">>>STEP 2: Confirm that user is successfully registered.\n")
print ("Confirm that user is successfully registered.")

conn = http.client.HTTPConnection(url)

payload = "{\r\n\"enrollId\":\"user_type1_063f1266b6\",\r\n\"enrollSecret\":\"1499234092\"\r\n}"

conn.request("GET", "/registrar/user_type1_063f1266b6", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#'''
#Deploy chaincode example02
#'''

logger.info(">>>STEP 3: Deploy chaincode example02.\n")
print ("Deploy chaincode example02.")

conn = http.client.HTTPConnection(url)

payload = "{\r\n  \"jsonrpc\": \"2.0\",\r\n  \"method\": \"deploy\",\r\n  \"params\": {\r\n    \"type\": 1,\r\n    \"chaincodeID\":{\r\n        \"path\":\"github.com/hyperledger/fabric/examples/chaincode/go/chaincode_example02\"\r\n    },\r\n    \"ctorMsg\": {\r\n        \"function\":\"init\",\r\n        \"args\":[\"a\", \"5000\", \"b\", \"5000\"]\r\n    },\r\n    \"secureContext\": \"user_type1_063f1266b6\"\r\n  },\r\n  \"id\": 1\r\n}"

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

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"invoke\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"invoke\",\r\n            \"args\": [\r\n                \"a\",\r\n                \"b\",\r\n                \"500\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 3\r\n}"

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

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"query\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"query\",\r\n            \"args\": [\r\n                \"a\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 5\r\n}"

conn.request("POST", "/chaincode", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#'''
#Complete execution
#'''

logger.info(">>>Completed test execution.\n")
print ("Completed test execution")

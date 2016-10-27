#!/usr/bin/python3

import sys
import subprocess
import http.client
import time

#'''
#zBC - Long run
#'''

url = '9.2.98.113:20000'

#'''
#Invoke chaincode to transfer 500 from a to b
#'''

print ("Invoking chaincode to transfer 500 from a to b.")

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"invoke\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"invoke\",\r\n            \"args\": [\r\n                \"a\",\r\n                \"b\",\r\n                \"500\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 3\r\n}"

conn.request("POST", "/chaincode/", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

time.sleep(2)

#'''
#Query chaincode to verify successful invoke
#'''

print ("Query chaincode to verify values.")

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"query\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"query\",\r\n            \"args\": [\r\n                \"a\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 5\r\n}"

conn.request("POST", "/chaincode", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"query\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"query\",\r\n            \"args\": [\r\n                \"b\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 5\r\n}"

conn.request("POST", "/chaincode", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#'''
#Invoke chaincode to transfer 500 from b to a
#'''

print ("Invoking chaincode to transfer 500 from b to a.")

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"invoke\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"invoke\",\r\n            \"args\": [\r\n                \"b\",\r\n                \"a\",\r\n                \"500\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 3\r\n}"

conn.request("POST", "/chaincode/", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

time.sleep(2)

#'''
#Query chaincode to verify successful invoke
#'''

print ("Query chaincode to verify values.")

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"query\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"query\",\r\n            \"args\": [\r\n                \"a\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 5\r\n}"

conn.request("POST", "/chaincode", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

conn = http.client.HTTPConnection(url)

payload = "{\r\n    \"jsonrpc\": \"2.0\",\r\n    \"method\": \"query\",\r\n    \"params\": {\r\n        \"type\": 1,\r\n        \"chaincodeID\": {\r\n            \"name\":\"e0d5efeafa6b6e244a99a3bd4efed36099f5593af76d99c324af3dcf2d26549494fb75c161489e9908d52f23b09c8f734d741bb2cb94ee876114665bdd94cf13\"\r\n        },\r\n        \"ctorMsg\": {\r\n            \"function\": \"query\",\r\n            \"args\": [\r\n                \"b\"\r\n            ]\r\n        },\r\n        \"secureContext\": \"user_type1_063f1266b6\"\r\n    },\r\n    \"id\": 5\r\n}"

conn.request("POST", "/chaincode", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


#'''
#Complete execution
#'''

print ("Completed test execution")
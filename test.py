from generate import GenerateConversation
import urllib.request
import json
import requests

API_END_POINT = "http://localhost:5000/api/inputText"

generateConversation = GenerateConversation("MHRA.csv")
conversation = generateConversation.generate()
print(conversation)
# TODO: process user message
userMessage = "hi"
body = {
        "message"   : userMessage,
        "sessionID" : "ryan"
        }
header = {"Content-Type": "application/json"}

# Method 1
r = requests.post(API_END_POINT, json=body, headers=header)
print(r.text)

# Method 2
# req = urllib.request.Request(API_END_POINT)
# req.add_header('Content-Type', 'application/json')
# jsondata = json.dumps(body)
# jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
# # req.add_header('Content-Length', len(jsondataasbytes))
# print (jsondataasbytes)
# response = urllib.request.urlopen(req, jsondataasbytes)
# print(response)

# TODO: Compare
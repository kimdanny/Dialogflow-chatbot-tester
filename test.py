from generate import GenerateConversation
import urllib.request
import json
import requests

API_END_POINT = "http://localhost:5000/api/inputText"

generateConversation = GenerateConversation()
conversation = generateConversation.generate()
# TODO: process user message
userMessage = ""
body = {
        "message"   : userMessage,
        "sessionID" : "ryan"
        }
header = {"Content-Type": "application/json"}

r = requests.post(API_END_POINT, json=body, headers=header)
print(r.text)

# req = urllib.request.Request(API_END_POINT)
# req.add_header('Content-Type', 'application/json; charset=utf-8')
# jsondata = json.dumps(body)
# jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
# req.add_header('Content-Length', len(jsondataasbytes))
# print (jsondataasbytes)
# response = urllib.request.urlopen(req, jsondataasbytes)
from generate import GenerateConversation
import requests

API_END_POINT = "http://localhost:5000/api/inputText"

generateConversation = GenerateConversation()
conversation = generateConversation.generate()
userMessage = {}

r = requests.post(API_END_POINT, json=userMessage)
print(r.text)
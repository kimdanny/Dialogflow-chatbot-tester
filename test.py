import requests
from generate import GenerateConversation
from CustomError import TestFailError, StatusCodeError, Error
from QandA import QandA
import shutil
import os


API_END_POINT = "http://localhost:5000/api/inputText"


def post_request(userMessage):
    body = {
        "message": userMessage,
        "sessionID": "Danny"
    }
    header = {"Content-Type": "application/json"}

    res = requests.post(API_END_POINT, json=body, headers=header)

    if res.status_code is not 200:
        raise StatusCodeError("HTTP Error")
    res = res.json()["message"]
    return res

# for video demo
# print(post_request("hi"))
# print(post_request("my name is danny"))


# Clear target directory if previously made
if os.path.exists(os.path.join(os.path.dirname(__file__), "target")):
    shutil.rmtree(os.path.join(os.path.dirname(__file__), "target"))

files = ["MHRA.csv", "NHSD.csv", "FINAL.csv"]  # "MHRA.csv", "NHSD.csv", "NICE.csv", "FINAL.csv"

# ==== Testing Starts Here======
for file in files:

    if file[:file.index('.')] == "FINAL":
        EOCs = QandA.Final_end_of_conversation
    if file[:file.index('.')] == "MHRA":
        EOCs = QandA.MHRA_end_of_conversation
    if file[:file.index('.')] == "NHSD":
        EOCs = QandA.NHSD_end_of_conversation
    if file[:file.index('.')] == "NICE":
        EOCs = QandA.NICE_end_of_conversation

    for index in range(5):
        try:
            gen = GenerateConversation(file)
            gen.history = []        # empty the history
            conversation = gen.generate(i=index, CSV=True, TEXT=True)
            print("\n=========", gen.organisation_name, f"convos{index} is generated and ready to be tested =========")

            for i in range(len(conversation)-1):

                if conversation[i+1][0] in EOCs:
                    print(f"{gen.organisation_name} convos{index} Test => Success")
                    break

                if not post_request(conversation[i][1]) == conversation[i + 1][0]:
                    print(f"conversation[{i}][0]: ", conversation[i][0], "||")
                    print(f"conversation[{i}][1]: ", conversation[i][1], "||")
                    print(post_request(conversation[i][1]), "||", conversation[i + 1][0])
                    raise TestFailError(f"{gen.organisation_name} convos{index} Test => FAIL")

        except TestFailError:
            pass

        except Error as err:
            print(f"Error {type(err)} Occurred in {gen.organisation_name} -> convos{index}.csv")

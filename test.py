import requests
from generate import GenerateConversation
from CustomError import TestFailError, StatusCodeError, Error
from QandA import QandA


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

files = ["Final.csv"]  # "MHRA.csv", "NHSD.csv", "NICE.csv", "Final.csv"

# generate 10 test cases
for file in files:

    if file[:file.index('.')] == "Final":
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
                conversation = gen.generate(i=index)
                print("\n=========", gen.organisation_name, f"convos{index} is generated and ready to be tested =========")

                # TODO: compare with real here
                for i in range(len(conversation)-1):
                    # if conversation[i][1] == '':
                    #     print(f"{gen.organisation_name} convos{index} Test => Success")
                    # if post_request(conversation[i][1]) == conversation[i + 1][0]:
                    #     pass
                    # else:
                    #     print(post_request(conversation[i][1]), "||", conversation[i + 1][0])
                    #     raise TestFailError(f"{gen.organisation_name} convos{index} Test => FAIL")
                    # print(conversation)
                    # print("=====")
                    # print(conversation[i][1], "||", conversation[i+1][0])
                    if conversation[i+1][0] in EOCs:
                        print(f"{gen.organisation_name} convos{index} Test => Success")

                    if not post_request(conversation[i][1]) == conversation[i + 1][0]:
                        print(post_request(conversation[i][1]), "||", conversation[i + 1][0])
                        raise TestFailError(f"{gen.organisation_name} convos{index} Test => FAIL")

            except TestFailError:
                pass

            except Error as err:
                print(f"Error {type(err)} Occurred in {gen.organisation_name} -> convos{index}.csv")

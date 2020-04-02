from generate import GenerateConversation
import requests


# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    def __init__(self):
        super().__init__()


class TestFailError(Error):
    """Raised when test is failed"""
    def __init__(self, msg):
        print(msg)

class StatusCodeError(Error):
    """Raised when HTTTP Status code is not 200"""
    def __init__(self, msg):
        print(msg)


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


files = ["MHRA.csv"]  # "MHRA.csv", "NHSD.csv", "NICE.csv"

# generate 10 test cases
for file in files:
        for index in range(10):
            try:
                gen = GenerateConversation(file)
                gen.history = []
                conversation = gen.generate(i=index)
                print("\n=========", gen.organisation_name, f"convos{index} is generated and ready to be tested =========")

                # TODO: compare with real here
                for i in range(len(conversation)):
                    if len(conversation[i][1]) == 0:
                        print(f"{gen.organisation_name} convos{index} Test => Success")
                    if post_request(conversation[i][1]) == conversation[i + 1][0]:
                        pass
                    else:
                        raise TestFailError(f"{gen.organisation_name} convos{index} Test => FAIL")

            except TestFailError:
                pass

            except Exception as ex:
                print(f"Error {type(ex)} Occurred in {gen.organisation_name} -> convos{index}.csv")

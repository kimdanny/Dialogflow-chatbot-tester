import csv
import random
import numpy as np
import pandas as pd
import os


# question and answer examples
class QandA:
    helloMessage_from_user = [
        "hi",
        "hello",
        "hey",
        "I want to start the chat",
        "let's start",
        "hey man"
    ]

    initial_QandA = {
        "What’s your name?": [
            "I'm Danny",
            "Ryan Zhao",
            "I am Xinyao Chuah",
            "my name is Joseph Connor",
            "Riyan Kim",
            "Haaroon Yousaf",
            "Dean Mohamedally",
            "Yun Fu",
            "i am toeun"
        ],

        "What is the name of the contact person in your organization?": [
            "He is Anthony Connor",
            "John Doe",
            "Joseph"
        ],

        # TODO: Can you generate strings based on regex?
        "What is their email address?": [
            "adfaff@email.com",
            "sampleemail@gmail.com",
            "123email456@gmail.com",
            "email456thisone@hotmail.com",
            "1iam2sohot3baby@hotbaby.co.uk",
            "thisisfake@fakeuni.ac.fakecountrycode",
        ],

        "What is their phone number?": [
            "01012345678",
            "074847572823",
            "It is +447394817293",
            "+447394817293",
            "+3569877675525",
            "It's 07394817293",
        ],

        "What is your organisation's name": [
            "carefulai",
            "it is Google",
            "it's called Facebook",
            "RCGP",
            "the name of the organisation is named carefulAI"
        ],

        "What is your organisation's address?": [
            "24 bedford way",
            "it is 48 marchmount street, London",
            "Lebus St. Tottenham Hale, London N17 9FD",
            "It's Lebus St. Tottenham Hale, London N17 9FD"
        ]
    }

    Yeses = [
        "yes that is correct",
        "that is correct",
        "they do",
        "does",
        "it does",
        "yup",
        "y",
        "right",
        "yes it does",
        "yes"
    ]

    Nos = [
        "no that is not correct",
        "that is not correct",
        "that is incorrect",
        "they don't",
        "does not",
        "it doesn't",
        "nop",
        "n",
        "wrong",
        "no it does not",
        "no"
    ]

    Clarification = [
        "what?",
        "can you say that in a different way",
        "could you specify?",
        "clarify",
        "clarify that please",
        "again?",
        "say that again?",
        "phrase it differently",
        "phrase it again?",
        "what does that mean",
        "what's that?",
        "what's dat",
        "what is it"
    ]

    MHRA_end_of_conversation = [
        "Great! You’re all set!",
        "Your MD belongs to Class I.",
        "Your MD belongs to Class IIa.",
        "Your MD belongs to Class IIb.",
        "Your MD belongs to Class III."
    ]

    NICE_end_of_conversation = [
        """
        This is the end of the Functional Classification. If you have told multiple Tiers, then you have to choose 
        the highest Tier. Plus, the Tiers are cumulative. This means that your DHT must meet all the standards 
        in the previous Tier(s), as well as its own Tier. (Please say Clarification if you need more explanation)
        """,
        """
        I am sorry. NICE's framework has been designed for DHTs that are commissioned in the UK health and care system, 
        it is less relevant to DHTs that are downloaded or purchased directly by users (such as through app stores). 
        Separate standards (including principle 7 of the code of conduct for data-driven health and care technology) 
        will apply to your DHT. Do you want me to move on to the NHSD checking? Plus, NICE's framework may be used with 
        DHTs that incorporate artificial intelligence using fixed algorithms. However, it is not designed for use with 
        DHTs that incorporate artificial intelligence using adaptive algorithms. For the same reason, separate 
        standards (including principle 7 of the code of conduct for data-driven health and care technology) will 
        apply to your DHT.
        """,
        "Great! You’re all set!"
    ]

    # TODO
    # NHSD_end_of_conversation = []

    @staticmethod
    def generate_seed(seed=None):
        if seed is not None:
            random.seed(seed)

    def random_hello(self, seed=None):
        self.generate_seed(seed)
        rand_index = random.randint(0, len(self.helloMessage_from_user) - 1)
        return self.helloMessage_from_user[rand_index]

    def random_yes(self, seed=None):
        self.generate_seed(seed)
        rand_index = random.randint(0, len(self.Yeses) - 1)
        return self.Yeses[rand_index]

    def random_no(self, seed=None):
        self.generate_seed(seed)
        rand_index = random.randint(0, len(self.Nos) - 1)
        return self.Nos[rand_index]

    def random_clarification(self, seed=None):
        self.generate_seed(seed)
        rand_index = random.randint(0, len(self.Clarification) - 1)
        return self.Clarification[rand_index]

    def random_initial_answer_for(self, question, seed=None):
        self.generate_seed(seed)
        answerList = self.initial_QandA.get(question)
        rand_index = random.randint(0, len(answerList) - 1)
        return self.initial_QandA[question][rand_index]


QUESTION = 0
YES = 1
NO = 2
CLARIFICATION = 3 # TODO: process clarification
IDENTIFIER = 4


class CSVData:
    """
    if string is "1 Line below", will return "1".
    if string is "You are unhealthy", will return "You are unhealthy"
    """

    @staticmethod
    def format_possible_offset(string):
        s = string.split(" ", 1)
        if s[0].isdigit():
            return s[0]
        else:
            return string

    # Drops identifier
    def csv_data(self, path):
        with open(path, 'r') as csv_file:
            data = []
            csv_reader = csv.reader(csv_file, delimiter=',')

            next(csv_reader, None)  # skip header during iteration
            for row in csv_reader:
                row[YES] = self.format_possible_offset(row[YES])
                row[NO] = self.format_possible_offset(row[NO])
                # row[CLARIFICATION] = self.format_possible_offset(row[CLARIFICATION]) --> no need
                # del row[CLARIFICATION] # TODO: make it work without this
                del row[IDENTIFIER]

                data.append(row)
            return data


"""
type: list of lists
Generates text and csv in target folder

Output format
[
[Question, UserInput-Sentence OR (Yes/No)],
[Following question OR Class, UserInput-Sentence OR (Yes/No)],
...,
]
"""


class GenerateConversation:
    history = []
    q_and_a = QandA()

    def __init__(self, filename):
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "tree", filename)
        organisation_name = filename[: filename.index('.')]  # string before the first dot
        self.target_path = os.path.join(dirname, "target", organisation_name)
        self.data = CSVData().csv_data(filepath)
        self.initial_q_and_a = self.q_and_a.initial_QandA
        del dirname, filepath, organisation_name

    def say_hello(self):
        self.history.append(["", self.q_and_a.random_hello()])

    def generate_initial(self):
        initials = self.data[:len(self.initial_q_and_a)]
        for initial in initials:
            rand_answer = self.q_and_a.random_initial_answer_for(initial[QUESTION])  # TODO: seed
            self.history.append([initial[QUESTION], rand_answer])

    """
    <Algorithm>
    while not the end of the list:
        check if it is end of the conversation
    
        randomly choose yes or no
            when yes -> randomly choose yes answer from q_and_a Yeses
            when no -> randomly choose no answer from q_and_a Nos
            
        if yes_or_no => yes:
            history.append([body[QUESTION], randomly_selected_answer])            
            skip the digit number of rows
            continue
                
        else yes_or_no => no:
            history.append([body[QUESTION], randomly_selected_answer])            
            skip the digit number of rows
            continue
    """

    def generate_body(self):
        bodies = iter(self.data[len(self.initial_q_and_a):])
        for body in bodies:
            # base case
            if body[QUESTION] in self.q_and_a.MHRA_end_of_conversation:
                self.history.append([body[QUESTION], ""])
                break

            # 1 -> yes  2 -> no
            yes_or_no = random.randint(1, 2)
            if yes_or_no == 1:
                rand_answer = self.q_and_a.random_yes()  # TODO: seed
                self.history.append([body[QUESTION], rand_answer])
                for _ in range(int(body[YES]) - 1):  # skip rows
                    next(bodies)
                continue

            else:  # yes_or_no==2 (NO)
                rand_answer = self.q_and_a.random_no()  # TODO: seed
                self.history.append([body[QUESTION], rand_answer])
                for _ in range(int(body[NO]) - 1):  # skip rows
                    next(bodies)
                continue

    def create_text_file(self, i=0):
        pass

    def create_csv_file(self, i=0):
        history_array = np.array(self.history)
        df = pd.DataFrame(history_array)
        df.to_csv(os.path.join(self.target_path, f"convos{i}.csv"), encoding='utf-8')
        del history_array

    def generate(self, i=0):
        self.say_hello()
        self.generate_initial()
        self.generate_body()
        # Debugging purpose
        # for x in self.history:
        #     print(x)
        self.create_text_file(i)
        self.create_csv_file(i)
        return self.history

if __name__ == '__main__':

    # csvdata = CSVData()
    # data = csvdata.csv_data("./tree/MHRA.csv")
    #
    # for x in data:
    #     if len(x[CLARIFICATION]) is not 0:
    #         print(x)

    # generate 10 test cases
    for index in range(10):
        gen = GenerateConversation("MHRA.csv")
        gen.history = []
        gen.generate(i=index)

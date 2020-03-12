import csv
import random
import numpy as np
import pandas as pd
import os


# question and answer examples
class QandA:
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
        "yes",
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
        "no",
    ]

    @staticmethod
    def generate_seed(seed=None):
        if seed is not None:
            random.seed(seed)

    def random_yes(self, seed=None):
        self.generate_seed(seed)
        rand_index = random.randint(0, len(self.Yeses) - 1)
        return self.Yeses[rand_index]

    def random_no(self, seed=None):
        self.generate_seed(seed)
        rand_index = random.randint(0, len(self.Nos) - 1)
        return self.Nos[rand_index]

    def random_initial_answer_for(self, question, seed=None):
        self.generate_seed(seed)
        answerList = self.initial_QandA.get(question)
        rand_index = random.randint(0, len(answerList) - 1)
        return self.initial_QandA[question][rand_index]


QUESTION = 0
YES = 1
NO = 2
CLARIFICATION = 3
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


class GenerateTest:
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

    def generate_initial(self):
        initials = self.data[:len(self.initial_q_and_a)]
        for initial in initials:
            rand_answer = self.q_and_a.random_initial_answer_for(initial[QUESTION])  # TODO: seed
            self.history.append([initial[QUESTION], rand_answer])

    """
    <Algorithm>
    while not the end of the list:
        randomly choose yes or no
            when yes -> randomly choose yes answer from q_and_a Yeses
            when no -> randomly choose no answer from q_and_a Nos
            
        history.append([body[QUESTION], randomly_selected_answer])
        if yes_or_no => yes:
            Look body[YES]
            if that was not digit:
                history.append([body[YES], ""])
                break
            else if that was a digit:
                skip the digit number of rows
                continue
                
        else if yes_or_no => no:
            Look body[NO]
            if that was not digit:
                history.append([body[NO], ""])
                break
            else if that was a digit:
                skip the digit number of rows
                continue
    """

    def generate_body(self):
        bodies = iter(self.data[len(self.initial_q_and_a):])
        for body in bodies:
            # 1 -> yes  2 -> no
            yes_or_no = random.randint(1, 2)
            if yes_or_no == 1:
                rand_answer = self.q_and_a.random_yes()  # TODO: seed
                self.history.append([body[QUESTION], rand_answer])

                if not body[YES].isdigit():
                    self.history.append([body[YES], ""])
                    break
                else:  # body[YES] is digit
                    for _ in range(int(body[YES]) - 1):  # skip rows
                        next(bodies)
                    continue

            else:  # yes_or_no==2 (NO)
                rand_answer = self.q_and_a.random_no()  # TODO: seed
                self.history.append([body[QUESTION], rand_answer])

                if not body[NO].isdigit():
                    self.history.append([body[NO], ""])
                    break
                else:  # body[NO] is digit
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
        self.generate_initial()
        self.generate_body()
        # Debugging purpose
        # for x in self.history:
        #     print(x)
        self.create_text_file(i)
        self.create_csv_file(i)
        self.history = []   # clean history for many generations # TODO: why doesn't this work?


if __name__ == '__main__':

    # generate 10 test cases
    for index in range(10):
        gen = GenerateTest("MHRA.csv")
        gen.history = []
        gen.generate(i=index)

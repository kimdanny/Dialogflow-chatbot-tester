import csv
import random
import numpy as np
import pandas as pd
import os
from QandA import QandA

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
        self.organisation_name = filename[: filename.index('.')]  # string before the first dot
        self.target_path = os.path.join(dirname, "target", self.organisation_name)
        self.data = CSVData().csv_data(filepath)
        self.initial_q_and_a = self.q_and_a.initial_QandA
        del dirname, filepath

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
            if self.organisation_name == "MHRA":
                if body[QUESTION] in self.q_and_a.MHRA_end_of_conversation:
                    self.history.append([body[QUESTION], ""])
                    break
            if self.organisation_name == "NHSD":
                if body[QUESTION] in self.q_and_a.NHSD_end_of_conversation:
                    self.history.append([body[QUESTION], ""])
                    break
            if self.organisation_name == "NICE":
                if body[QUESTION] in self.q_and_a.NICE_end_of_conversation:
                    self.history.append([body[QUESTION], ""])
                    break
            if self.organisation_name == "Final":
                if body[QUESTION] in self.q_and_a.Final_end_of_conversation:
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

# if __name__ == '__main__':
#     for index in range(10):
#         gen = GenerateConversation('Final.csv')
#         gen.history = []
#         conversation = gen.generate(i=index)
#         print(conversation)
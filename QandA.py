import random


# question and answer examples
class QandA:
    helloMessage_from_user = [
        # "hello",
        # "hey",
        # "I want to start the chat",
        # "let's start",
        # "hey man",
        "hi"
    ]

    initial_QandA = {
        "What’s your name?": [
            # "I'm Danny",
            # "Ryan Zhao",
            # "I am Xinyao Chuah",
            # "my name is Joseph Connor",
            # "Riyan Kim",
            # "Haaroon Yousaf",
            # "Dean Mohamedally",
            # "Yun Fu",
            # "i am toeun",
            "my name is danny"
        ],

        "What is the name of the contact person in your organization?": [
            # "He is Anthony Connor",
            # "John Doe",
            "Joseph"
        ],

        # TODO: Can you generate strings based on regex?
        "What is their email address?": [
            # "adfaff@email.com",
            # "123email456@gmail.com",
            # "email456thisone@hotmail.com",
            # "1iam2sohot3baby@hotbaby.co.uk",
            # "thisisfake@fakeuni.ac.fakecountrycode",
            "sampleemail@gmail.com"
        ],

        "What is their phone number?": [
            # "01012345678",
            # "074847572823",
            # "It is +447394817293",
            # "+447394817293",
            # "+3569877675525",
            "It's 07394817293"
        ],

        "What is your organisation's name": [
            # "it is Google",
            # "it's called Facebook",
            # "RCGP",
            # "the name of the organisation is named carefulAI",
            "carefulai"
        ],

        "What is your organisation's address?": [
            # "24 bedford way",
            # "Lebus St. Tottenham Hale, London N17 9FD",
            # "It's Lebus St. Tottenham Hale, London N17 9FD",
            "it is 48 marchmount street, London"
        ]
    }

    Yeses = [
        # "yes that is correct",
        # "that is correct",
        # "they do",
        # "does",
        # "it does",
        # "yup",
        # "y",
        # "right",
        # "yes it does",
        "yes"
    ]

    Nos = [
        # "no that is not correct",
        # "that is not correct",
        # "that is incorrect",
        # "they don't",
        # "does not",
        # "it doesn't",
        # "nop",
        # "n",
        # "wrong",
        # "no it does not",
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

    NHSD_end_of_conversation = [
        "Great! You’re all set!"
    ]

    Final_end_of_conversation = [
        "Great! You’re all set! Now you can look up our suggestions. Next time you visit us, you can look up your previous chat history!"
    ]

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

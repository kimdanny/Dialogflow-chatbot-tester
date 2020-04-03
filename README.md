# Dialogflow-chatbot-tester

**Disclaimer**  
This test is suitable for chatbots that walk through a decision tree.

## Getting Ready
1. You need to first build csv formatted file(s) that represents your decision tree.  
The first line of the CSV file must contain the following header:  
    `Questions,Yes,No,Clarification,Unique Identifier`   
You can take a closer look on how the form looks like and how it can be parsed and used from 
[chatbot-builder from tree](https://github.com/ryanchuah/chatbot-builder-from-tree)

2. For **Unit Testing**, place part of your CSV tree under `tree` folder.  
In my case, under `tree` folder, I have MHRA.csv, NICE.csv and NHSD.csv (named as <organisation_name>.csv ).

3. For **Integration Testing**, place the integrated CSV file under the `tree` folder.

4. Get your chatbot's back-end running.  
To test our chatbot, Clone [Chatbot Backend](https://github.com/ryanchuah/compliance-backend) and run the server.  
This tester will send a POST request to _inputText API_ and retrieve the bot's response.  
You must finish all the steps to run your Dialogflow chatbot (e.g. filling up your hidden .env file with Dialogflow credentials).


## Getting Started
1. If you are running our project, simply run `test.py` and left points below as options. Otherwise, start from step 2.

2. Navigate to **QandA.py** and modify various data as you want. The more data you put in to the dictionaries, 
the more the generated conversations will be randomised, thus adding more stress to your chatbot.

3. Navigate to **generate.py** and place appropriate CSV file name in GenerateConversation().generate_body() and check if GenerateConversation().generate() works.
You should see that `target` directory, which contains randomly generated convos as csv, in your root folder.

4. Navigate to **test.py** and place appropriate CSV file name in `files` list and run `test.py`. You can see SUCCESS or FAIL on your terminal for each test case.

## Extensibility
1. Generate an HTML report
2. Create convos.txt file
3. Make this repository as a package

### Author
* [To Eun Kim](https://github.com/kimdanny)

### License
This project is licensed under the MIT License. Check [LICENSE.md](LICENSE.md) for more details.
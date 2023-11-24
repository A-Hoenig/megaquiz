import gspread # needed for access to google sheets to store user wrong questions
import html #needed to decode html specials in quiz questions
import requests #needed to request questions from open trivia DB API
import json #needed to help parse the recieved json strings
import os #access to cli clear command to clear out previous text
import random #needed to shuffle answers

from google.oauth2.service_account import Credentials
from pprint import pprint

# connect to google sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('training_questions')

def generate_new_token():
    """
    requests a new token from open trivia API and returns the string only
    """
    url = "https://opentdb.com/api_token.php?command=request"
    response = requests.get(url)
    response_json = response.json()
    return response_json['token'] #used once per game to prevent duplicate questions

def get_categories():
    """
    function to retrieve all available categories from open Trivia DB and the associated category code
    """
    category_list = requests.get('https://opentdb.com/api_category.php')
    category_list_json = category_list.json()
    return category_list_json

def get_questions(number, category, question_type, difficulty, token):
    """
    Main function to generate API query string from given inputs.
    Token is required per session to prevent repeated questions
    returns a json dictionary containing requested number of questions from given type and category
    setting parameters to ANY opens up request to ANY categories or difficulties or types
    default number of questions is 10
    number, category are integers, difficulty = 'easy', 'medium', 'hard' strings
    """
    url_no_of_questions = f'amount={number}'

    if category == 'ANY':
        url_category = ""
    else:
        url_category = f'&category={category}'

    if question_type == "ANY":
        url_type = ""
    else:
        url_type = f'&type={question_type}'

    if difficulty == "ANY":
        url_difficulty = ""
    else:
        url_difficulty = f'&difficulty={difficulty}'

    url_token = f'&token={token}'

    questions_url = ('https://opentdb.com/api.php?' + url_no_of_questions + url_category + url_difficulty + url_type + url_token)
    questions = requests.get(questions_url)
    questions_json = questions.json()
    
    return questions_json

def reset_cli (readout_line):
    """
    clears the CLI and repaints the quiz header graphics. 
    Score or messages can be passed in the readout_line
    """
    os.system('clear') #clear the cli first
    str_title = '''
Welcome to
┳┳┓┏┓┏┓┏┓  ┏┓┳┳┳┏┓
┃┃┃┣ ┃┓┣┫  ┃┃┃┃┃┏┛
┛ ┗┗┛┗┛┛┗  ┗┻┗┛┻┗┛
'''
    print(str_title)
    print('\u23AF' * 50)
    print(f'{readout_line}')
    print('\u23AF' * 50)

def display_main_menu():
    '''
    displays the main menu to start the quiz.
    also gives option to go into settings and change quiz parameters
    '''
    global num
    global difficulty
    global question_type
    global category
    global training_mode
    
    reset_cli("Main Menu")
    print(f'\n1. Start Quiz\n2. Enter Game Settings\n\nNext Quiz will be :\nQuestions:\u0009{num}\nDifficulty:\u0009{difficulty}\nType:\u0009\u0009{question_type}\nCategory:\u0009{category}\n')
    while True:
        try:
            user_input = int(input('Select your option: '))
            if 1 <= user_input <= 2:
                if user_input == 1:
                    print("START THE QUIZ!!")
                    question_list = get_questions(num, category, question_type, difficulty, tok)
                    display_quiz(question_list)
                    exit()
                else:
                    display_settings()
            else:
                print("Please enter 1 or 2!")
        except ValueError:
            print('Please enter a number!')

def display_settings():
    '''
    displays the settings options and calls appropriate functions to change the global variables for the quiz parameters
    '''
    global num
    global difficulty
    global question_type
    global category
    global training_mode

    reset_cli("Settings")

    if question_type == "boolean":
        str_question_type = "True/False"
    elif question_type == "multiple":
        str_question_type = "Multiple Choice"
    else:
        str_question_type = "ANY"

    print(f'\n1. Number of Questions:\u0009{num}\n2. Change Difficulty:\u0009{difficulty}\n3. Change Type:\u0009\u0009{str_question_type}\n4. Change Category:\u0009{display_category(category,category_list)}\n5. Training Mode:\u0009{training_mode}\n6. Exit Settings \n')
    print('Turning on training mode will remember questions you got wrong\nYou can then select "training" as a category to build quizzes\nusing only previously wrong questions\n')
    while True:
            try:
                user_input = int(input('Select your option: '))
                if 1 <= user_input <= 6:
                    match user_input:
                        case 1:
                            no_of_questions()
                        case 2:
                            change_difficulty()
                        case 3:
                            change_type()
                        case 4:
                            change_category()
                        case 5:
                            toggle_training_mode()
                        case 6:
                            display_main_menu()
                else:
                    print("Please enter 1 - 6!")
            except ValueError:
                print('Please enter a number!')

def no_of_questions():
    '''
    Allow user to change the number of questions per quiz. Changes the global variable
    '''
    global num

    reset_cli('Number of Questions:')
    while True:
        try:
            user_input = int(input('\nType how many questions you would like (1-50):\n'))
            if 1 <= user_input <= 50:
                num = user_input
                display_settings()
                break
            else:
                print("Please enter a value from 1 to 50!")
        except ValueError:
            print('Please enter a number!')

def change_difficulty():
    '''
    Allow user to change the difficulty level of quiz. Changes the global variable
    '''
    global difficulty

    reset_cli('Difficulty Level')
    while True:
        try:
            print(f'\n1. ANY\n2. easy\n3. medium\n4. hard\n')
            user_input = int(input('\nPLease select the difficulty level:\n'))
            if 1 <= user_input <= 4:
                match user_input:
                        case 1:
                            difficulty = 'ANY'
                        case 2:
                            difficulty = 'easy'
                        case 3:
                            difficulty = 'medium'
                        case 4:
                            difficulty = 'hard'
                display_settings()
                break
            else:
                print("Please enter a value from 1 to 4!")
        except ValueError:
            print('Please enter a number!')

def change_type():
    '''
    Allow user to change the type of quiz. (multpile choice, true or false or both (ANY). Changes the global variable
    '''
    global question_type

    reset_cli('Question Types')
    while True:
        try:
            print(f'\n1. ANY\n2. Multiple Choice\n3. True/False\n')
            user_input = int(input('\nPlease select the question type:\n'))
            if 1 <= user_input <= 3:
                match user_input:
                        case 1:
                            question_type = 'ANY'
                        case 2:
                            question_type = 'multiple'
                        case 3:
                            question_type = 'boolean'
                display_settings()
                break
            else:
                print("Please enter a value from 1 to 3!")
        except ValueError:
            print('Please enter a number!')

def change_category ():
    '''
    Allow user to change the category.list pulled from open quiz DB. Changes the global variable
    '''
    global category

    reset_cli('Available Categories')
    print(create_category_list(category_list))
    
    while True:
        try:
            user_input = int(input('\nPlease type the number of the category:\n'))
            if 7 <= user_input <= 32:
                if user_input == 7:
                    category = 'Training'
                elif user_input == 8:
                    category = 'ANY'
                else:
                    category = user_input
                display_settings()
            else:
                print("Please enter a valid category number!")
        except ValueError:
            print('Please enter a number!')

def display_category(id, category_list):
    '''
    function to return the category name based on the given ID
    '''
    trivia_categories = category_list.get("trivia_categories", [])
    #loop through to find given ID
    for cat in trivia_categories:
        #check for ID match
        if cat.get('id') == id:
            #return cat name
            return cat.get('name')
    if id == "Training":
        return 'Training'
    else:
        return 'ANY' #if ID not found

def create_category_list(categories):
    '''
    pass API category data and create string to display in settings menu for category selection
    '''
    str_categories = "7 -- TRAINING Category (Previous wrong questions)\n8 -- ANY category\n"
    trivia_categories = categories.get('trivia_categories', [])
    #loop through entries:
    for cat in trivia_categories:
        #get ID and name
        cat_id = cat.get('id')
        cat_name = cat.get('name')
        #append to string
        str_categories += f'{cat_id} -- {cat_name}\n'
    
    #return the completed string
    return str_categories

def toggle_training_mode():
    '''
    toggle training more on or off
    used to determine if wrong questions should be stored on the google sheet
    '''
    global training_mode

    if training_mode == 'OFF':
        training_mode = 'ON'
    else:
        training_mode = 'OFF'
    display_settings()

def format_question(raw_question_list, n):
    '''
    returns the nth question from the given raw question list in a proper
    format. Answers are shuffled and category + difficulty added
    '''
    #get nth question from given list
    q = raw_question_list['results'][n]

    #add question first
    individual_question = f'\n{html.unescape(q['question'])}\n{html.unescape(q['category'])} ({q['difficulty']})\n\n'
    #add answer
    if q['type'] == 'boolean':
        correct_answer_number = 1 if q['correct_answer'] == 'True' else 2
        individual_question += f'1. True\n2. False\n' # T/F question only needs std 2 answers

    else:
        answers = [html.unescape(q['correct_answer'])] + html.unescape(q['incorrect_answers'])
        random.shuffle(answers) #shuffle so correct answer is not always 1
        #add answers underneath question string
        for i, ans in enumerate(answers, start=1): # don't use 0 for first answer
            individual_question += f'{i}. {ans}\n' # number and add all answers
            if ans == html.unescape(q['correct_answer']):
                correct_answer_number = i

    return individual_question, correct_answer_number

def display_quiz(raw_question_list):
    '''
    main quiz function that loops through all given questions, displays one by one,
    processes user answer and updates the scores.
    If training mode is on, function will also append a list of the incorrect answers and export to google sheet
    '''
    global correct, wrong, training_mode
    
    for question_count, _ in enumerate(raw_question_list['results'], start = 1): # display first question as 1, not 0

        percentage = correct / num  * 100 #num must never be zero ... set to default 10
        status = f'Question {question_count} of {num}. Correct: {correct} / Wrong: {wrong}. ({round(percentage,1)}%)'
        reset_cli(f'{status}')

        # display formatted question
        print(f'{format_question(raw_question_list, question_count-1)[0]}\n') # real question index ( = -1 )
        correct_answer = format_question(raw_question_list, question_count-1)[1]

        print(correct_answer)

        # get user answer and validate
        if raw_question_list['results'][question_count-1]['type'] == 'boolean': #set how many valid answers there are
            qs = 2
        else:
            qs = 4

        while True:
            try:
                user_answer = int(input(f"Select Answer: (type 1 - {qs})\n"))
                if 1 <= user_answer <= qs: #valid answer
                    # compare answers and update scores
                    if user_answer == correct_answer:
                        correct +=1
                        status = f'Question {question_count} of {num}. Correct: {correct} / Wrong: {wrong}. ({round(percentage,1)}%)'
                    else:
                        wrong += 1
                        status = f'Question {question_count} of {num}. Correct: {correct} / Wrong: {wrong}. ({round(percentage,1)}%)'
                    break
                else:
                    print(f"Please enter 1 or {qs}!")
            except ValueError:
                print('Please enter a number!')

    reset_cli(f'{status}') #update cli after last question
    print('quiz ended!')
    
        

######################################################################################

#global variables/defaults to keep track of selected quiz parameters
category_list = get_categories() #get and store list of categories from Trivia DB
category = 'ANY' # number of category or ANY
question_type = 'ANY' #multiple, boolean, ANY
difficulty = 'ANY' # easy, medium, hard, ANY
num = 3
training_mode = "OFF"
tok = generate_new_token()
correct = 0
wrong = 0


#launch quiz CLI app
display_main_menu()

# questions = SHEET.worksheet('questions')
#                             data = questions.get_all_values()
#                             pprint(data)

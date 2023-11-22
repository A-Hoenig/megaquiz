import gspread # needed for access to google sheets to store user wrong questions
import html #needed to decode html specials in quiz questions
import requests #needed to request questions from open trivia DB API
import json #needed to help parse the recieved json strings
import os #access to cli clear command to clear out previous text

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
    function to retrieve all available categories form open Trivia DB and the associated category code
    """
    category_list = requests.get('https://opentdb.com/api_category.php')
    category_list_json = category_list.json()
    return category_list_json

def get_questions(number, category, question_type, difficulty, token):
    """
    Main function to generate API query string from given inputs.
    Token is required per session to prevent repeated questions
    returns a json dictionary containing requested number of questions from given type and category
    setting parameters to ANY opens up request to ANYL categories or difficulties or types
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
    print('\u23AF' * 40)
    print(f'    {readout_line}')
    print('\u23AF' * 40)

def display_main_menu():
    '''
    resets the CLI and then displays the main menu to start the quiz.
    also gives option to go into settings and change quiz parameters
    '''
    global num
    global difficulty
    global question_type
    global category
    global training_mode
    
    reset_cli("Main Menu:")
    print(f'Select number to proceed:\n\n1. Start Quiz\n2. Enter Game Settings\n\nNext Quiz will be :\nQuestions:\u0009{num}\nDifficulty:\u0009{difficulty}\nType:\u0009\u0009{question_type}\nCategory:\u0009{category}\n\nEnter a number to proceed')
    while True:
        try:
            user_input = int(input('Select your option: '))
            if 1 <= user_input <= 2:
                if user_input == 1:
                    print("START THE QUIZ!!")
                    exit()
                else:
                    display_settings()
            else:
                print("Please enter 1 or 2!")
        except ValueError:
            print('Please enter a number!')

def display_settings():
    global num
    global difficulty
    global question_type
    global category
    global training_mode

    reset_cli("Settings:")
    print(f'\n1. Number of Questions:\u0009{num}\n2. Change Difficulty:\u0009{difficulty}\n3. Change Type:\u0009\u0009{question_type}\n4. Change Category:\u0009{category}\n5. Training Mode:\u0009{training_mode}\n6. Exit Settings \n')
    print('Turning on training mode will remember questions you got wrong\nYou can then select "training" as a category to build quizzes\nusing only previously wrong questions\n')
    while True:
            try:
                user_input = int(input('Select your option: '))
                if 1 <= user_input <= 6:
                    match user_input:
                        case 1:
                            print("one")
                            no_of_questions()
                        case 2:
                            print("two")
                            change_difficulty()
                        case 3:
                            print("three")
                            change_type()
                        case 4:
                            print("four")
                            print(get_categories())
                        case 5:
                            print('five')
                            questions = SHEET.worksheet('questions')
                            data = questions.get_all_values()
                            pprint(data)
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

    reset_cli('Difficulty Level:')
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
    Allow user to change the type of quiz. (multpile choice, true or false or noth (ANY). Changes the global variable
    '''
    global question_type

    reset_cli('Question Types:')
    while True:
        try:
            print(f'\n1. ANY\n2. Multiple Choice\n3. True/False\n')
            user_input = int(input('\nPLease select the question type:\n'))
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

######################################################################################

category = 'ANY' # number of category or ANY
question_type = 'ANY' #multiple, boolean, ANY
difficulty = 'ANY' # easy, medium, hard, ANY
num = 20
training_mode = "OFF"
tok = generate_new_token()


display_main_menu()



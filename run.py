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
    setting parameters to ALL opens up request to ALL categories or difficulties or types
    default number of questions is 10
    number, category are integers, difficulty = 'easy', 'medium', 'hard' strings
    """
    url_no_of_questions = f'amount={number}'

    if category == 'ALL':
        url_category = ""
    else:
        url_category = f'&category={category}'

    if question_type == "ALL":
        url_type = ""
    else:
        url_type = f'&type={question_type}'

    if difficulty == "ALL":
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

def display_main_menu(num, diff, question_type, cat):
    reset_cli("Main Menu:")
    print(f'Select number to proceed:\n\n1. Start Quiz\n2. Enter Game Settings\n\nNext Quiz will be :\nQuestions:\u0009{num}\nDifficulty:\u0009{diff}\nType:\u0009\u0009{question_type}\nCategory:\u0009{cat}\n\nEnter a number to proceed')
    while True:
        try:
            user_input = int(input('Select your option: '))
            if 1 <= user_input <= 2:
                return user_input
            else:
                print("Please enter 1 or 2!")
        except ValueError:
            print('Please enter a number!')

def display_settings(num, diff, question_type, cat, training_mode):
    reset_cli("Settings:")
    print(f'\n1. Number of Questions:\u0009{num}\n2. Change Difficulty:\u0009{diff}\n3. Change Type:\u0009\u0009{question_type}\n4. Change Category:\u0009{cat}\n4. Training Mode:\u0009{training_mode}\n5. Exit Settings \n')
    while True:
            try:
                user_input = int(input('Select your option: '))
                if 1 <= user_input <= 5:
                    return user_input
                else:
                    print("Please enter 1 - 5!")
            except ValueError:
                print('Please enter a number!')
######################################################################################

cat = 'ALL' # number of category or ALL
question_type = 'ALL' #multiple, boolean, ALL
diff = 'ALL' # easy, medium, hard, ALL
num = 20
training_mode = "ON"
tok = generate_new_token()

user_selection = display_main_menu(num, diff, question_type, cat)
if user_selection == 1:
    print('START THE QUIZ')
else:
    settings_selection = display_settings(num, diff, question_type, cat, training_mode)
    print(f'You selected {settings_selection}')

# print(get_questions(num, cat, question_type, diff, tok))





# questions = SHEET.worksheet('questions')

# data = questions.get_all_values()

# pprint(data)

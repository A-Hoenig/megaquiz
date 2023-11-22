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
    print('---------------------------------------')
    print(f'    {readout_line}')
    print('---------------------------------------')



######################################################################################
reset_cli("Hello")

cat = 'ALL' # number of category or ALL
question_type = 'ALL' #multiple, boolean, ALL
diff = 'ALL' # easy, medium, hard, ALL
num = 20
tok = generate_new_token()
# print(get_questions(num, cat, question_type, diff, tok))





# questions = SHEET.worksheet('questions')

# data = questions.get_all_values()

# pprint(data)

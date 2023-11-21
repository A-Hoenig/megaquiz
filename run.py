import gspread # needed for access to google sheets to store user wrong questions
import html #needed to decode html specials in quiz questions
import requests

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

#connect to Open Trivia database
url = "https://opentdb.com/api_token.php?command=request"
response = requests.get(url)
response_json = response.json()
token = response_json['token'] #store session token - used once per game to prevent duplicate questions



int_number_of_questions = 10
url_questions = f'amount={int_number_of_questions}'

category = 20
url_category = f'&category={category}'

difficulty = 'hard'
url_difficulty = f'&difficulty={difficulty}'

url_token = f'&token={token}'

questions_url = ('https://opentdb.com/api.php?' + url_questions + url_category + url_difficulty + url_token)

questions = requests.get(questions_url)
questions_json = questions.json()

print(questions_json)

category_list = requests.get('https://opentdb.com/api_category.php')
category_list_json = category_list.json()
print(f'Available Categories:\n {category_list_json}')

# questions = SHEET.worksheet('questions')

# data = questions.get_all_values()

# pprint(data)

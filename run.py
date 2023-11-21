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






# questions = SHEET.worksheet('questions')

# data = questions.get_all_values()

# pprint(data)

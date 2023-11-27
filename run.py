import gspread # needed for access to google sheets to store user wrong questions
import html #needed to decode html specials in quiz questions
import requests #needed to request questions from open trivia DB API
import json #needed to help parse the recieved json strings
import os #access to cli clear command to clear out previous text
import random #needed to shuffle answers

from pyfiglet import Figlet #generate ASCII text art / fonts for CLI (install with  pip install pyfiglet)
from google.oauth2.service_account import Credentials #secure IO access to google sheets
from datetime import date # for timestamp when wrong questions are added to google sheet

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
    Main function to generate API query string from given inputs / global variables
    Token is required per session to prevent repeated questions
    returns a json dictionary containing requested number of questions from given type and category
    setting parameters to ANY opens up request to ANY categories or difficulties or types
    number, category are integers, difficulty = 'easy', 'medium', 'hard' type = 'boolean', 'multiple' strings
    """
    url_no_of_questions = f'amount={number}' # always pass number for questions requested (max 50)

    if category == 'ANY': #if setting is ANY, omit category string from URL
        url_category = ""
    else:
        url_category = f'&category={category}'

    if question_type == "ANY": #if setting is ANY, omit type string from URL
        url_type = ""
    else:
        url_type = f'&type={question_type}'

    if difficulty == "ANY": #if setting is ANY, omit category difficultyfrom URL
        url_difficulty = ""
    else:
        url_difficulty = f'&difficulty={difficulty}'

    url_token = f'&token={token}' # add session token last to ensure unique question session

    questions_url = ('https://opentdb.com/api.php?' + url_no_of_questions + url_category + url_difficulty + url_type + url_token) #build complete API URL
    questions = requests.get(questions_url) #get the questions
    questions_json = questions.json()
    
    return questions_json

def reset_cli (readout_line):
    """
    clears the CLI and repaints the quiz header graphics. 
    Score or messages can be passed in the readout_line
    """
    os.system('clear') #clear the cli first
    
    custom_ascii_font = Figlet(font='graffiti') # change font name for different styles
   
    print('Welcome to')
    print(custom_ascii_font.renderText('MEGA\nQUIZ'))

    print('\u23AF' * 50) # creates continuous line of 50 characters
    print(f'{readout_line}')
    print('\u23AF' * 50)

def display_main_menu():
    '''
    displays the main menu to start the quiz as well as change the quiz parameters
    '''
    global num
    global difficulty
    global question_type
    global category
    global training_mode
    
    reset_cli("Main Menu")

    # display user readable text instead of boolean or multiple
    if question_type == "boolean":
        str_question_type = "True/False"
    elif question_type == "multiple":
        str_question_type = "Multiple Choice"
    else:
        str_question_type = "ANY"

    # print the menu items with the current set global variables
    print(f'\n1. Start Quiz\n\n2. Number of Questions:\u0009{num}\n3. Change Difficulty:\u0009{difficulty}\n4. Change Type:\u0009\u0009{str_question_type}\n5. Change Category:\u0009{display_category(category,category_list)}\n6. Training Mode:\u0009{training_mode}\n')
    print('Turning on training mode will remember questions you got wrong\nYou can then select "training" as a category to build quizzes\nusing only previously wrong questions\n')
    
    # get user menu selection and validate input
    while True:
        try:
            user_input = int(input('Select your option: '))
            if 1 <= user_input <= 6:
                match user_input:
                    case 1:
                        print("... GENERATING THE QUIZ ...")
                        question_list = get_questions(num, category, question_type, difficulty, tok)
                        run_quiz(question_list)
                        exit()
                    case 2:
                        no_of_questions()
                    case 3:
                        change_difficulty()
                    case 4:
                        change_type()
                    case 5:
                        change_category()
                    case 6:
                        toggle_training_mode()
        
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

    #get user selection and validate input
    while True:
        try:
            user_input = int(input('\nType how many questions you would like (1-50):\n'))
            if 1 <= user_input <= 50:
                num = user_input
                display_main_menu()
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

    #get user selection and validate input
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
                display_main_menu()
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

    #get user selection and validate input
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
                display_main_menu()
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
    
    #get user selection and validate input
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
                display_main_menu()
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
    if id == "Training": #special category to get questions from google sheet (collection of previous wrong answers)
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
    display_main_menu()

def format_question(raw_question_list, n):
    '''
    returns the nth question from the given raw question list in a proper format as well as the correct answer number
    Answers are shuffled and category + difficulty added. 
    '''
    #get nth question from given list
    q = raw_question_list['results'][n]
   
    #add question first and add category and difficulty to it
    individual_question = f'\n{html.unescape(q['question'])}\n{html.unescape(q['category'])} ({q['difficulty']})\n\n'
    
    #add answers
    if q['type'] == 'boolean':
        correct_answer_number = 1 if q['correct_answer'] == 'True' else 2
        individual_question += f'1. True\n2. False\n' # T/F question only needs std 2 answers
    else:
        answers = html.unescape([q['correct_answer']] + q['incorrect_answers'])
        random.shuffle(answers) #shuffle so correct answer is not always 1
        #add answers underneath question string
        for i, ans in enumerate(answers, start=1): # don't use 0 for first answer
            
            individual_question += f'{i}. {ans}\n' # number and add all answers
            if ans == q['correct_answer']:
                correct_answer_number = i
   
    return individual_question, correct_answer_number

def add_question_to_sheet(question_list):
    '''
    recieves list of wrong questions and extracts the data into a single key / column match
    then saves the data to the google sheet via API
    also adds the date when the question was added.
    '''
    destination = SHEET.worksheet('questions')
  
    print("Saving wrong questions for training category...")
    
    # EXTRACT data from wrong question list
    for q in question_list:
        data = [q['type'], q['difficulty'], q['category'], q['question'], q['correct_answer']]
        wrong_answers = q['incorrect_answers']
        if q['type'] == 'boolean': #add 2 blank wrong answers to keep sheet column matching
            wrong_answers.extend(['', ''])
        data.extend(wrong_answers)

        #add date to end of data to track when question was added
        todays_date = date.today()
        str_todays_date = todays_date.strftime('%Y.%m.%d')

        data.append(str_todays_date)

        destination.append_row(data) #add data to google sheet

    print("Questions saved")

def get_wrong_questions():
    '''
    Function retrieves the saved data from the google sheet stored questions.
    Data is then reconfigured into the same format recieved from Trivia API
    this can be passed to normal quiz functions to generate a quiz.
    '''
    wrong_questions_dict = {'response_code': 0, 'results': []} # build dict in same format as returned from the API
    questions = SHEET.worksheet('questions')
    data = questions.get_all_values()

    for item in data[1:]: #iterate through sheet data and append to new dictionary
        temp_dict = {
            'type': item[0],
            'difficulty': item[1],
            'category': item[2],
            'question': item[3],
            'correct_answer': item[4],
            'incorrect_answers': item[5:8]
        }
        wrong_questions_dict['results'].append(temp_dict)
    
    return wrong_questions_dict
    
def run_quiz(raw_question_list):
    '''
    main quiz function that loops through all given questions, displays one by one,
    processes user answer and updates the scores.
    If training mode is on, function will also append a list of the incorrect answers and export to google sheet
    '''
    global correct, wrong, training_mode
    wrong_questions_list = []

    for question_count, question_data in enumerate(raw_question_list['results'], start = 1): # start loop, display first question as 1, not 0

        percentage = correct / num  * 100 #num must never be zero ... set to default 10
        status = f'Question {question_count} of {num}. Correct: {correct} / Wrong: {wrong}. ({round(percentage,1)}%)'
        reset_cli(f'{status}') # reset CLI before showing first question

        # get formatted question
        result = format_question(raw_question_list, question_count-1) #returns formatted question, answers, as well as correct answer
        print(f'{result[0]}\n') # first tuple result from format function - prints question to CLI
        correct_answer = result[1] #second tuple result from format function - store correct answer
        
        print(f'Debug: CorrectAnswerNo: {correct_answer}') #######################     DELETE ME     ##########################################

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
                    else:
                        wrong += 1
                        if training_mode == "ON":
                            wrong_questions_list.append({'type': question_data['type'],
                                                   'difficulty': question_data['difficulty'],
                                                   'category': question_data['category'],
                                                   'question': question_data['question'],
                                                   'correct_answer': question_data['correct_answer'],
                                                   'incorrect_answers': question_data['incorrect_answers']})
                    break
                else:
                    print(f"Please enter 1 or {qs}!")
            except ValueError:
                print('Please enter a number!')
                
            status = f'Question {question_count} of {num}. Correct: {correct} / Wrong: {wrong}. ({round(percentage,1)}%)' #update status bar

    percentage = correct / num  * 100 #final calc after last question
    status = f'Question {question_count} of {num}. Correct: {correct} / Wrong: {wrong}. ({round(percentage,1)}%)'
    reset_cli(f'{status}') #update cli after last question
    print('Quiz ended!')
        
    #export wrong questions to google sheet
    if training_mode == "ON":
        add_question_to_sheet(wrong_questions_list)
    
###########################################################################
### global variables/defaults to keep track of selected quiz parameters ###
###########################################################################

category_list = get_categories() #get and store list of categories from Trivia DB
category = 'ANY' # number of category or ANY
question_type = 'ANY' #multiple, boolean, ANY
difficulty = 'ANY' # easy, medium, hard, ANY
num = 5 #default number of questions. Do not set to 0!
training_mode = "ON"
tok = generate_new_token()
correct = 0
wrong = 0

#launch quiz CLI app
# display_main_menu()

q = format_question(get_wrong_questions(),0)
print (q[0])



import gspread  # access to google sheets to store user wrong questions
import html  # needed to decode html specials in quiz questions
import requests  # needed to request questions from open trivia DB API
import json  # needed to help parse the recieved json strings
import os  # access to cli clear command to clear out previous text
import random  # needed to shuffle answers
import time  # used for pausing to display messages
import getpass  # used to input passwords without showing letters

from pyfiglet import Figlet  # generate CLI ASCII text art/fonts
from google.oauth2.service_account import Credentials  # IO access to google
from datetime import date  # needed for delays


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
    return response_json['token']  # prevent duplicate questions


def get_categories():
    """
    function to retrieve all available categories
    from open Trivia DB and the associated category code
    """
    category_list = requests.get('https://opentdb.com/api_category.php')
    category_list_json = category_list.json()
    return category_list_json


def get_questions(number, category, question_type, difficulty, token):
    """
    Main function to generate API query string from inputs / global variables
    Token is required per session to prevent repeated questions
    returns a json dictionary containing requested number of questions
    from given type and category setting parameters to ANY opens up request
    to ANY categories or difficulties or types. number, category are integers
    difficulty = 'easy', 'medium', 'hard' type = 'boolean', 'multiple' strings
    """
    url_no_of_questions = f'amount={number}'  # pass number of questions

    if category == 'ANY':  # if setting is ANY, omit category string from URL
        url_category = ""
    else:
        url_category = f'&category={category}'

    if question_type == "ANY":  # if setting is ANY, omit type string from URL
        url_type = ""
    else:
        url_type = f'&type={question_type}'

    if difficulty == "ANY":   # omit category difficulty from URL for ANY
        url_difficulty = ""
    else:
        url_difficulty = f'&difficulty={difficulty}'

    url_token = f'&token={token}'  # ensure unique question session

    questions_url = ('https://opentdb.com/api.php?'
                     + url_no_of_questions
                     + url_category
                     + url_difficulty
                     + url_type
                     + url_token)  # build complete API URL

    questions = requests.get(questions_url)  # get the questions
    questions_json = questions.json()

    return questions_json


def reset_cli(readout_line):
    """
    clears the CLI and repaints the quiz header graphics.
    Score or messages can be passed in the readout_line
    """
    os.system('clear')  # clear the cli first

    custom_ascii_font = Figlet(font='standard')  # choose font

    print('Welcome to')
    print(custom_ascii_font.renderText('MEGA-QUIZ'))

    print('\u23AF' * 50)  # creates continuous line of 50 characters
    print(f'{readout_line}')
    print('\u23AF' * 50)


def display_main_menu():
    '''
    displays the main menu to start the quiz
    as well as change the quiz parameters
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
    print(
        f'\n1. Start Quiz\n\n'
        f'2. Number of Questions:\u0009{num}\n'
        f'3. Change Difficulty:\u0009{difficulty}\n'
        f'4. Change Type:\u0009\u0009{str_question_type}\n'
        f'5. Change Category:\u0009{display_category(category,category_list)}'
        f'\n6. Training Mode:\u0009{training_mode}\n'
        f'7. Log In\u0009\u0009{user}\n'
        f'8. Exit MegaQuiz\n'
        )

    print(
        f'Turn on training mode to track wrong questions\n'
        f'Then select "Training" category to practice them'
        )

    # get user menu selection and validate input
    while True:
        try:
            user_input = int(input('Select option & press Enter: \n'))
            if 1 <= user_input <= 8:
                match user_input:
                    case 1:
                        if category == 'Training':
                            print('... LOADING TRAINING QUESTIONS ...')
                            # get n questions
                            run_quiz(get_wrong_questions(num))
                            exit()
                        else:
                            print("... GENERATING NEW QUIZ ...")
                            # generate n questions from API
                            question_list = get_questions(
                                                        num,
                                                        category,
                                                        question_type,
                                                        difficulty,
                                                        tok
                                                        )
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
                    case 7:
                        log_in()
                    case 8:
                        exit()

            else:
                print("Please enter 1 - 8!")
        except ValueError:
            print('Please enter a number!')


def log_in():
    '''
    show log in screen
    option to create new user
    '''
    global user

    reset_cli('Log in...')
    user_list = get_users()
    user_input = input("Enter your username: ")
    if user_input in user_list:
        print (f"Welcome back, {user_input}!\n")
        while True:
            user_pw = getpass.getpass("Enter your password: \n")
            if check_password(user_list, user_input, user_pw) == True:
                user = user_input
                display_main_menu()
                break
            else:
                print("Incorrect Password. Please try again")
    else:
        print ("User does not exist!")
        # get user selection and validate input
        while True:
            try:
                print(f'\n1. Add {user_input} as new user\n'
                      f'2. Abort / Back to Menu\n')
                user_selection = int(input('\nSelect option 1 or 2:\n'))
                if 1 <= user_selection <= 2:
                    match user_selection:
                        case 1:
                            create_user(user_input)
                        case 2:
                            question_type = 'multiple'
                            display_main_menu()
                    break
                else:
                    print("Please enter 1 or 2!")
            except ValueError:
                print('Please enter a number!')
    exit()


def check_password(user_list, username, pw):
    '''
    compares user input pw with saved one from user_list
    '''
    correct_pw = user_list.get(username, None)

    if correct_pw is not None and correct_pw == pw:
        return True
    else:
        return False


def get_users():
    '''
    returns a dictionary of all users and passwords for login
    virification
    '''
    user_list = SHEET.worksheet('users')
    
    keys = user_list.col_values(1)[1:]
    values = user_list.col_values(2)[1:]
    defaults = user_list.col_values(4)[1:]
    # create dictionary of users and passwords
    user_data = dict(zip(keys, values))
    
    return user_data


def create_user(user_name):
    '''
    if user does not exist, add a new one and create a sheet
    '''
    print(f'Creating new user {user_name}')
    
    while True:
        pass1 = getpass.getpass("Enter a password:\n")
        pass2 = getpass.getpass("Repeat password:\n")

        if pass1 == pass2:
            # add user to password list
            SHEET.worksheet('users').append_row([user_name, pass1])
            #create new user sheet to store their wrong questions
            print("Creating new user profile...")
            new_tab = SHEET.add_worksheet(title=user_name, rows="2000", cols="10")
            display_main_menu()
            break
        else:
            print('Passwords do not match. Please try again!')

def no_of_questions():
    '''
    Allow user to change the number of questions per quiz.
    Changes the global variable
    '''
    global num

    reset_cli('Number of Questions:')

    # get user selection and validate input
    while True:
        try:
            user_input = int(input(f'\nType how many questions'
                                   f' you would like (1-50):\n'))
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
    Allow user to change the difficulty level of quiz.
    Changes the global variable
    '''
    global difficulty

    reset_cli('Difficulty Level')

    # get user selection and validate input
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
    Allow user to change the type of quiz.
    (multpile choice, true or false or both (ANY).
    Changes the global variable
    '''
    global question_type

    reset_cli('Question Types')

    # get user selection and validate input
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


def change_category():
    '''
    Allow user to change the category.list pulled from open quiz DB.
    Changes the global variable
    '''
    global category

    reset_cli('Available Categories')
    print(create_category_list(category_list))

    # get user selection and validate input
    while True:
        try:
            user_input = int(input(f'\nPlease type the '
                                   f'number of the category:\n'))
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
    # loop through to find given ID
    for cat in trivia_categories:
        # check for ID match
        if cat.get('id') == id:
            # return cat name
            return cat.get('name')
    # get questions (collection of previous wrong answers)
    if id == "Training":
        return 'Training'
    else:
        return 'ANY'   # if ID not found


def create_category_list(categories):
    '''
    pass API category data and create string to
    display in settings menu for category selection
    '''
    str_categories = (f"7 -- TRAINING Category (Previous wrong questions)\n"
                      f"8 -- ANY category\n")
    trivia_categories = categories.get('trivia_categories', [])
    # loop through entries:
    for cat in trivia_categories:
        # get ID and name
        cat_id = cat.get('id')
        cat_name = cat.get('name')
        # append to string
        str_categories += f'{cat_id} -- {cat_name}\n'

    # return the completed string
    return str_categories


def toggle_training_mode():
    '''
    toggle training more on or off
    used to determine if wrong questions
     should be stored on the google sheet
    '''
    global training_mode
    global user

    if user == "Not Logged In":
        print(f'Sorry, you must be logged into your profile'
              f' to use Training Mode (option 7)')
        time.sleep(3)
        display_main_menu()
        exit()

    if training_mode == 'OFF':
        training_mode = 'ON'
    else:
        training_mode = 'OFF'
    display_main_menu()


def format_question(raw_question_list, n):
    '''
    returns the nth question from the given raw question list
    in a proper format as well as the correct answer number
    Answers are shuffled and category + difficulty added.
    '''
    # get nth question from given list
    q = raw_question_list['results'][n]

    # add question first and add category and difficulty to it
    individual_question = (
        f"{q['question']}\n"
        f"{q['category']} ({q['difficulty']})\n\n"
        )

    # add answers
    if q['type'] == 'boolean':
        correct_answer_number = 1 if q['correct_answer'] == 'True' else 2
        individual_question += f'1. True\n2. False\n'  # only needs std 2 ans
    else:
        answers = [q['correct_answer']] + q['incorrect_answers']
        random.shuffle(answers)  # shuffle so correct answer is not always 1
        # add answers underneath question string
        for i, ans in enumerate(answers, start=1):  # don't use 0 for first ans
            individual_question += f'{i}. {ans}\n'  # number and add all ans
            if ans == q['correct_answer']:
                correct_answer_number = i  # remember correct answer number

    return html.unescape(individual_question), correct_answer_number


def add_question_to_sheet(question_list):
    '''
    recieves list of wrong questions and
    extracts the data into a single key / column match
    then saves the data to the google sheet via API
    also adds the date when the question was added.
    '''
    destination = SHEET.worksheet(user)
    print("Saving wrong questions for training category...")

    # EXTRACT data from wrong question list
    for q in question_list:
        data = [q['type'],
                q['difficulty'],
                q['category'],
                q['question'],
                q['correct_answer']]
        wrong_answers = q['incorrect_answers']
        if q['type'] == 'boolean':  # add 2 blank wrong answers
            wrong_answers.extend(['', ''])
        data.extend(wrong_answers)

        # add date to end of data to track when question was added
        todays_date = date.today()
        str_todays_date = todays_date.strftime('%Y.%m.%d')
        data.append(str_todays_date)
        destination.append_row(data)  # add data to google sheet
    print("Questions saved")


def get_wrong_questions(n):
    '''
    Function retrieves n questions from the saved data
    from the google sheet stored questions.
    If there are not enough questions in the list,
    informs the user and sets n to all available questions
    Returned result is randomized
    Data is then reconfigured into the same format recieved from Trivia API
    this can be passed to normal quiz functions to generate a quiz.
    '''
    global num  # change num if not enouigh wrong questions for quiz

    # build dict in same format as returned from the API
    wrong_questions_dict = {'response_code': 0, 'results': []}
    questions = SHEET.worksheet(user)
    data = questions.get_all_values()
    max_questions = 0

    if len(data) <= 1:
        # no questions saved in google sheet yet
        print(f"Sorry, no questions have been saved yet."
              f"Ensure Training Mode is on to remember wrong questions")
        input("Press enter to continue\n")
        display_main_menu()
        return
    elif n > (len(data) - 1):
        # use number of available questions if n is greater
        print(f'Not enough data to create training quiz with {n} questions.\n'
              f'Max available is {len(data)-1}')
        max_questions = len(data) - 1
        num = len(data)-1
        time.sleep(4)
        display_main_menu()
        return
    else:
        max_questions = n

    # create maximum random indices either n or max of wrong questions
    random_indices = random.sample(range(1, len(data)), max_questions)

    # iterate through sheet data and append to new dictionary
    for index in random_indices:
        item = data[index]  # pick a question based on random index list
        temp_dict = {
            'type': item[0],
            'difficulty': item[1],
            'category': item[2],
            'question': item[3],
            'correct_answer': item[4],
            'incorrect_answers': item[5:8]
        }
        wrong_questions_dict['results'].append(temp_dict)

    print(wrong_questions_dict)
    return wrong_questions_dict


def show_result(score):
    '''
    display end of quiz result and a message based on the percentage
    '''
    reset_cli('End of Quiz!')
    custom_ascii_font = Figlet(font='broadway')  # set font name
    print(custom_ascii_font.renderText('END!'))
    print(f'Your Final Score:  {round(score,1)}%\n')
    match score:
        case _ if score == 100:
            print("You aced it! Awesome!\n")
        case _ if score > 90:
            print("Great effort! You're a trivia master!\n")
        case _ if score > 75:
            print('Not too bad! Keep practicing\n')
        case _ if score > 50:
            print('Good effort. Have you tried Training mode yet?\n')
        case _ if score >= 25:
            print('These topics were not your strongpoint. Try again!\n')
        case _ if score < 25:
            print('Sorry, you need to brush up on this topic!\n')
    return


def run_quiz(raw_question_list):
    '''
    main function that loops through all given questions, displays one by one,
    processes user answer and updates the scores.
    If training mode is on, function will also append
    a list of the incorrect answers and export to google sheet
    '''

    global correct, wrong, training_mode, num
    wrong_qs = []  # remember which questions were wrong

    #     main loop to display each question     ##
    # start loop, display first question as 1, not 0
    for q_count, q_data in enumerate(raw_question_list['results'],
                                     start=1):
        percentage = correct / num * 100
        status = (f'Question {q_count} of {num}.'
                  f' Correct: {correct} / Wrong: {wrong}.'
                  f' ({round(percentage,1)}%)')
        reset_cli(f'{status}')  # reset CLI before showing first question

        # get formatted question
        # returns formatted question, answers, as well as correct answer
        result = format_question(raw_question_list, q_count-1)
        # first tuple result from format function - prints question to CLI
        print(f'{result[0]}\n')
        # second tuple result from format function - store correct answer
        correct_answer = result[1]

        # UNCOMMENT FOR DEBUG / EVALUATION PURPOSES
        # print(f'Debug: CorrectAnswerNo: {correct_answer}')

        # get user answer and validate
        # set how many valid answers there are
        if raw_question_list['results'][q_count-1]['type'] == 'boolean':
            qs = 2
        else:
            qs = 4

        while True:
            grn = '\033[92m'
            rst = '\033[0m'
            try:
                user_answer = int(input(f"Select Answer: (type 1 - {qs})\n"))
                if 1 <= user_answer <= qs:  # valid answer
                    # compare answers and update scores
                    if user_answer == correct_answer:
                        correct += 1
                        print(f'{grn}CORRECT!{rst}')
                        time.sleep(2)
                    else:
                        wrong += 1

                        print(f"{grn}Correct answer: {correct_answer}: "
                              f"{html.unescape(q_data['correct_answer'])}{rst}")
                        time.sleep(2)
                        if training_mode == "ON":
                            wrong_qs.append({'type': q_data['type'],
                                             'difficulty': q_data['difficulty'],
                                             'category': q_data['category'],
                                             'question': q_data['question'],
                                             'correct_answer': q_data['correct_answer'],
                                             'incorrect_answers': q_data['incorrect_answers']})
                    break
                else:
                    print(f"Please enter 1 or {qs}!")
            except ValueError:
                print('Please enter a number!')

            # update status bar
            status = (f'Question {q_count} of {num}.'
                      f' Correct: {correct} / Wrong: {wrong}.'
                      f' ({round(percentage,1)}%)'
                      )
        percentage = correct / num * 100  # final calc after last question
        status = (f'Question {q_count} of {num}.'
                  f' Correct: {correct} / Wrong: {wrong}.'
                  f' ({round(percentage,1)}%)')
        reset_cli(f'{status}')  # update cli after last question
        show_result(percentage)
    # ###########################    end of loop

    # export wrong questions to google sheet
    # do not save wrong qeustions from previous wrong q's
    if training_mode == "ON" and category != "Training":
        add_question_to_sheet(wrong_qs)

    print('Would you like to play again?\n')

    # ask user if they want to play again
    while True:
        try:
            user_input = int(input('1. YES\n2. NO\n'))
            if 1 <= user_input <= 2:
                match user_input:
                    case 1:
                        correct = 0  # reset scores before starting again
                        wrong = 0
                        display_main_menu()
                    case 2:
                        status = 'Thanks for Playing'
                        reset_cli(f'{status}')  # update cli
                        custom_ascii_font = Figlet(font='small')
                        print(custom_ascii_font.renderText('Have a nice day!'))
                        exit()
                break
            else:
                print("Please enter 1 or 2!\n")
        except ValueError:
            print('Please enter a number!\n')

# ##########################################################################
# ## global variables/defaults to keep track of selected quiz parameters ###
# ##########################################################################


user = "Not Logged In"
category_list = get_categories()
category = 9  # number of category or ANY, dafault is 9, General Knowledge
question_type = 'ANY'  # multiple, boolean, ANY
difficulty = 'ANY'  # easy, medium, hard, ANY
num = 10  # default number of questions. Do not set to 0!
training_mode = "OFF"
tok = generate_new_token()
correct = 0
wrong = 0

# launch quiz CLI app
display_main_menu()

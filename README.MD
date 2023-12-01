# MEGA-QUIZ 
a CLI Interface to <a href="https://opentdb.com/">OpenTriviaDatabase</a>

Find it on GitHub: <a href="https://github.com/A-Hoenig/megaquiz">MEGA-QUIZ</a>

<img src="./assets/screenshot0.png" alt="MEGA-QUIZ" width="400"/>

## CONTENTS

<!-- TABLE OF CONTENTS -->

  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#user-experience">User Experience</a></li>
    <li><a href="#design">Design</a></li>
    <li><a href="#technologies-used">Technologies</a></li>
    <li><a href="#repository">Deployment</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#image-credits">Image Credits</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>

### Built With
* [https://www.gitpod.io/](GitPod)

![GitHub last commit](https://img.shields.io/github/last-commit/A-Hoenig/WordDash?color=red&style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/A-Hoenig/WordDash?color=orange&style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/A-Hoenig/WordDash?color=yellow&style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/A-Hoenig/WordDash?color=green&style=for-the-badge)


<!-- ABOUT THE PROJECT -->
## About The Project

The OpenTriviaDatabase is an online database of thousands of trivia questions which can be accessed via an API.
The website itself has no option to display a quiz and is only setup to allow users to create accounts and contribute questions to the database. User suggested questions are added once they are verified.  

MEGA-QUIZ gives the user the ability to customize the parameters for a quiz and generate a trivia quiz of random questions from the site.

Additionally, Mega-Quiz offers a training option. In this case, the user can log in and create a user profile.  
As long as training mode is activated, any questions the user gets wrong are stored in a private google sheet.
This self generated database of 'wrong questions' can then be selected as a category so that previously wrong questions can be specifically trained in order to increase ones knowlege on desired topics.

## User stories
  
template:  
As a **'role'**, I can **'capability'**, so that **'receive benefit'**

the role will always be **"user/player..."**

"As a user, I can... 

* ...view the menu and select an option to quickly change parameters and start a game"
* ...log in to a user profile so my wrong answers can be stored"
* ...create a user profile if I am new and setup a password"
* ...change the number of questions per quiz so I can decide how long the quiz will be"
* ...change the difficulty level so I can challenge myself or not"
* ...change the type of questions so I can focus on only true or false if I want"
* ...change the category so I can focus on a specific quiz topic"
* ...turn on Training Mode so I can store wrong questions"
* ...select training category so I can revisit wrong questions and improve my knowledge"
* ...exit the menu so I can finish the quiz when I am done"
* ...start a quiz so I can display questions based on my quiz parameters"
* ...enter an answer so I can guess the correct answer to the question"
* ...receive feedback if my answer was right or wrong"
* ...see the correct answer if I got it wrong"
* ...get a final summary of my quiz performance including a percentage"
* ...decide if I want to play again or leave the app"

## Underlying Functionality

### User alterable parameters:
<ol>
  <li>Number of questions (API allows 1-50)</li>
  <li>Type of Questions (True / False or Multiple Choice)</li>
  <li>Difficulty Level (Easy / Medium / Hard)</li>
  <li>Category (list below)</li>
</ol>

These parameters can be passed to the API which will then return an object containing random questions.
If the parameters are not provided (except number of questions), the site will return a random selection of ANY of the options

ie -- if no category is provided, questions will be sourced from ALL categories or only the one that is selected. The API does not allow selection of multiple different categories.

### Available categories:

* 7 -- TRAINING Category (Previous wrong questions)
* 8 -- ANY category
* 9 -- General Knowledge
* 10 -- Entertainment: Books
* 11 -- Entertainment: Film
* 12 -- Entertainment: Music
* 13 -- Entertainment: Musicals & Theatres
* 14 -- Entertainment: Television
* 15 -- Entertainment: Video Games
* 16 -- Entertainment: Board Games
* 17 -- Science & Nature
* 18 -- Science: Computers
* 19 -- Science: Mathematics
* 20 -- Mythology
* 21 -- Sports
* 22 -- Geography
* 23 -- History
* 24 -- Politics
* 25 -- Art
* 26 -- Celebrities
* 27 -- Animals
* 28 -- Vehicles
* 29 -- Entertainment: Comics
* 30 -- Science: Gadgets
* 31 -- Entertainment: Japanese Anime & Manga
* 32 -- Entertainment: Cartoon & Animations

The numbering of the categories is defined by the API which startes at 9-32. These integers must be passed to the site to specifiy the desired category. Adding 7 and 8 were a logical continuation of this fact: these are added by the program to allow the user to select ANY category (ie no category will be passed to the API) or TRAINING. Therefore category 7 and 8 are NOT passed to the API.

When training category is selected, the source of questions becomes the linked google sheet that is accessed via the google gspread and google sheets APIs. Using this mode requires that a user has previously generated a profile, and wrong questions were already stored in Training mode.

The specific API documantation can be referenced <a href="https://opentdb.com/api_config.php">HERE</a>

<p align="right">(<a href="#contents">back to top</a>)</p>

### Datamodel

The site returns a json string which is then converted into a dictionary of the entire quiz (using json library). It contains all questions, including their type, difficulty and category, the correct answer as well as a list of incorrect answers. The raw structure is as follows:

```
{  
  "response_code": 0,  
  "results": [  
              {  
                "type": "multiple",  
                "difficulty": "easy",  
                "category": "General Knowledge",  
                "question": "What is Tasmania?",  
                "correct_answer": "An Australian State",  
                "incorrect_answers": [  
                  "A flavor of Ben and Jerry&#039;s ice-cream",  
                  "A Psychological Disorder",  
                  "The Name of a Warner Brothers Cartoon Character"  
                                      ]  
              },  
              {  
                "type": "boolean",  
                "difficulty": "easy",  
                "category": "General Knowledge",  
                "question": "A pasodoble is a type of Italian pasta sauce.",  
                "correct_answer": "False",  
                "incorrect_answers": [  
                  "True"  
                                    ]  
              },  
              {  
                "type": "multiple",  
                "difficulty": "easy",  
                "category": "General Knowledge",  
                "question": "Who invented the first ever chocolate bar, in 1847?",  
                "correct_answer": "Joseph Fry",  
                "incorrect_answers": [  
                  "Andrew Johnson",  
                  "John Cadbury",  
                  "John Tyler"  
                                    ]  
              }  
]  
}  
```
The resulting dictionary contains 2 keys: response_code and results.  
The results value is a list of n dictionaries (based on how many questions are requested)  
Each question dictionary contains the parameters, the question, the correct answer, and an additional list of incorrect answers. Multiple Choice questions therefore have 3 incorrect answers, whereas boolean questions only have one.

This structure must be iterated correctly to extract and build legible questions for the user.

Finally, to handle special characters, all text from the site can be encoded by different means. The default is HTML encoding. (&#)  
An exmple can be seen in the first wrong answer of the first question.

Extracted text therefore needs to interpret special characters using the html.unescape() method from the html library.

<p align="right">(<a href="#contents">back to top</a>)</p>

## Command Line Interface

Since this is part of a course user project, the directive was to design a user font end using python only in a commandline environment. A full HTML/CSS/JS based front end is recommended eventually to drastically improve the user UX/UI experience.

Design choices were made to ensure ease of use inside an 80x44 character CLI window using a keyboard only input device. This drove all choices in how the interface would be structured. The CI CLI index.html template deployed to Heroku was modified from 24 to 44 rows of text to allow more screen realestate for displaying quiz graphics and menu items.

## Main application logic (Flowchart)
Below is the main logic decided upon for the flow of the game interaction.

<img src="./assets/flowchart-main.jpg" alt="MEGA-QUIZ" width="600"/>

The main structure is a single function that pauses for a user input. All options are captured and then call additional functions to display submenus, change parameters or start the quiz.

The main quiz function is a single loop that iterates through the question dictionary and builds each question to display it. The correct answer is compared with the user input and then repeated until all questions have been presented.

For simplicity and ease of use, all inputs are digits from 1-8 (with the exeption of when the user can input the number of questions: 1-50)  
This means once started, the user can keep his or her hand on the numberpad or numbers 1-4 and easily interact with the quiz without needing to navigate the keyboard.

All inputs are verified to allow only the applicable numbers to be input.

If the number is out of range, the input is repeated and feedback is given.

<p align="right">(<a href="#contents">back to top</a>)</p>


## Design

#### The Main Menu

<img src="./assets/screenshot1.jpg" alt="main menu" width="600"/>

#### Adjusting number of questions

<img src="./assets/screenshot2.jpg" alt="no of qs" width="600"/>

<p align="right">(<a href="#contents">back to top</a>)</p>

#### Setting the difficulty level

<img src="./assets/screenshot3.jpg" alt="difficulty" width="600"/>

#### Selecting the question type

<img src="./assets/screenshot4.jpg" alt="type" width="600"/>

<p align="right">(<a href="#contents">back to top</a>)</p>

#### Selecting the category

<img src="./assets/screenshot5.jpg" alt="category" width="600"/>

#### Training Mode

<img src="./assets/screenshot6.jpg" alt="training mode" width="600"/>

<p align="right">(<a href="#contents">back to top</a>)</p>

#### User Login

<img src="./assets/screenshot7.jpg" alt="login" width="600"/>

#### Main Menu User Logged In

<img src="./assets/screenshot8.jpg" alt="logged in" width="600"/>

<p align="right">(<a href="#contents">back to top</a>)</p>

#### User Does not exist / Create new user

<img src="./assets/screenshot9.jpg" alt="new user" width="600"/>

#### Standard question format display

<img src="./assets/screenshot10.jpg" alt="question" width="600"/>

<p align="right">(<a href="#contents">back to top</a>)</p>

#### Question CORRECT ANSWER

<img src="./assets/screenshot11.jpg" alt="correct" width="600"/>

#### Question INCORRECT ANSWER

<img src="./assets/screenshot12.jpg" alt="wrong" width="600"/>

<p align="right">(<a href="#contents">back to top</a>)</p>

#### Quiz completed feedback

<img src="./assets/screenshot13.jpg" alt="end of quiz" width="600"/>

#### User quit goodbye

<img src="./assets/screenshot14.jpg" alt="goodbye" width="600"/>

<p align="right">(<a href="#contents">back to top</a>)</p>


### Future Development

* Since the API will only return a singe category or ALL categories, use the front end to allow the user to select multiple categories. Then manually pull a set of the requested topics from the database. eg user wants 20 questions and selected 3 categories, app would then request (20 / 3) + 1 questions from each topic and then build a random quiz using those quesitions.
* use the date of when questions were added to prioritize older questions rather than recently added ones (user option selectable)
* allow user to set a threshold when to remove training questions from the stored list - eg if the user has answered a specific question correctly x times, it can be removed
* improve the funciton that gets the google sheets questions to only collect questions of the specificed type, category and difficulty
* store the user settings in their profile so that the app defaults can be remembered
* add user feedback of how many wrong questions are stored and what categories
* store a high score for each category in the user profile and track some basic useage statisics - number of questions, overall percentage etc
* add a user change password option
* add password encryption to keep everything secure
* instead of googe sheets, store user data in an actual back end database
* integrate app into a well designed graphical front end that allows keyboard and mouse user input with engaging graphics

## Technologies Used

#### Languages:

PYTHON FOR MAIN APP. HTML, CSS for mock CLI in HEROKU.

* [EDrawMax](https://www.edrawsoft.com/ad/edrawmax-diagram-tool.html?gad_source=1&gclid=CjwKCAiAjfyqBhAsEiwA-UdzJP7WWEuJcqaBE2Vag1b0U3ukJ_MwizjN76YlORg6EU2jBAXaFfTgxxoC2vAQAvD_BwE) - Used to create flowcharts.

* [Git](https://git-scm.com/) - For version control.

* [Github](https://github.com/) - To save and store the files for the website.

* [GitPod](https://gitpod.io/) - IDE used to create the site.

* [Heroku](https://www.heroku.com) - Hosts a mock CLI to run python app

#### Python Libraries:
| Library        | Needed For |
| :-------------- | :------ |
|gspread|google sheet manipulation|
|from google.oauth2.service_account import Credentials|authenticate google sheets|
|html|decode special characters from trivia site|
|requests|used for trivia API query|
|json|used to parse the recieved dictionary|
|os|needed to be able to clear CLI|
|random|needed to randomize questions answers|
|time|used to pause app long enough for user to read feedback|
|getpass|allow password entry without showing input text|
|from pyfiglet import Figlet|ASCII font art generator|
|from datetime import date|format date string for google sheet data|

<p align="right">(<a href="#contents">back to top</a>)</p>

<!-- GETTING STARTED -->
## Running the app

for a quick run without google sheets integration:

1. fork or clone the repository and enter your IDE
2. In the terminal / command line type **python3 run.py** to run the app on your IDE

The finished app is hosted with HEROKU here:
<br>
<a href="https://mega-quiz-c93f32d70f60.herokuapp.com/">MEGA-QUIZ</a>
<br/>

For full app functionality, a google sheet needs to be set up with API credentials as well.
A step by step guide on how to do this can be referenced [Here (README_googleAPI)](README_googleAPI.md)

## Repository

###  **Deploying to Heroku**

1. Go to [Heroku](https://id.heroku.com/login), create account if you don't have and log in.

2. Head to your dashboard and click "New", then "Create new app"

    <details>
    <summary>New / Create New App</summary>
              
    ![New/CreateNewApp](/assets/images/deployment/step1-create-new-app.png)  

    </details>

3. Next step is to give your app a name and to choose region. After that click on "Create app".

    <details>
    <summary>Name / Region / Create</summary>
              
    ![Name/Region/Create](/assets/images/deployment/step2.png)  

    </details>

4. After that head to "Settings" tab which you can find on top of your Heroku page and under the "Config Vars" set your Key/Value Pairs.

    <details>
    <summary>CREDS / PORT</summary>
              
    ![CREDS/PORT](/assets/images/deployment/step3.png)  

    </details>

    First Key = **CREDS**. Value: Paste content of **creds.json** file  
    Second Key = **PORT**. Value: **8000**

5. Then in the "Buildpacks" section you will need to add buildpacks. Pay attention to the order in which you add buildpacks you need. In my case I had to add Python first and nodejs second.

    <details>
    <summary>Buildpacks</summary>
              
    ![Buildpacks](/assets/images/deployment/step4.png)  

    </details>

6. First add "Python", by clicking on Python icon and then click on "Add Buildpack".

    <details>
    <summary>Python</summary>
              
    ![Python](/assets/images/deployment/step5-python.png)  

    </details>

7. Then add "nodejs", by clicking on nodejs icon and then click on "Add Buildpack".

    <details>
    <summary>nodejs</summary>
              
    ![nodejs](/assets/images/deployment/step6-nodejs.png)  

    </details>

8. Then head to "Deployment" tab which you can also find on top of your Heroku page and under "Deployment method" click on "GitHub"(in my case that's where my repository is).

    <details>
    <summary>GitHub</summary>
              
    ![GitHub](/assets/images/deployment/step7-github.png)  

    </details>

9. After that, just under the "Deployment method" section is "Connect to GitHub" section where you need to find your repository and then click on "Connect".

    <details>
    <summary>Connect</summary>
              
    ![Connect](/assets/images/deployment/step8.png)  

    </details>

10. Just under "Connect to GitHub" section is "Automatic deploys" section where you can click on "Enable Automatic Deploys" if that's what you want and just under is "Manual Deploy" section, where you need to click on "Deploy Manually".

    <details>
    <summary>Enable Automatic Deploys / Deploy Manually</summary>
              
    ![EnableAutomaticDeploys/DeployManually](/assets/images/deployment/step9-deployment-type.png)  

    </details>

### Local Development

#### How to Fork

To fork the repository:

1. Log in (or sign up) to Github.
2. Go to the repository for this project, [A-Hoenig/megaquiz](https://github.com/A-Hoenig/megaquiz)
3. Click the Fork button in the top right corner.
4. Drag and drop the CREDS.json file into the root directory
5. Make sure to add CREDS.json to the .gitignore file to prevent the secure key being commited to github
6. To run the quiz type: **python3 run.py** in the command line / terminal

#### How to Clone

To clone the repository:

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [A-Hoenig/megaquiz](https://github.com/A-Hoenig/megaquiz)
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.
6. Ensure the CREDS.json file is uploaded and ignored as mentioned above.

<p align="right">(<a href="#contents">back to top</a>)</p>

## Testing

### Validator Testing

#### PYTHON
  - No errors were returned when passing through the official [CI pep8 Linter](https://pep8ci.herokuapp.com/)


## Manual Testing

### 1. GENERAL TESTS / LOGIC
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|App starts after run.py|Enter command in CLI|Verified OK|
|App starts in Heroku CLI|Click run app on page|Verified OK|
|App accepts keyboard input|Type keyboard input|**Verfied except Safari in Heroku**|
|Input validation blank input|Type Enter w/ no num |Verified OK|
|Input validation no number|Type letter & special characters|Verified OK|
|Input validation wrong number|Typed 0 and 9+|Verified OK|
|New user creates new sheet in google|Created new user|Verified OK|
|New sheet is correctly named|open google sheet after new user added|Verified OK|
|Google users sheet is updated with new user + pw|check google sheet|Verified OK|
|User can exit gracefully|press 8 in menu or 2 after quiz|Verified OK|
|Exit shows goodbye message|exited app from quiz and menu|Verified OK|

### 2. MENU TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|Main Menu displays correct in CLI|start app|Verified OK|
|Input Number launches correct action|checked all options|Verified OK|
|Input 1 starts the quiz|selected 1|Verified OK|
|Input 2 shows change question number screen|Selected 2|Verified OK|
|Input 3 shows change difficulty|Selected 3|Verified OK|
|Input 4 shows change type|Selected 4|Verified OK|
|Input 5 shows change category|Selected 5|Verified OK|
|Input 6 toggles training mode|Selected 6 when logged in|Verified OK|
|Input 6 flags error if not logged in|Selected 6 not logge in|Verified OK|
|Input 7 shows log in screen|Selected 7|Verified OK|
|Input 7 shows user name if logged in|logged in|Verified OK|
|Input 8 end app and returns to CLI|Selected 8|Verified OK|
|Change question accepts only 1-50|Typed letter and 0 or 51+|Verified OK|
|No of questions is updated in main menu|Updated number|Verified OK|
|Change difficulty menu displayed correctly|Selected 6|Verified OK|
|New Difficulty displayed in Main menu|Changed Difficulty|Verified OK|
|Change type menu displays correctly|Selected 4|Verified OK|
|New Type displayed in Menu|Changed Type|Verified OK|
|Type correctly displays True/False, not boolean|Change to T/F|Verified OK|
|Change category menu displays correctly|Selected 5|Verified OK|
|Categories recieved from API|Selected 5|List displays correctly|
|New category displays name in Menu (not number)|Changed Category|Verified OK|
|Training mode only toggles if logged in|Selected 7 logged out|Verified OK|
|Training mode displays correctly in main menu|Selected 7 logged in|Verified OK|
|User login displayed correctly|Selected 7|Verified OK|
|Once logged in, user name displays in main menu|logged in|Verified OK|

### 3. LOGIN / USER ACCOUNT TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|User can log in|input dummy user and pw|Verified OK|
|Password entry is checked|typed correct and wrong pw|Verified OK|
|Wrong password x3 = back to menu|type 3 wrong pw|Verified OK|
|User recognized|logged in correectly|Verified OK|
|Username validation rejects special characters|input @$_ etc|Verified OK|
|Unreconized User triggers 'create new'|typed a new username|Verified OK|
|New user can enter password|new user name + password input|Verified OK|
|New password is checked matching|typed wrong and correct repeat pw|Verified OK|
|Feedback given to user|typed all options|Verified OK|

### 4. API TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|Connect to Trivia API|start quiz|Verified OK|
|Trivia token recognized for unique session|start quiz|Verified OK|
|Connect to Google Drive|start quiz in training mode|Verified OK|
|Connect to Google Sheets|add new user|Verified OK|
|Trivia API returns correct object|start quiz|Verified OK|
|Error returns user back to main menu|input more qs than on sheet|Verified OK|
|Training questions correctly received from google sheet|start training quiz|Verified OK|
|After quiz, wrong questions added to user sheet|deliberately answer wrong|Verified OK|

### 5. QUIZ MECHANICS TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|Quiz Starts as expected|Input 1|Verified OK|
|Number of question displayed correctly|start quiz check for 1|Verified OK|
|Total number of questions displayed|start quizzes with different n|Verified OK|
|Right and Wrong counters start at 0|start quiz|Verified OK|
|Question is displayed correctly|play many quizzes and check|Verified OK|
|Correct question category displayed|start quiz compare category|Verified OK|
|Correct question difficulty displayed|start quiz compare difficulty|Verified OK|
|Possible answers are displayed correctly|start quiz|Verified OK|
|All text is decoded when HTML codes present|play many quizzes to check examples|Verified OK|
|Correct answer is at random position|play many quizzes|Verified OK|
|True False question changes input promt|checked on boolean questions|Verified OK|
|Input only allows 1-4 or 1-2|input deliberate wrong digits|Verified OK|
|Correct answer is recognized|input correct answer|Verified OK|
|Correct answer updates correct counter|input correct answer|Verified OK|
|Correct answer user feedback is shown in green|input correct answer|Verified OK|
|Wrong answer is flagged|input wrong answer|Verified OK|
|Wrong answer updates wrong counter|input wrong answer|Verified OK|
|Wrong answer shows correct answer in green|input wrong answer|Verified OK|
|Percentage calculates correctly|input right and wrong answers|Verified OK|
|Quiz ends after the expected number of questions|played different num quizzes to end|Verified OK|
|Quiz feedback is shown at the end with total score|played quizzes to end|Verified OK|
|Feedback is different based on percentage|adjusted how many wrong answers given|Verified OK|
|User can end app or return to play again|press 1 and 2|Verified OK|
|User is shown feedback that wrong questions are being saved|answered wrong in training mode|Verified OK|

### 5. TRAINING MODE TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|Questions retrieved from google sheet correctly|start training quiz|Verified OK|
|Questions converted into correct data object|start many training quizzes|Verified OK|
|Training mode checks available questions|start training cat with more/less questions than avail|Verified OK|
|Training mode returns error if requested number > available|input more qs than on sheet|Verified OK|
|Number of questions reset to max available|input more qs than on sheet|Verified OK|
|Quiz correctly displays previous wrong questions|compare google sheet with quiz|Verified OK|
|Wrong questions from 'wrong' list arent added to sheet again (no doubles)|anser training quiz q wrong compare sheet|Verified OK|
|Questions render correctly with decoded HTML escape tags|repeat quizzes and check|Verified OK|
|Wrong questions are saved to correct user sheet|answer wonrg questions and check user sheet|Verified OK|
|Correct date recorded with each wrong question|not tested yet|**TBD**|
|User gets feedback if no questions saved yet|select cat 7 before wrong qs added|Verified OK|

### Browser Compatibility

The deployed app on heroku was tested on the three most popular browsers for functionality:
* Chrome
* Safari - CI CLI app doens not accept keyboard input on macOS/iOS Safari and iOS Chrome!
* Edge

### Known / Fixed Bugs

No bugs found impacting playability or styling.

## Credits

### External Help

* Google / Stackoverflow
* TheQuizArms Pub Quiz project README was recommended as a baseline for this README. Many thanks. <a href="https://github.com/kera-cudmore/TheQuizArms/blob/main/README.md">The Quiz Arms README.md</a>
* Thanks to https://github.com/AleksandarJavorovic for sharing the instructions on how best to deploy the app on Heroku.

## License

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png) 
<br>
This project is license free and part of Code Institute Full Stack Developer Course.
It is for educational use only.

<!-- CONTACT -->
## Contact

Alex Hönig -  LimeyDeveloper@pm.me

Project Link: [https://github.com/A-Hoenig/Project-One/tree/main](https://github.com/A-Hoenig/Project-One/tree/main)

## Acknowledgments

I would like to acknowledge the following people:

* Jubril Akolade - My Code Institute Mentor for the guidance.


<p align="right">(<a href="#contents">back to top</a>)</p>
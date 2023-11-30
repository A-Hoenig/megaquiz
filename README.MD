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
    <li><a href="#accessibility">Accessibility</a></li>
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
The website itself has no front end and is only setup to allow users to create accounts and contribute questions to the database once they are verified.

MEGA-QUIZ gives the user the ability to customize the parameters for a quiz and generate a trivia quiz of random questions from the site.

Additionally, Mega-Quiz offers a training option. In this case, the user can log in and create a user profile.
Once training mode is selected, any questions the user gets wrong are stored in a private google sheet.
This self generated database of 'wrong questions' can then also be selected as a category so that previously wrong questions can be repeatedly trained in order to increase ones knowlege on desired topics.

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

### The available categories:

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

The numbering of the categories is defined by the API which startes at 9-32. These integers must be passed to the site to specifiy the desired category. Adding 7 and 8 were a logical continuation of this fact: thsese are added by the program to allow the user to select ANY category (ie no category will be passed to the API) or TRAINING.

In this case the source of questions becomes the linked google sheet, that is accessed via a different API. Using this mode requires that previously, a user has generated a profile and stored wrong questions in Training mode.

The specific API documantation can be referenced <a href="https://opentdb.com/api_config.php">HERE</a>

<p align="right">(<a href="#contents">back to top</a>)</p>

### Datamodel

The site returns a dictionary of the entire quiz. It contains all questions, including their type, difficulty and category, the correct answer as well as a list of incorrect answers. The raw structure is as follows:

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
The API returns a dictionary of 2 keys: response_code and results.  
The results value is a list of n dictionaries (based on how many questions are requested)  
Each question dictionary contains the parameters, the question, the correct answer, and an additional list of incorrect answers. Multiple Choice questions therefore have 3 incorrect answers, whereas True/False questions only have one.

This structure must be iterated correctly to extract and build legible questions for the user.

Finally, to handle special characters, all text form the site can be encoded by different means. The default is HTML encoding. (&#)  
An exmple can be seen in the first wrong answer of the first question.

Extracted text therefore needs to interpret special characters using the html.unescape() method from the html library.

## Command Line Interface

Since this is part of a course user project, the directive was to design a user font end using python only in a commandline environment. A full HTML based front end is recommended eventually to drastically improve the user interaction.

Design choices were made to ensure ease of use inside an 80x44 character CLI window using a keyboard only input device. This drove all choices in how the interface would be structured.

## Main application logic (Flowchart)
Below is the main logic decided upon for the flow of the game interaction.

<img src="./assets/flowchart-main.jpg" alt="MEGA-QUIZ" width="600"/>

<!-- GETTING STARTED -->
## Accessing the Site

The finished site is hosted with gitpages under:

<br>
<a href="https://a-hoenig.github.io/worddash/">WordDash Word Guessing Game</a>
<br/>

## User Experience



## Design



### FLOW CHART

<img src="./assets/flowchart.jpg" alt="quiz flow chart" width="400"/>

#### The Main Menu



#### The Game Settings



#### Quiz Questions



#### Quiz Feedback



#### Training Mode

#### Future Development



## Technologies Used

#### Languages:

PYTHON FOR MAIN APP. HTML, CSS for mock CLI in HEROKU.

* [EDrawMAax](https://www.edrawsoft.com/ad/edrawmax-diagram-tool.html?gad_source=1&gclid=CjwKCAiAjfyqBhAsEiwA-UdzJP7WWEuJcqaBE2Vag1b0U3ukJ_MwizjN76YlORg6EU2jBAXaFfTgxxoC2vAQAvD_BwE) - Used to create flowcharts.

* [Git](https://git-scm.com/) - For version control.

* [Github](https://github.com/) - To save and store the files for the website.

* [GitPod](https://gitpod.io/) - IDE used to create the site.

* [GithubPages](https://pages.github.com/) - Hosts the deployed website.

<p align="right">(<a href="#contents">back to top</a>)</p>

## Repository

### Deployment

The site is deployed using GitHub pages - [WordDash](https://a-hoenig.github.io/WordDash/).

To deploy the site using GitHub pages:

1. Login (or signup) to Github.
2. Go to the repository for this project, [A-Hoenig/WordDash](https://github.com/A-Hoenig/WordDash).
3. Click the settings button.
4. Select pages in the left hand navigation menu.
5. From the source dropdown select main branch and press save.
6. The site has now been deployed, please note that this process may take a few minutes before the site goes live.

### Local Development

#### How to Fork

To fork the repository:

1. Log in (or sign up) to Github.
2. Go to the repository for this project, [A-Hoenig/WordDash](https://github.com/A-Hoenig/WordDash)
3. Click the Fork button in the top right corner.

#### How to Clone

To clone the repository:

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [A-Hoenig/WordDash](https://github.com/A-Hoenig/WordDash)
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.

<p align="right">(<a href="#contents">back to top</a>)</p>

## Testing

### Validator Testing

#### PYTHON
  - No errors were returned when passing through the official [W3C validator](https://validator.w3.org/)
mance.png" alt="lighthouse-results" width="400"/>

## Manual Testing

### HOME PAGE

### GAMEPLAY TESTING

| Feature        | Expect | Action | Result |
| :-------------- | :------ | :------ | :------ |
|||||

### Browser Compatibility

The site was tested on the three most popular browsers for functionality:

<img src="./assets/docs/popular-browsers.png" alt="popular browsers" width="400"/>

<pre>|       SAFARI MacOS      |         SAFARI iOS      |        CHROME         |          EDGE           |</pre>

### Known / Fixed Bugs

No bugs found impacting playability or styling.

## Credits

### Code Used

* TheQuizArms Pub Quiz project README was recommended as a baseline for this README. Many thanks. <a href="https://github.com/kera-cudmore/TheQuizArms/blob/main/README.md">The Quiz Arms README.md</a>


<!-- IMAGE-CREDITS -->
## Image Credits

Quiz Menu graphic was created using <a href="https://patorjk.com/software/taag/#p=testall&f=Big&t=MEGA%20QUIZ">TEXT TO ASCII ART GENERATOR</a> 
<br>

## Open Trivia Quiz Database
The comprehensive list of 5 letter words was sourced at:
nt to the list is recommended to remove obscure or obsolete words aswell.

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
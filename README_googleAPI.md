# Accessing Google Sheets via API

To create your own google sheet database and be able to access it via API
Creating your own google sheet to act as a database for users wrong questions follow these steps:

## STEPS

### 1. Create a google account (use a dummy one if you plan to actually share the app)
* make sure you are log into the account you will use

### 2. Go to https://docs.google.com/spreadsheets/u/0/?ec=asw-sheets-hero-goto
* Click blank spreadsheet to create an new sheet
* for MegaQuiz to work without modifying source code, name the sheet : **'training_questions'**
* at the bottom tab, rename Sheet1 to **'users'**
* all other required sheets and entries are handled by the app
* keep the sheet open - you'll come back to it when its time to share it

### 3. Setup API access:
* Goto: https://console.cloud.google.com/
* Click on API and services
* Then select Library on the left
* In the search field type : **google drive API** to search for it
* Select the google drive API service
* Click ENABLE
* Click CREATE CREDENTIALS

#### Credential type  

* Dropdown: Select **Google Drive API**
* What data will you access: click **Application Data**
* Click **NEXT**

#### Service Account Details

* Service account name: **Pick a name**
* Service account ID will be generated
* Click **CREATE AND CONTINUE**

#### Grant service account access to the project
* Dropdown: click and in search field type: **'editor'**
* Select **EDITOR**
* Click CONTINUE

#### Grant users access to this service
* No steps required here

#### Click **DONE**

### 4. Next screen: Click **Credentials** on the left menu

* Scroll down and click on service accounts generated email
* **do not click the check box, click the actual link**
* Click the KEYS tab at the top
* Select **ADD KEY**
* Click **Create New Key**
* Keytype JSON
* Click **CREATE**
* File will be created and downloaded to your computer.
* Navigate to file and rename it: **'CREDS.json'**
* **make sure you have the same capitalization**

### 5. Go back to API Library & Install Google Sheets
* Click on burger menu top left and select API and Services --> Library
* In search window type **'google sheets'**
* Click on **Google Sheets API**
* Click on **ENABLE**

### 6. Copy Service account Email Address
* Click on **Credentials**
* Right click Service account email you created and copy

### 7. Share Google sheet with Service Account
* Go back to the new google sheet
* Click **SHARE** on the top right
* Paste the email address and uncheck Notify people
* Click **SEND**

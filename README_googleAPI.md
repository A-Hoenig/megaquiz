# Accessing Google Sheets via API

### Create your own google sheet database and access it via API.  
To create your own google sheet to act as a database for users' wrong questions follow these steps:

# STEPS

## 1. Create a google account (use a dummy one if you plan to actually share the app)
* make sure you are logged into the account you will use

## 2. Go to https://docs.google.com/spreadsheets/u/0/?ec=asw-sheets-hero-goto
* Click blank spreadsheet to create a new sheet
<details>

![GitHub](/assets/images/googleapi/google-sheet-1.jpg)
</details>

* For MegaQuiz to work without modifying source code, name the sheet : **'training_questions'**
<details>

![GitHub](/assets/images/googleapi/google-sheet-2.jpg)
![GitHub](/assets/images/googleapi/google-sheet-3.jpg)
</details>

* At the bottom tab, rename Sheet1 to **'users'**
* All other required sheets and entries are handled by the app
* Keep the sheet open - you'll come back to it when its time to share it

## 3. Setup API access:
* Goto: https://console.cloud.google.com/
* Click the dropdown next to **Google Cloud**
<details>

![GitHub](/assets/images/googleapi/google-api-2.jpg)  

**OR**  

![GitHub](/assets/images/googleapi/google-api-1a.png)  

</details>

* Click **Create New Project**
* Give Project a name
* If notification bell pop up shows:
* Click **SELECT PROJECT**
<details>

![GitHub](/assets/images/googleapi/google-api-5.jpg)
</details>


* Click on API and services
* Then select Library on the left
<details>

![GitHub](/assets/images/googleapi/google-api-6.jpg)
</details>

* In the search field type : **google drive API** to search for it
<details>

![GitHub](/assets/images/googleapi/google-api-7.jpg)
</details>

* Select the google drive API service
<details>

![GitHub](/assets/images/googleapi/google-api-8.jpg)
</details>

* Click ENABLE
<details>

![GitHub](/assets/images/googleapi/google-api-9.jpg)
</details>

* Click CREATE CREDENTIALS
<details>

![GitHub](/assets/images/googleapi/google-api-10.jpg)
</details>

### Credential type  

* Dropdown: Select **Google Drive API**
* What data will you be accessing: click **Application Data**
* Click **NEXT**
<details>

![GitHub](/assets/images/googleapi/google-api-12.jpg)
</details>

### Service Account Details

* Service account name: **Pick a name**
* Service account ID will be generated
* Click **CREATE AND CONTINUE**
<details>

![GitHub](/assets/images/googleapi/google-api-13.jpg)
</details>

### Grant service account access to the project
* Dropdown: click and in search field type: **'editor'**
* Select **EDITOR**
* Click CONTINUE
<details>

![GitHub](/assets/images/googleapi/google-api-14.jpg)  
<hr>

![GitHub](/assets/images/googleapi/google-api-15.jpg)  
<hr>

![GitHub](/assets/images/googleapi/google-api-16.jpg)  

</details>

### Grant users access to this service
* No steps required here
<details>

![GitHub](/assets/images/googleapi/google-api-17.jpg)
</details>

### Click **DONE**

## 4. Next screen: Click **Credentials** on the left menu
* Click **CREATE CREDENTIALS BUTTON ON RIGHT**
<details>

![GitHub](/assets/images/googleapi/google-api-18.jpg)
</details>

* Scroll down and click on service accounts generated email
* **do not click the check box, click the actual link**
<details>

![GitHub](/assets/images/googleapi/google-api-19.jpg)
</details>

* Click the KEYS tab at the top
<details>

![GitHub](/assets/images/googleapi/google-api-20.jpg)
</details>

* Select **ADD KEY DROPDOWN**
<details>

![GitHub](/assets/images/googleapi/google-api-21.jpg)
</details>

* Click **Create New Key**
* Keytype JSON
* Click **CREATE**
<details>

![GitHub](/assets/images/googleapi/google-api-22.jpg)  
<hr>

![GitHub](/assets/images/googleapi/google-api-23.jpg)
</details>

* File will be created and downloaded to your computer.
* Navigate to file and rename it: **'CREDS.json'**
* **make sure you have the same capitalization**
<details>

![GitHub](/assets/images/googleapi/google-api-24.jpg)
</details>


## 5. Go back to API Library & Install Google Sheets
* Click on burger menu top left and select API and Services --> Library
<details>

![GitHub](/assets/images/googleapi/google-api-25.jpg)
</details>

* In search window type **'google sheets'**
* Click on **Google Sheets API**
<details>

![GitHub](/assets/images/googleapi/google-api-26.jpg)  
<hr>

![GitHub](/assets/images/googleapi/google-api-27.jpg)
</details>

* Click on **ENABLE**
<details>

![GitHub](/assets/images/googleapi/google-api-28.jpg)
</details>

## 6. Copy Service account Email Address
* Click on **Credentials**
* Right click Service account email you created and copy
<details>

![GitHub](/assets/images/googleapi/google-api-29.jpg)
</details>


## 7. Share Google sheet with Service Account
* Go back to the new google sheet
* Click **SHARE** on the top right
<details>

![GitHub](/assets/images/googleapi/google-api-30.jpg)
</details>

* Paste the email address and uncheck Notify people
* Click **SEND**
<details>

![GitHub](/assets/images/googleapi/google-api-31.jpg)
</details>

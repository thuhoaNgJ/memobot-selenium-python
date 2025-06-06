# Memobot Selenium Python

## Overview
This project automates interactions with the Memobot application using Selenium WebDriver.

## Prerequisites
- Python 3.x
- Selenium library
- WebDriver for your preferred browser (e.g., ChromeDriver for Google Chrome): I use ChromeDriver for this code.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd memobot-selenium-python
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration
1. Update the email and password in file:
   ```python
   email = 'your_email@example.com'
   password = 'your_password'
   ```

2. Ensure the WebDriver executable is in your system PATH or specify its location in `setupDriver.py`.

## Running the Application
1. Open a terminal and navigate to the project directory.
2. Run the main script:
   Example:
   ```
   python check_chatAI.py
   ```
3. Create a new file:
   - test_file.py is already setup to write test function
   - 2 ways to create a test file:
     + Duplicate the test_file.py
     + Create a new file.py:
         - import check_login
         - import setupDriver
         - Launch chrome browser
         - Call login function from check_login.py
         - Continue to write test function...

## Notes
- Adjust the sleep times in the script as necessary to accommodate your internet speed and the application's response time.
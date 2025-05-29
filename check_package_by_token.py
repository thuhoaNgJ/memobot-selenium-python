import json
import requests
import check_login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_account_information(email):
    driver.get("https://app.memobot.io/tai-khoan")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.email_user.pb-65")))
    print("Load done page Tai khoan")
    # check the email of user
    actual_gmail = driver.find_element(By.CSS_SELECTOR,"div.email_user.pb-65").text
    print("actual_gmail is: " + actual_gmail)
    assert actual_gmail == email, f"Assertion failed: {actual_gmail} does not equal {email}"
    print("email is correct")

def get_token_from_local_storage():
        # Execute JavaScript to get the "tokens" value from local storage
    tokens = driver.execute_script("return Coo.getItem('tokens')")

    # Print the tokens
    print("Tokens from local storage:", tokens)

    # If you need to parse the JSON data to extract the access token
    if tokens:
        tokens_data = json.loads(tokens)
        access_token = tokens_data.get("access", {}).get("token")
        print("Access Token:", access_token)

def get_response_data(url, token=None):
    headers = {} 
    if token:
        headers["Authorization"] = f"Bearer {token}"  # Add the token to the headers

    response = requests.get(url, headers=headers)
    data = None

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to fetch API. Status code: {response.status_code}")
    
    return data, response


# Check luu_tru time and the number of used files of user
def check_user_package(url):
    driver.get("https://app.memobot.io/thanh-toan")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.package_content")))

    # Retrieve the token from local storage
    token = get_token_from_local_storage()
    if not token:
        print("Unable to retrieve token. Exiting.")
        return

    data, response = get_response_data(url, token)
 
    # Check if the request was successful
    if response.status_code == 200:
        # Compare luu_tru time (from API response) to luu_tru time presented on the screen
        luu_tru = data.get("data", {}).get("current", {}).get("value", {}).get("luu_tru", {}).get("value", None)
        if luu_tru is not None:
            luu_tru_time = int(((luu_tru / 1000) / 60) / 60)  # Convert milliseconds to hours and round the number down
            print(f"The value of 'luu_tru' from the API response is: {luu_tru_time} hours.")
        else:
            print("The 'luu_tru' field was not found in the response.")
        # Retrieve actual 'luu_tru' from the UI
        actual_luu_tru_time = driver.find_element(By.XPATH, "//div[@class='info_user_right p-4']//div[@class='mb-4'][3]//div[@class='content_info']//span[1]").text
        print(f"The actual 'luu_tru' presented on the screen is: {actual_luu_tru_time}")

        # Compare number of uploaded files minute (from API response) to the one on the screen
        so_file_upload = data.get("data", {}).get("current", {}).get("value", {}).get("so_file_upload", {}).get("value", None)
        if luu_tru is not None:
            print(f"The value of 'so_file_luu_tru' from the API response is: {so_file_upload} files.")
            assert so_file_upload == actual_so_file_upload, f"Assertion failed: {so_file_upload} does not equal {actual_so_file_upload}"
        else:
            print("The 'so_file_upload' field was not found in the response.")

        # Retrieve actual 'so_file_upload' from the UI
        actual_so_file_upload = driver.find_element(By.XPATH, "//div[@class='info_user_right p-4']//div[@class='mb-4'][1]//div[@class='content_info']//span[1]").text
        print(f"The actual 'so_file_upload' presented on the screen is: {actual_so_file_upload}")

        # Compare number of uploaded files minute (from API response) to the one on the screen
        so_file_upload = data.get("data", {}).get("current", {}).get("value", {}).get("so_file_upload", {}).get("value", None)
        if luu_tru is not None:
            print(f"The value of 'so_file_luu_tru' from the API response is: {so_file_upload} files.")
            assert so_file_upload == actual_so_file_upload, f"Assertion failed: {so_file_upload} does not equal {actual_so_file_upload}"
        else:
            print("The 'so_file_upload' field was not found in the response.")

        # Retrieve actual 'so_file_upload' from the UI
        actual_so_file_upload = driver.find_element(By.XPATH, "//div[@class='info_user_right p-4']//div[@class='mb-4'][1]//div[@class='content_info']//span[1]").text
        print(f"The actual 'so_file_upload' presented on the screen is: {actual_so_file_upload}")    


if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    check_login.check_login(driver, wait, email, password)
    # check xoá audio đầu tiên



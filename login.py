import setupDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import json
import time
import os

driver = setupDriver.setupWebdriver()
wait = WebDriverWait(driver, 10)

def check_login(email, password):
    input_email = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
    input_password = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Mật khẩu"]')
    login_btn = driver.find_element(By.ID, 'web-login')

    input_email.send_keys(email)
    input_password.send_keys(password)
    login_btn.click()
    time.sleep(5)

    # Close the promotion image
    try:
        # Wait for the promotion image to appear (optional: adjust timeout)
        promotion_img = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='promotion']"))
        )
        print("Promotion image is visible. Attempting to close the dialog.")

        # Click the promotion dialog close button
        promotion_close_btn = driver.find_element(By.CSS_SELECTOR, "div.dialog-promotion div.el-dialog__wrapper")
        promotion_close_btn.click()
        print("Promotion dialog closed successfully.")

    except Exception as e:
        print("Promotion image not found or already closed. Continuing execution.")

    # Close the notification popup
    try:
        # Wait for the notification popup to appear (optional: adjust timeout)
        notify_popup = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="el-message-box__title"]'))
        )
        print("Notification popup is visible. Attempting to close the popup.")

        # Click the notification popup close button
        notify_close_btn = driver.find_element(By.XPATH, '//button[@class="el-message-box__headerbtn"]')
        notify_close_btn.click()
        print("Notification popup closed successfully.")

    except Exception as e:
        print("Notification popup not found or already closed. Continuing execution.")

    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.pack-container')))
    print("login done")

def check_account_information():
    driver.get("https://app.memobot.io/tai-khoan")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.email_user.pb-65")))
    print("Load done page Tai khoan")
    # check the email of user
    actual_gmail = driver.find_element(By.CSS_SELECTOR,"div.email_user.pb-65").text
    print("actual_gmail is: " + actual_gmail)
    assert actual_gmail == email_plus, f"Assertion failed: {actual_gmail} does not equal {email_plus}"
    print("email is correct")

def get_token_from_local_storage():
        # Execute JavaScript to get the "tokens" value from local storage
    tokens = driver.execute_script("return localStorage.getItem('tokens')")

    # Print the tokens
    print("Tokens from local storage:", tokens)

    # If you need to parse the JSON data to extract the access token
    if tokens:
        tokens_data = json.loads(tokens)
        access_token = tokens_data.get("access", {}).get("token")
        print("Access Token:", access_token)

# def get_token_from_api(url):
#     # Example headers (customize as needed)
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         # Add any other required headers here
#     }

#     # Send the request
#     response = requests.get(url, headers=headers)

#     # Check if the response is successful
#     if response.status_code == 200:
#         # Extract the Authorization token from headers
#         token = response.headers.get("Authorization")
#         if token:
#             print("Token extracted from API headers:", token)
#         else:
#             print("Authorization token not found in headers.")
#         return token
#     else:
#         print(f"Failed to fetch API. Status code: {response.status_code}")
#         return None


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

# Check list languages
def check_list_languages():
    go_to_page("https://app.memobot.io")

    upload_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='upload-audio']")))
    driver.execute_script("arguments[0].click();", upload_button)

    language_option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.is-flex.items-center.mb-3 > div > div > input")))
    driver.execute_script("arguments[0].click();", language_option)

    try:
        # Locate all <li> elements
        li_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.el-select-dropdown__item > span"))
        )

        list_A = ["Tiếng Việt", "Tiếng Anh", "Tiếng Pháp (Thử nghiệm)", "Tiếng Trung (Thử nghiệm)", 
                "Tiếng Nhật (Thử nghiệm)", "Tiếng Hàn (Thử nghiệm)", "Tự động (Thử nghiệm)"]

        # Extract the text from each dropdown element
        dropdown_languages = [item.text.strip() for item in li_elements]
        # print("dropdown_languages: " + dropdown_languages)
        
        # Check if all items in List A are in the dropdown texts
        missing_items = [item for item in list_A if item not in dropdown_languages]
        
        if not missing_items:
            print("List language options: " + list_A)
        else:
            print(f"Missing items from the dropdown: {missing_items}")

    except Exception as e:
        print(f"An error occurred: {e}")        


def go_to_page(url):
    current_url = driver.current_url
    # Check if the URL does not contain the specified text
    if url not in current_url:
        driver.get(url)  # Navigate to the URL
        print(f"Redirected to {url}")
    else:
        print("Already on the correct page, continuing execution.")

# Check upload file
def upload_file(audio_path, audio_upload_name):
    go_to_page("https://app.memobot.io/")
    # Click button upload file
    upload_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='upload-audio']")))
    # audio_upload_name = "File 24p - Cách nhanh nhất để nâng cấp bản thân"
    try:
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_path = os.path.abspath(audio_path)
        file_input.send_keys(file_path)
        try:
            title_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//h2[contains(text(),'Chọn kênh âm thanh')]")))
            print("Element appeared:", title_element.text)
            time.sleep(5)
            channel_button = wait.until(EC.visibility_of_element_located(
                (By.XPATH,"(//button[@class='el-button el-button--default'] / span[contains(.,'Chọn kênh này')])[1]"))
                )
            channel_button.click()
            print("Clicked 'Chọn kênh này' của kênh số 1")
        except TimeoutException:
            print("Element 'Chọn kênh này' not found")
        loading_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Đang convert file')]"))
        )

        print("Loading text: ", loading_text.text)
        # Then, wait for it to disappear
        WebDriverWait(driver, 100).until(EC.invisibility_of_element_located((By.XPATH, "//p[contains(text(),'Đang convert file')]")))
        print("Loading text disappeared.")
        time.sleep(5)
        
        # Wait for all elements with class 'audio_title' to appear 
        # Means the audio is successfully uploaded
        audio_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']"))
        )

        # Extract text from all elements
        audio_texts = [element.text.strip() for element in audio_elements]

        # Print all extracted texts
        print("List of audio titles:", audio_texts)

        # Check if audio name is in the list
        if audio_upload_name in audio_texts:
            print("✅ Uploaded file is found in the list!")
        else:
            print("❌ Uploaded file is NOT found in the list.")
            
    except Exception as e:
        print(f"An error occurred: {e}")


def search_audio(search_input):
    go_to_page("https://app.memobot.io/")
    try:
        print("search input is: ", search_input)
        search_textbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='search_transcript']")))
        search_textbox.send_keys(search_input)
        time.sleep(5)
        searched_audio_title = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']"))
        )
        audio_title = [element.text.strip() for element in searched_audio_title]
        print("Search results audio title: ", audio_title)
        # check if the search_input appear anywhere in the audio_title of the result list
        if any(search_input in title for title in audio_title):
            print("✅ Audio is found in the list!")
        else:
            print("❌ Audio is NOT found in the list.")
    except Exception as e:
        print(f"An error occurred: {e}")

def filter_audio_by_date():
    go_to_page("https://app.memobot.io/")
    try:
        date_filter_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Đến ngày')]")))
    except Exception as e:
        print(f"An error occurred: {e}")


def edit_audio_name():
    go_to_page("https://app.memobot.io/")

    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    
    if len(audio_titles) > 1:  # Kiểm tra tránh lỗi IndexError
        audio_titles[0].click()
    else:
        print("This account doesn't have any audio")
        return
    
    # Tìm và nhập nội dung vào textarea
    time.sleep(5)
    title_areatext = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//textarea[contains(@class, 'f4 w-100 mb2')]")))
    title_areatext[0].clear()  # Xóa nội dung cũ trước khi nhập mới
    title_areatext[0].send_keys("Tên mới của audio")

    # Click vào biểu tượng lịch
    wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='fa fa-calendar']"))).click()
    time.sleep(5)

    driver.back()

    audio_name = [element.text.strip() for element in audio_titles]
    print("Search results audio title: ", audio_name)
    # check if the search_input appear anywhere in the audio_title of the result list
    if any("Tên mới của audio" in title for title in audio_name):
        print("✅ Audio title is changed successfully!")
    else:
        print("❌ Audio title is changed unsuccessfully")


email_plus = "memo17@mailinator.com"
password_plus = "Abcd@12345"
url = "https://sohoa.memobot.io/analytic-v2/api/v1/payment/user-usage-stats"
audio_path = "C://Users/admin/Videos/Memobot/Audio test memobot/File 24p - Cách nhanh nhất để nâng cấp bản thân.mp3"
audio_upload_name = "File 24p - Cách nhanh nhất để nâng cấp bản thân"

check_login(email_plus, password_plus)
# check_account_information()
# get_token_from_local_storage()
# check_user_package(url)
# check_list_languages()
# upload_file()
# upload_file(audio_path, audio_upload_name)
# search_input = "nội dung tiêu cực" 
# search_audio(search_input)
edit_audio_name()






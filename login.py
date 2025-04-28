import setupDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from langdetect import detect
from collections import Counter
import re
import requests
import json
import time
import os

driver = setupDriver.setupWebdriver()
wait = WebDriverWait(driver, 10)
options = Options()

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

def edit_audio_name(title_id, new_title):
    go_to_page("https://app.memobot.io/")

    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    
    if len(audio_titles) > 1:  # Kiểm tra tránh lỗi IndexError
        audio_titles[title_id].click()
    else:
        print("This account doesn't have any audio")
        return
    
    # Tìm và nhập nội dung vào textarea
    time.sleep(5)
    title_areatext = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//textarea[contains(@class, 'f4 w-100 mb2')]")))
    title_areatext[title_id].clear()  # Xóa nội dung cũ trước khi nhập mới
    time.sleep(3)
    title_areatext[title_id].send_keys(new_title)
    driver.find_element(By.XPATH, "//button[contains(text(),'Đánh dấu')]").click()
    time.sleep(5)
    driver.back()
    audio_name = [element.text.strip() for element in audio_titles]
    print("Search results audio title: ", audio_name)
    # check if the search_input appear anywhere in the audio_title of the result list
    if any("Tên mới của audio" in title for title in audio_name):
        print("✅ Audio title is changed successfully!")
    else:
        print("❌ Audio title is changed unsuccessfully")

def delete_audio():
    go_to_page("https://app.memobot.io/")
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))

    if len(audio_titles) > 0: 
        delete_audio_title = audio_titles[0].text
        print("The audio's name is chosen to delete: " + delete_audio_title) 

        delete_audio_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "(//button[@id='delete_transcript'])[1]"))) 
        delete_audio_btn.click()
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//h2[contains(text(),'Xóa bản ghi âm')]")))
        confirm_delete_btn = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//button[@class='el-button mt-4 btn_new_layout_v2_popup el-button--danger']//span[contains(text(),'Xóa')]")))
        confirm_delete_btn.click()
        time.sleep(5)

        # compare the 1st audio's name before and after deleteing
        if len(audio_titles) > 0: 
            audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
            print("The first audio title after deleting the first audio: ", audio_titles[0].text)
            if (delete_audio_title != audio_titles[0].text):
                print("✅DONE delete the first audio of the audio list")
            else:
                print("❌Audio hasn't been deleted.")
        else:
            print("✅The number of audio is 0. The audio is already deleted.")

def filter_audio_by_date():
    go_to_page("https://app.memobot.io/")
    calender_filter = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//input[contains(@placeholder, 'Tìm từ ngày')]")))
    calender_filter.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='vc-weeks']")))
    return
 

def upload_file(chosen_language, audio_path, audio_upload_name):
    go_to_page("https://app.memobot.io/")
    time.sleep(5)
    
    try:
        # Choose language
        upload_file_btn = driver.find_element(By.XPATH, "//span[@class='title-file-upload']")
        upload_file_btn.click()
        language_dropdowns = driver.find_element(
            By.XPATH, "//div[@class='pb_share absolute hidden show']//input[@placeholder='Select']")
        language_dropdowns.click()
        
        language_options = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.el-select-dropdown__item > span"))
        )
        language_name = [item.text.strip() for item in language_options]
        print(language_name)

        for option in language_options:
            text = option.text.strip()
            if text == chosen_language:
                option.click()
                print(f"✅ Đã chọn ngôn ngữ: {text}")
                break
        else:
            print(f"❌ Không tìm thấy ngôn ngữ: {chosen_language}")
 
        # Upload file audio theo ngôn ngữ đã chọn

        # driver.set_window_size(800, 800)
        # driver.refresh() 
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
             time.sleep(5)
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

        time.sleep(5)
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
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(),'Tệp âm thanh')])"))) 
        print("Done convert file")    
    except Exception as e:
        print(f"An error occurred: {e}")

# Chuyển ngôn ngữ được chọn thành mã ngôn ngữ
def get_lang_code(language_name): 
    lang_code_map = {
        "Tiếng Việt": "vi",
        "Tiếng Anh": "en",
        "Tiếng Pháp (Thử nghiệm)": "fr",
        "Tiếng Trung (Thử nghiệm)": "zh-cn",
        "Tiếng Nhật (Thử nghiệm)": "ja",
        "Tiếng Hàn (Thử nghiệm)": "ko",
        "Tự động (Thử nghiệm)": "auto" 
    }

    lang_code = lang_code_map.get(language_name, "unknown")

    if lang_code != "unknown":
        print(f"Mã ngôn ngữ của '{language_name}' là: '{lang_code}'")
    else:
        print(f"⚠️Không xác định được mã ngôn ngữ của: '{language_name}'")

    return lang_code 


def detect_language_from_text(full_text: str, chosen_language_code):
    """
    Phát hiện ngôn ngữ chính trong một đoạn text,
    và liệt kê các câu không phải thuộc ngôn ngữ mong muốn.
    
    Args:
        full_text (str): Đoạn văn cần kiểm tra.
        chosen_language_code (str): Mã ngôn ngữ mong đợi (vd: 'vi' cho tiếng Việt).
        
    Returns:
        None
    """
    # 🧹 Tách câu dựa trên dấu câu tiếng Việt + tiếng Nhật
    sentences = re.split(r'[.,?!;:。、？！]\s*', full_text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    lang_count = Counter()
    non_chosen_sentences = []

    for sentence in sentences:
        try:
            lang = detect(sentence)
            lang_count[lang] += 1

            if lang != chosen_language_code:
                non_chosen_sentences.append((sentence, lang))
        except Exception as e:
            print(f"⚠️ Lỗi khi detect câu '{sentence}': {e}")

    # 🧠 In kết quả
    most_common_lang = lang_count.most_common(1)[0][0] if lang_count else 'unknown'
    print(f"\n🔍 Ngôn ngữ chiếm ưu thế: {most_common_lang}")

    if most_common_lang == chosen_language_code:
        print(f"✅ Đoạn text chủ yếu là {chosen_language_code}.")
    else:
        print(f"❌ Đoạn text chủ yếu không phải {chosen_language_code}, mà là: {most_common_lang}")

    # 📌 In các câu không thuộc ngôn ngữ mong muốn
    if non_chosen_sentences:
        print("\n📛 Các câu không phải ngôn ngữ mong muốn:")
        for sentence, lang in non_chosen_sentences:
            print(f"  - '{sentence}' ➡ {lang}")
    else:
        print("\n🎉 Tất cả câu đều thuộc ngôn ngữ mong muốn!")



def check_language(chosen_language, audio_path, audio_upload_name):
    go_to_page("https://app.memobot.io/")
    upload_file(chosen_language, audio_path, audio_upload_name)
    lang_code = get_lang_code(chosen_language)
    # vi_audio_path = "C://Users/admin/Videos/Memobot/Audio test memobot/Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24.mp3"
    # vi_audio_name = "Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24"
    # chosen_language = 'vi'
    # upload_file(chosen_language, vi_audio_path, vi_audio_name)
    print("DONE upload " + chosen_language + " audio")
    # wait until the audio complete
    # WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(),'Tệp âm thanh')])"))) 
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    print("Audio uploaded name: " + audio_titles[0].text)
    audio_titles[1].click()

    content_audio = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Bản dịch')]")))
    content_audio.click()
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-type,'audio-text')]")))
    audio_text = driver.find_elements(By.XPATH, "//span[contains(@data-type,'audio-text')]")
    print("The first word of audio text: " + audio_text[0].text)

    all_words = []
    non_chosen_words = []

    for element in audio_text:
        word = element.text.strip()
        if word:
            all_words.append(word)

    # Gộp lại thành 1 câu
    full_text = ' '.join(all_words)
    print("📝 Full sentence:", full_text)
    detect_language_from_text(full_text, lang_code)

    # # Đếm số lượng từng ngôn ngữ
    # lang_count = Counter()

    # for word in all_words:
    #     try:
    #         lang = detect(word)
    #         lang_count[lang] += 1

    #         if lang != 'vi':
    #             non_chosen_words.append((word, lang))
    #     except Exception as e:
    #         print(f"⚠️ Lỗi khi detect từ '{word}': {e}")

    # # 🧠 In kết quả
    # most_common_lang = lang_count.most_common(1)[0][0] if lang_count else 'unknown'
    # print(f"\n🔍 Ngôn ngữ chiếm ưu thế: {most_common_lang}")

    # if most_common_lang == 'vi':
    #     print("✅ Đoạn text chủ yếu là tiếng Việt.")
    # else:
    #     print(f"❌ Không phải tiếng Việt, có vẻ là: {most_common_lang}")

    # # 📌 In các từ không phải tiếng Việt
    # if non_chosen_words:
    #     print("\n📛 Các từ không phải tiếng Việt:")
    #     for word, lang in non_chosen_words:
    #         print(f"  - '{word}' ➡ {lang}")
    # else:
    #     print("\n🎉 Không có từ nào khác ngoài tiếng Việt.")
    
   


email_plus = "memo17@mailinator.com"
password_plus = "Abcd@12345"
url = "https://sohoa.memobot.io/analytic-v2/api/v1/payment/user-usage-stats"
audio_path = "C://Users/admin/Videos/Memobot/Audio test memobot/Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24.mp3"
audio_upload_name = "Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24" #get the exactly name of the audio after successfully

check_login(email_plus, password_plus)
# check_account_information()
# get_token_from_local_storage()
# check_user_package(url)
check_list_languages()
# upload_file("Tiếng Việt", audio_path, audio_upload_name)
# search_input = "nội dung tiêu cực" 
# search_audio(search_input)
# edit_audio_name(0,"Tên mới của audio")
# delete_audio()
# filter_audio_by_date()
vi_audio_path = "C://Users/admin/Videos/Memobot/Audio test memobot/Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24.mp3"
vi_audio_name = "Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24"
chosen_language = 'Tiếng Việt'
#check language of an uploaded audio
check_language(chosen_language, vi_audio_path, vi_audio_name)







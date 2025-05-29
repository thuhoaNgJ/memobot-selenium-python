import setupDriver
import check_login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langdetect import detect
from collections import Counter
import re
import time
import os
from selenium.common.exceptions import TimeoutException

# Check list languages
def check_list_languages():
    check_login.go_to_page(driver, "https://app.memobot.io")

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

def upload_file(driver, wait, chosen_language, audio_path, audio_upload_name):
    check_login.go_to_page(driver, "https://app.memobot.io/")
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


def detect_language_from_text(full_text, chosen_language_code):
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

def check_language(driver, wait, chosen_language, audio_path, audio_upload_name):
    check_login.go_to_page(driver, "https://app.memobot.io/")
    upload_file(driver, wait, chosen_language, audio_path, audio_upload_name)
    lang_code = get_lang_code(chosen_language)
    print("DONE upload " + chosen_language + " audio")
    # wait until the audio complete
    # WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "(//p[contains(text(),'Tệp âm thanh')])"))) 
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    print("Audio uploaded name: " + audio_titles[0].text)
    audio_titles[1].click()

    # Gộp lại thành màn 'Bản dịch' thành 1 câu, sau đó dùng detect_language_from_text() 
    # để check xem ngôn ngữ xuất hiện chủ yếu trong bản dịch audio là gì

    content_audio = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Bản dịch')]")))
    content_audio.click()
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-type,'audio-text')]")))
    audio_text = driver.find_elements(By.XPATH, "//span[contains(@data-type,'audio-text')]")
    print("The first word of audio text: " + audio_text[0].text)

    all_words = []

    for element in audio_text:
        word = element.text.strip()
        if word:
            all_words.append(word) 

    # Gộp lại thành 1 câu
    full_text = ' '.join(all_words)
    print("📝 Full sentence:", full_text)
    detect_language_from_text(full_text, lang_code)


if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    check_login.check_login(driver, wait, email, password)

    audio_path = "/Users/apple/Documents/memobot/Vais memobot/audio file/Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24.mp3"
    audio_upload_name = "Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24" #get the exactly name of the audio after successfully
    chosen_language = "Tiếng Việt" 
    # liệt kê các ngôn ngữ có trong dropdown
    check_list_languages()

    #upload audio với ngôn ngữ đã chọn là "Tiếng Việt"
    upload_file(driver, wait,"Tiếng Việt", audio_path, audio_upload_name) 

    # kiểm tra ngôn ngữ của audio đã upload có đúng như ngôn ngữ đã chọn hay không
    # chuyển ngôn ngữ đã chọn thành mã ngôn ngữ
    get_lang_code(chosen_language) 

    # kiểm tra ngôn ngữ của audio đã upload
    check_language(driver, wait, chosen_language, audio_path, audio_upload_name)

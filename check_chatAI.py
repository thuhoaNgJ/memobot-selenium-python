import pyperclip
import check_login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.common.exceptions import TimeoutException

def go_to_chatAI_page(driver, wait):
    search_input = "YouTube"
    check_login.search_audio(driver, wait, search_input)
    searched_audio_title = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']"))
        )
    audio_title = searched_audio_title[0].text.strip() # click on the first audio in the search result
    searched_audio_title[0].click()  

    chat_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='Chat']")))
    chat_btn.click()
    time.sleep(5)  # wait for the chat page to load
    # 📝 Lấy toàn bộ nội dung văn bản từ trang
    page_text = driver.page_source

    # 🔍 Kiểm tra tên audio có tồn tại không
    if audio_title in page_text:
        print("Đã mở trang chat AI thành công với audio: ", audio_title)
    else:
        print("❌ Không mở được trang chat AI với audio: ", audio_title)

def get_chatAT_token(driver, wait):
    # 💫 Regex tìm 2 con số kiểu '11k' và '500k'
    token_text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-placement='bottom']"))).text
    print("Giá trị hiện tại:", token_text)
    match = re.search(r'Token:\s*(\d+(?:\.\d+)?k)\s*/\s*(\d+(?:\.\d+)?k)', token_text)
    if match:
        current_token_str = match.group(1)  # "11k"
        max_token_str = match.group(2)      # "500k"

        # 🔄 Chuyển 'k' thành số
        current_token = float(current_token_str.replace("k", "")) * 1000
        max_token = float(max_token_str.replace("k", "")) * 1000

        print(f"Token hiện tại: {int(current_token)}")
        print(f"Giới hạn token: {int(max_token)}")
    else:
        print("Không tìm thấy số token.")
    return int(current_token), int(max_token)

# div class chứa 'justify-content-start': câu hỏi AI gợi ý
# div class chứa 'justify-end': câu hỏi đã đươc gửi
# div class chứa 'justify-start': câu trả lời do AI tạo ra

def send_question(driver, wait):
    current_token, _ = get_chatAT_token(driver, wait)
    print("Giá trị token hiện tại là:", current_token)  
    
    # Tìm div cha chứa class 'justify-content-start' bằng wait
    parent_div = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'justify-content-start')]"))
    )

    # Lấy các nút <button> bên trong div đó
    AIquestion_buttons = parent_div.find_elements(By.TAG_NAME, "button")

    # In ra text từng button
    print("Danh sách câu hỏi AIgen:")
    for btn in AIquestion_buttons:
        print("-", btn.text.strip())
    
    #Kiểm tra ấn vào 1 câu hỏi AIgen
    if AIquestion_buttons:
        print("✅ Đã tìm thấy câu hỏi AIgen.")
        AIquestion_buttons[0].click()  # ấn vào câu hỏi AIgen đầu tiên
        time.sleep(10)  # đợi một chút để xem phản hồi

        # Kiểm tra xem có gửi đúng câu hỏi đầu đã chọn được AI gen không?
        # Lấy text của nút button đầu tiên (btn[0])
        first_question_text = AIquestion_buttons[0].text.strip()
        # Lấy nội dung của câu hỏi đầu tiên đã gửi 
        sent_questions = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'justify-end')]/div"))
        )
        sent_questions_text = sent_questions[0].text.strip()
        # So sánh và in kết quả
        if sent_questions_text == first_question_text:
            print("Đã gửi câu hỏi AI gen đầu tiên.")
        else:
            print("Câu hỏi chưa khớp với nút đầu tiên.")

        # Kiểm tra xem có nhận được câu trả lời từ AI không?
        AI_response = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'justify-start')]/div"))
        )
        AI_response_text = AI_response[0].text.strip()
        if AI_response_text:
            print("Đã nhận được câu trả lời từ AI gen.")
            print("Câu trả lời:", AI_response_text)
        else:
            print("❌ Không nhận được câu trả lời từ AI gen.")  

        # Kiểm tra xem token đã sử dụng có tăng không
        new_current_token, _ = get_chatAT_token(driver, wait) 
        if new_current_token > current_token:
            print("✅ Token sử dụng đã tăng sau khi ấn vào câu hỏi AIgen.")
        else:
            print("❌ Token không tăng sau khi ấn vào câu hỏi AIgen.")
 
    else:
        print("❌ Không tìm thấy câu hỏi AIgen.")

def check_input_question(driver, wait):
    current_token, _ = get_chatAT_token(driver, wait)
    print("Giá trị token hiện tại là:", current_token)  
    # Nhập và gửi câu hỏi đến AIgen
    input_box = wait.until(EC.presence_of_element_located((
        By.XPATH, "//textarea[@placeholder='Bắt đầu nhập... (Enter để submit, Shift-Enter để xuống dòng)']"
        )))
    input_box.send_keys("Có cần kiểm soát những nội dung tiêu cực từ Youtube không?") 

    # Tìm nút gửi và click vào nó
    send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    send_button.click()
    time.sleep(10)  # Đợi một chút để xem phản hồi

    # Kiểm tra xem có nhận được câu trả lời từ AI không?
    AI_response = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'justify-start')]/div"))
    )
    AI_response_text = AI_response[0].text.strip()
    if AI_response_text:
        print("Đã nhận được câu trả lời từ AI gen.")
        print("Câu trả lời:", AI_response_text)
    else:
        print("❌ Không nhận được câu trả lời từ AI gen.")  

    # Kiểm tra xem token đã sử dụng có tăng không
    new_current_token, _ = get_chatAT_token(driver, wait) 
    if new_current_token > current_token:
        print("✅ Token sử dụng đã tăng sau khi ấn vào câu hỏi AIgen.")
    else:
        print("❌ Token không tăng sau khi ấn vào câu hỏi AIgen.")

def get_answer_text(driver, wait):
    # Tìm câu trả lời do AI tạo ra
    AI_response = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'justify-start')]/div"))
    )
    if AI_response:
        AI_response_text = AI_response[0].text.strip()
        print("Câu trả lời:", AI_response_text)
        return AI_response_text
    else:
        print("❌ Không tìm thấy câu trả lời từ AI gen.")
        return None

def check_copy_answer(driver, wait):
    try:
        copy_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Sao chép']"))
        )
        print("Nút 'Sao chép' đã xuất hiện.")
    except TimeoutException:    
        print("❌ Nút 'Sao chép' chưa xuất hiện do chưa có câu hỏi và câu trả lời nào.")
        check_input_question(driver, wait)

    copy_button.click()
    print("✅ Đã bấm nút 'Sao chép'.")
    # Kiểm tra xem có thông báo sao chép thành công không? 
    # so sánh text trong câu trả lời có chứa trong đoạn copy không?
    copied_answer_text = pyperclip.paste().split('[')[0].strip() 
    # dùng split để loại bỏ dạng [1]("?time_code=00:01:20" 
    print("Đoạn text đã sao chép:", copied_answer_text)
    AI_response_text = get_answer_text(driver, wait) # đoạn text đầu trong câu trả lời AI gen
    
    print("Đoạn text trong câu trả lời AI gen:", AI_response_text)
    if AI_response_text:
        if copied_answer_text in AI_response_text in copied_answer_text:
            print("✅ Đã sao chép câu trả lời thành công.")
        else:
            print("❌ Không sao chép được câu trả lời.")

def save_answer(driver, wait):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'justify-around')]"))
        )
        # ✅ Cuộn tới cuối
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", discussion_div)

        save_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/i[@class='fa fa-save']"))
        )
        print("Nút 'Lưu' đã xuất hiện.")
    except TimeoutException:    
        print("❌ Nút 'Lưu' chưa xuất hiện do chưa có câu hỏi và câu trả lời nào.")
        check_input_question(driver, wait)

    save_button.click()
    print("✅ Đã bấm nút 'Lưu'.")
    # Kiểm tra xem có thông báo lưu thành công không?
    
    # ✅ Tìm thẻ <p> đầu tiên bên trong div có id chứa 'noteModalbookmark'
    p_element = driver.find_element(By.XPATH, "//div[contains(@id, 'noteModalbookmark')]//p[1]")

    # ✅ Lấy text
    first_paragraph = p_element.text
    print("📝 Đoạn text đầu tiên trong <p>:", first_paragraph)    
    clean_text = first_paragraph.split('[')[0].strip()
    print("🔍 Text trước dấu [: ", clean_text)
              

if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    # Khởi tạo 2 trình duyệt
    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    check_login.check_login(driver, wait, email, password)
    # go_to_chatAI_page(driver, wait)
    driver.get("https://app.memobot.io/memobot-v2/#!/memobot-audios/chat/681d68bca4e66dc8d4736dbf")
    time.sleep(10)  # wait for the chat page to load
    send_question(driver, wait)
    check_input_question(driver, wait)
    check_copy_answer(driver, wait)
    # save_answer(driver, wait)
import re
import check_login
import check_search_audio
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def edit_audio_name(title_id, new_title):
    driver.get("https://app.memobot.io/")
    time.sleep(5)

    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    
    if len(audio_titles) > 1: 
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

def edit_audio_summary(driver, wait, text_tab, targetText, insertText):
    tab_option = f"//button[contains(text(),'{text_tab}')]"
    text_tab = wait.until(
        EC.presence_of_element_located((By.XPATH, tab_option))
    )
    text_tab.click()
    time.sleep(10)

    # Tìm phần tử contenteditable
    p = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")

    # Lấy HTML hiện tại trong phần tử
    html = p.get_attribute("innerHTML")
    # print("htmllllllllllllllllllllllllll: " + html)

    # Kiểm tra nếu targetText có trong đoạn HTML của phần tử
    if targetText in html:
        print("✅ Đoạn văn bản mục tiêu đã được tìm thấy!")

        # Chèn đoạn văn bản insertText vào đúng vị trí trước targetText
        new_html = html.replace(targetText, insertText + targetText)

        # Cập nhật lại nội dung trong phần tử
        driver.execute_script("arguments[0].innerHTML = arguments[1];", p, new_html)

        # Đợi một chút để xem kết quả
        time.sleep(2)

        # Lấy lại nội dung sau khi thay đổi
        paragraphs_after_added = p.get_attribute("innerHTML")

        # Kiểm tra xem đoạn văn bản insertText đã được thêm vào đúng vị trí chưa
        if insertText in paragraphs_after_added:
            print("✅ Đã chèn vào đoạn văn đúng!")
        else:
            print("❌ Chưa chèn đúng vào đoạn văn!")
    else:
        print("❌ Không tìm thấy đoạn văn bản mục tiêu!")
        

def delete_audio_summary_text():
    driver.get("https://app.memobot.io/")
    time.sleep(10)
    search_input = 'Holodomor'
    check_search_audio.search_audio(search_input)
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    audio_titles[0].click()
    time.sleep(5)

    # Mở tab "Dòng thời gian"
    timeline_tab = driver.find_element(By.XPATH, "//button[contains(text(),'Dòng thời gian')]")
    timeline_tab.click()
    time.sleep(10)

    # Tìm phần tử contenteditable
    p = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
    html = p.get_attribute("innerHTML")

    # Đoạn văn bản mục tiêu cần xóa
    targetText = "ĐÂY LÀ ĐOẠN TEXT ĐƯỢC THÊM BỞI AUTO TEST."

    if targetText in html:
        print("✅ Đoạn văn bản mục tiêu đã được tìm thấy!")

        # Xóa đoạn targetText
        new_html = html.replace(targetText, '')

        # Cập nhật lại nội dung đã xóa
        driver.execute_script("arguments[0].innerHTML = arguments[1];", p, new_html)

        time.sleep(2)

        # Kiểm tra kết quả sau khi xóa
        html_after_delete = p.get_attribute("innerHTML")
        if targetText not in html_after_delete:
            print("✅ Đã xóa thành công đoạn văn bản!")
        else:
            print("❌ Xóa thất bại – đoạn văn bản vẫn còn tồn tại!")
    else:
        print("❌ Không tìm thấy đoạn văn bản mục tiêu để xóa!")


def format_audio_summary_text(style='bold'):
    driver.get("https://app.memobot.io/")
    time.sleep(10)
    search_input = 'Holodomor'
    check_search_audio.search_audio(search_input)
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    audio_titles[0].click()
    time.sleep(5)

    # Mở tab "Dòng thời gian"
    timeline_tab = driver.find_element(By.XPATH, "//button[contains(text(),'Dòng thời gian')]")
    timeline_tab.click()
    time.sleep(10)

    # Lấy phần tử contenteditable
    p = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
    html = p.get_attribute("innerHTML")

    # Đoạn văn cần định dạng
    targetText = "Rất có thể đây là kế hoạch có chủ ý được thực hiện một cách tinh vi, có chủ đích để kiểm soát và đàn áp cả một dân tộc"

    if targetText in html:
        print("✅ Đã tìm thấy đoạn văn bản cần định dạng!")

        # Định dạng đoạn văn
        if style == 'bold':
            formatted = f"<b>{targetText}</b>"
        elif style == 'italic':
            formatted = f"<i>{targetText}</i>"
        else:
            print("⚠️ Chỉ hỗ trợ định dạng 'bold' hoặc 'italic'.")
            return

        # Thay thế trong HTML
        driver.execute_script("window.scrollTo(0, 0);")
        new_html = html.replace(targetText, formatted)
        driver.execute_script("arguments[0].innerHTML = arguments[1];", p, new_html)

        time.sleep(2)

        # Kiểm tra xem đã thay thành công chưa
        html_after_format = p.get_attribute("innerHTML")
        # Tạo biểu thức regex dựa theo style
        # re.escape(targetText) để escape ký tự đặc biệt.
        # .*? cho phép có các thẻ HTML bọc quanh targetText (như <span>).
        # flags=re.DOTALL để . match cả xuống dòng nếu có.
        if style == 'bold':
            pattern = rf"<strong[^>]*>.*?{re.escape(targetText)}.*?</strong>"
        elif style == 'italic':
            pattern = rf"<i[^>]*>.*?{re.escape(targetText)}.*?</i>"
        else:
            pattern = None

        if pattern and re.search(pattern, html_after_format, flags=re.DOTALL):
            print(f"✅ Đã áp dụng định dạng {style} thành công!")
        else:
            print(f"❌ Không áp dụng được định dạng {style}.")                      

if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    check_login.check_login(driver, wait, email, password)

    # đổi tên audio đầu tiên trong danh sách
    # edit_audio_name(0,"Tên mới của audio")

    # Đoạn văn bản mục tiêu dể sửa audio
    targetText = "Điện thoại thông minh và Internet đã trở thành một phần không thể thiếu trong cuộc sống của mọi người, từ trẻ nhỏ đến người già"
    # Đoạn văn bản cần chèn
    insertText = " ĐÂY LÀ ĐOẠN TEXT ĐƯỢC THÊM BỞI AUTO TEST. "

    # Cần gọi hàm tới audio trước sau đó gọi hàm sửa audio
    check_search_audio.go_to_audio_by_search(driver, wait, "internet")

    # thêm đoạn văn bản vào audio ở tab Dòng thời gian
    edit_audio_summary(driver, wait, 'Dòng thời gian', targetText, insertText)
    # Xóa đoạn văn bản đã chèn
    # delete_audio_summary_text()
    # Định dạng đoạn văn bản
    # format_audio_summary_text('bold') #in đậm
    # format_audio_summary_text('italic') #in nghiêng
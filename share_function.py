import login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pyperclip

#User host setup authorization for audio
def go_to_audio(driver, wait, search_input):
    audio_text = "Tác hại của việc sử dụng quá nhiều internet và thiết bị thông minh, đặc biệt là với trẻ em và thanh thiếu niên"
    page_text = driver.find_element(By.TAG_NAME, "body").text
    print("page text: "+ page_text)
    if audio_text not in page_text:
        driver.get("https://app.memobot.io/")
    try:
        print("search input is: ", search_input)
        search_textbox = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='search_transcript']")))
        search_textbox.send_keys(search_input)
        time.sleep(10)
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

def get_share_audio_link(driver, wait):
    go_to_audio(driver, wait, "internet")
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    audio_titles[0].click()
    time.sleep(10)
    share_function_btn = driver.find_element(By.XPATH, "//button[contains(@data-bs-target, 'modal-share-audio')]")
    share_function_btn.click()
    copy_button = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//button[@data-bs-dismiss='modal' and text()='Sao chép liên kết']")
    ))
    time.sleep(5)
    copy_button.click()
    share_url = pyperclip.paste()
    print("✅ URL đã copy là:", share_url)
    print("done function get_share_audio_link")
    return share_url

def setup_shared_user(driver, wait, permission_option):
    go_to_audio(driver, wait, "internet")
    print("heloooooooo")
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    audio_titles[0].click()
    time.sleep(10)
    print("✅ done go to youtube url audio.")
    share_function_btn = driver.find_element(By.XPATH, "//button[contains(@data-bs-target, 'modal-share-audio')]")
    share_function_btn.click()
    copy_button = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//button[@data-bs-dismiss='modal' and text()='Sao chép liên kết']")
    ))
    auth_dropdown_options = driver.find_element(By.XPATH, "//span[@class='me-2']//button[@id='dropRoleButton']")
    auth_dropdown_options.click()
    shared_chosen_option = f"//span[.='{permission_option}']"
    permission_element = wait.until(
        EC.presence_of_element_located((By.XPATH, shared_chosen_option))
    )
    permission_element.click()
    print(f"🔐 Đã chọn quyền: {permission_option}")
    time.sleep(5) #wait to save option

#check quyền của user
# Check user không được phân quyền
def check_user_no_auth(driver, wait, share_url):
    driver.get(share_url)
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "img[src='/memobot-v2/logo-memo.png']")))
    page_text = driver.find_element(By.TAG_NAME, "body").text
    if "Bạn không có quyền truy cập trang này" in page_text:
        print("🚫User không có quyền xem audio này.")
    else:
        print("✅Người dùng có quyền truy cập.")
    return

# check tất cả user có quyền xem
def check_user_only_see(driver, wait, share_url):
    driver.get(share_url)
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "img[src='/memobot-v2/logo-memo.png']")))
    text_tab, targetText, insertText = ["Dòng thời gian", "Điện thoại thông minh và Internet", "Thêm đoạn text"]
    login.edit_audio_summary(driver, wait, text_tab, targetText, insertText)

if __name__ == "__main__":
    # Khởi tạo 2 trình duyệt
    driverHost = setupDriver.setupWebdriver()
    driverUser = setupDriver.setupWebdriver()
    waitHost = WebDriverWait(driverHost, 15)
    waitUser = WebDriverWait(driverUser, 15)
    # Tài khoản user1 và user2
    email_host = 'memo17@mailinator.com'
    pass_host = 'Abcd@12345'
    email_user = 'memo16@mailinator.com'
    pass_user = 'Abcd@12345'

    login.check_login(driverHost, waitHost, email_host, pass_host)
    login.check_login(driverUser, waitUser, email_user, pass_user)

    # share_url = get_share_audio_link(driverHost, waitHost)
    # check_user_no_auth(driverUser, waitUser, share_url)

    share_user_option = "Chỉ những người dùng được mời"
    share_user_only_see_audio = "Bất kì ai có link chi có thể xem"
    share_user_see_edit_audio = "Bất kì ai có link đều có thể xem và sửa"
    setup_shared_user(driverHost, waitHost, share_user_only_see_audio)
    # check_user_only_see(driverUser, waitUser, share_url)



   

    





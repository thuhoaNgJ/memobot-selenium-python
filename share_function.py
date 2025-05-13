import login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pyperclip

#User host setup authorization for audio
def go_to_audio(driver, wait):
    audio_text = "Tóm tắt Thảo luận về Ảnh Hưởng của Phim Ngắn Trên YouTube Đối Với Giới Trẻ"
    page_text = driver.find_element(By.TAG_NAME, "body").text
    print("page text: "+ page_text)
    if audio_text not in page_text:
        driver.get("https://app.memobot.io")
        time.sleep(10)
        search_input = "YouTube" 
        login.search_audio(driver, wait, search_input)
        time.sleep(5)
        audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
        audio_titles[0].click()

def get_share_audio_link(driver, wait):
    go_to_audio(driver, wait)
    time.sleep(5)
    share_function_btn = driver.find_element(By.XPATH, "//button[contains(@data-bs-target, 'modal-share-audio')]")
    share_function_btn.click()
    copy_button = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//button[@data-bs-dismiss='modal' and text()='Sao chép liên kết']")
    ))
    copy_button.click()
    share_url = pyperclip.paste()
    print("✅ URL đã copy là:", share_url)
    return share_url

def setup_shared_all_user_see_audio(driver, wait, permission_option):
    go_to_audio(driver, wait)
    print("done go to youtube url audio.")
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

#check tất cả user có quyền xem
# def check_user_only_see(driver, wait, share_url):
#     driver.get(share_url)
#     wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "img[src='/memobot-v2/logo-memo.png']")))

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
    # login.check_login(driverUser, waitUser, email_user, pass_user)
    # print("done login")
    # share_url = get_share_audio_link(driverHost, waitHost)
    # check_user_no_auth(driverUser, waitUser, share_url)

    setup_shared_all_user_see_audio(driverHost, waitHost)

   

    





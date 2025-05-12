import login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pyperclip

def pause_until_done():
    input("🟢 Script kết thúc. Nhấn Enter để đóng trình duyệt...")

def get_share_audio_link(driver, wait):
    search_input = "YouTube" 
    login.search_audio(driver, wait, search_input)
    time.sleep(5)
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    audio_titles[0].click()
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

# Check user không được phân quyền
def check_user_no_auth(driver, wait, share_url):
    driver.get("https://www.google.com/")
    time.sleep(5)
    driver.get(share_url)
    return

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
    print("done login")
    share_url = get_share_audio_link(driverHost, waitHost)
    check_user_no_auth(driverUser, waitUser, share_url)

   

    





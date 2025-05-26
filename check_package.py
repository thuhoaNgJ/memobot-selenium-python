import login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def go_to_package_page(driver, wait):
    driver.get("https://app.memobot.io/thanh-toan")
    time.sleep(5)  # wait for the package page to load

def package_upload_file(driver, wait):
    go_to_package_page(driver, wait)
    package_file = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='content_info']//span[1])[2]")))
    print("Số file đã upload của user là: ", package_file.text)
    login.upload_file(driver, wait)

    return

if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    # Khởi tạo 2 trình duyệt
    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    login.check_login(driver, wait, email, password)
    package_upload_file(driver, wait)

import math
import login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def go_to_package_page(driver):
    driver.get("https://app.memobot.io/thanh-toan")
    time.sleep(5)  # wait for the package page to load

def check_package(driver, wait):
    go_to_package_page(driver)
    # check package before upload file
    print("-------Kiểm tra gói package của user hiện tại-------")
    before_package_file = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='content_info']//span[1])[2]")))
    print("Số file đã upload của user hiện tại là: ", before_package_file.text)
    before_package_minutes = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='content_info']//span[1])[3]")))
    print("Số phút đã sử dụng của user hiện tại là: ", before_package_minutes.text)    
    before_package_storage_hour = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='content_info']//span[1])[4]")))
    print("Thời gian sử dụng của user hiện tại là: ", before_package_storage_hour.text)

    #upload file
    driver.get("https://app.memobot.io")
    audio_path = "/Users/apple/Documents/memobot/Vais memobot/audio file/Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24.mp3"
    audio_upload_name = "Tác hại của màn hình điện tử đối với trẻ nhỏ ｜ VTV24" #get the exactly name of the audio after successfully
    login.upload_file(driver, wait, "Tiếng Việt", audio_path, audio_upload_name)
    time.sleep(20)  # wait for the upload to complete
    print("Đã upload file thành công")
    lenth_audio = wait.until(EC.presence_of_element_located((By.XPATH, 
                "body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) "
                "> div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) "
                "> div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) "
                "> div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > span:nth-child(2)"
                )))
    print("Thời gian của audio đã upload là: ", lenth_audio.text)

    #check package after upload file
    print("-------Kiểm tra gói package sau khi upload file-------")
    go_to_package_page(driver) 
    after_package_file = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='content_info']//span[1])[2]")))
    print("Số file đã upload của user sau khi upload file là: ", after_package_file.text)
    after_package_minutes = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='content_info']//span[1])[3]")))
    print("Số phút đã sử dụng của user sau khi upload file là: ", after_package_minutes.text)    
    after_package_storage_hour = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='content_info']//span[1])[4]")))
    print("Số giờ lưu trữ của user sau khi upload file là: ", after_package_storage_hour.text)
    if int(after_package_file.text) == int(before_package_file.text) + 1:
        print("✅ Số file upload đã tăng lên 1 sau khi upload file thành công")
    else:
        print("❌ Số file upload không tăng lên 1 sau khi upload file")
    if int(after_package_minutes.text) == math.ceil(int(before_package_minutes.text) + int(lenth_audio.text) / 60):
        print("✅ Số phút sử dụng đã tăng lên sau khi upload file thành công")
    else:
        print("❌ Số phút sử dụng không tăng lên sau khi upload file")

if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    login.check_login(driver, wait, email, password)
    check_package(driver, wait)

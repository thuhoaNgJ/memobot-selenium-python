from api import login
import check_login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def delete_audio():
    login.go_to_page(driver, "https://app.memobot.io/")
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


if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    check_login.check_login(driver, wait, email, password)
    # check xoá audio đầu tiên
    delete_audio()



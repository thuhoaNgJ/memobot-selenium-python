import check_login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def search_audio(driver, wait, search_input):
    check_login.go_to_page(driver, "https://app.memobot.io/")
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

def go_to_audio_by_search(driver, wait, search_input):
    driver.get("https://app.memobot.io/")
    time.sleep(10)
    search_audio(driver, wait, search_input)
    audio_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='audio_title']")))
    audio_titles[0].click()
    time.sleep(5)

def filter_audio_by_date():
    check_login.go_to_page(driver, "https://app.memobot.io/")
    try:
        date_filter_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Đến ngày')]")))
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    check_login.check_login(driver, wait, email, password)

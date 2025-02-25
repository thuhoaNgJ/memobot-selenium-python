from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setupWebdriver():
    # Set up the Chrome driver with automatic updates
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    
    # open a webpage
    driver.get("https://app.memobot.io/")
    # wait = WebDriverWait(driver, 10)
    time.sleep(10)
    return driver
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))

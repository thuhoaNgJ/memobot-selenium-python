from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setupWebdriver():
    # Set up the Chrome driver with automatic updates
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    # open a webpage
    driver.get("https://thicong-nhaplieu.aai.com.vn/v2/login")
    time.sleep(5)
    print("DONE setup")
    return driver


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def setupWebdriver():
    # Set up the Chrome driver with automatic updates
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    
    # open a webpage
    driver.get("https://app.memobot.io/")
    time.sleep(10)
    return driver


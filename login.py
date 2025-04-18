import setupDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import json
import time
import os

driver = setupDriver.setupWebdriver()
wait = WebDriverWait(driver, 10)

def check_login(email, password):
    login_by_account_linktext = driver.find_element(
        By.XPATH, "//span[contains(text(),'Đăng nhập bằng tài khoản được cấp')]")
    login_by_account_linktext.click()
    wait.until(EC.presence_of_element_located((
        By.XPATH, "//input[@placeholder='Nhập email hoặc số điện thoại']"
    )))

    input_email = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Nhập email hoặc số điện thoại']")
    input_password = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Nhập mật khẩu']")
    login_btn = driver.find_element(By.XPATH, "(//span[@class='n-button__content'][contains(text(),'Đăng nhập')])[1]")

    input_email.send_keys(email)
    input_password.send_keys(password)
    login_btn.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='bubble flex items-center']")))
    print("DONE login")

email_plus = "hoanguyencheck@gmail.com"
password_plus = "123456"

check_login(email_plus, password_plus)






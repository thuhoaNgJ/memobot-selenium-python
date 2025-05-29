import setupDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def check_login(driver, wait, email, password):
    input_email = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]')
    input_password = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Mật khẩu"]')
    login_btn = driver.find_element(By.ID, 'web-login')

    input_email.send_keys(email)
    input_password.send_keys(password)
    login_btn.click()
    time.sleep(5)

    # Close the promotion image
    try:
        # Wait for the promotion image to appear (optional: adjust timeout)
        promotion_img = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='promotion']"))
        )
        print("Promotion image is visible. Attempting to close the dialog.")

        # Click the promotion dialog close button
        promotion_close_btn = driver.find_element(By.CSS_SELECTOR, "div.dialog-promotion div.el-dialog__wrapper")
        promotion_close_btn.click()
        print("Promotion dialog closed successfully.")

    except Exception as e:
        print("Promotion image not found or already closed. Continuing execution.")

    # Close the notification popup
    try:
        # Wait for the notification popup to appear (optional: adjust timeout)
        notify_popup = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="el-message-box__title"]'))
        )
        print("Notification popup is visible. Attempting to close the popup.")

        # Click the notification popup close button
        notify_close_btn = driver.find_element(By.XPATH, '//button[@class="el-message-box__headerbtn"]')
        notify_close_btn.click()
        print("Notification popup closed successfully.")

    except Exception as e:
        print("Notification popup not found or already closed. Continuing execution.")

    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.pack-container')))
    print("login done")


def go_to_page(driver, url):
    current_url = driver.current_url
    # Check if the URL does not contain the specified text
    if url not in current_url:
        driver.get(url)  # Navigate to the URL
        print(f"Redirected to {url}")
    else:
        print("Already on the correct page, continuing execution.")

if __name__ == "__main__":
    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 10)
    options = Options()

    email_plus = "memo17@mailinator.com"
    password_plus = "Abcd@12345"
    check_login(driver, wait, email_plus, password_plus)


 







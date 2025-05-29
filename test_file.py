import check_login
import setupDriver

from selenium.webdriver.support.ui import WebDriverWait


def function():
    pass

if __name__ == "__main__":
    email= 'memo17@mailinator.com'
    password = 'Abcd@12345'

    # Khởi tạo trình duyệt
    driver = setupDriver.setupWebdriver()
    wait = WebDriverWait(driver, 15)

    check_login.check_login(driver, wait, email, password)

    # Gọi hàm function
    function()
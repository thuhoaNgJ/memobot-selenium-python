import login
import setupDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pyperclip

#User host setup authorization for audio
def search_audio(driver, wait, search_input):
    audio_text = "Tác hại của việc sử dụng quá nhiều internet và thiết bị thông minh, đặc biệt là với trẻ em và thanh thiếu niên"
    page_text = driver.find_element(By.TAG_NAME, "body").text
    # print("page text: "+ page_text)
    if audio_text not in page_text:
        driver.get("https://app.memobot.io/")
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

def get_share_audio_link(driver, wait):
    search_audio(driver, wait, "internet")
    share_function_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='share_transcript'][1]")))
    share_function_btn.click()
    time.sleep(5)
    copy_button = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(),'Sao chép liên kết')]")
    ))
    time.sleep(5)
    copy_button.click()
    share_url = pyperclip.paste()
    print("✅ URL đã copy là:", share_url)
    print("done function get_share_audio_link")
    return share_url

def setup_shared_user(driver, wait, permission_option):
    driver.get("https://app.memobot.io/")
    time.sleep(10)  # wait for the page to load
    print("Starting to set up shared user permissions...")
    search_audio(driver, wait, "internet")
    share_function_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='share_transcript'][1]")))
    share_function_btn.click()
    time.sleep(5)
    copy_button = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(),'Sao chép liên kết')]")
    ))

    auth_dropdown_options = driver.find_element(By.CSS_SELECTOR, '.el-dropdown-link.el-dropdown-selfdefine')
    auth_dropdown_options.click()
    time.sleep(2) 

    shared_chosen_option = f"(//li[@class='el-dropdown-menu__item'][contains(text(),'{permission_option}')])[1]"

    permission_element = wait.until(
        EC.presence_of_element_located((By.XPATH, shared_chosen_option))
    )
    permission_element.click()
    print(f"Đã chọn quyền chia sẻ: {permission_option}")
    time.sleep(5)  # đợi hệ thống lưu quyền
    copy_button.click()

def setup_shared_user_by_email(driver, wait, email, auth_user):
    driver.get("https://app.memobot.io/")
    permission_option = "Chỉ những người đùng được mời"
    setup_shared_user(driver, wait, permission_option)
    email_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "(//input[contains(@placeholder,'Nhập email để chia sẻ...')])[1]")))
    email_input.send_keys(email)
    time.sleep(5)  # wait for the email input to be filled

    # Click the dropdown to select the authorization option
    dropdown_auth_option = driver.find_element(By.XPATH, "//div[@class='mt-4']//div[@class='el-dropdown']")
    dropdown_auth_option.click()
    time.sleep(3)  # wait for the dropdown to open
    # auth_option = wait.until(
    #     EC.presence_of_element_located((By.XPATH, 
    #         "//ul[@id='dropdown-menu-5084']//li[contains(@class,'el-dropdown-menu__item')][contains(text(),'Chỉ xem')]"
    # )))
    auth_option = wait.until(
        EC.presence_of_element_located((By.XPATH, 
            f"//li[contains(text(),'{auth_user}')]"
        )))

    auth_option.click()
    time.sleep(2)  # wait for the option to be selected
    save_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Chia sẻ và sao chép liên kết')]")))
    save_button.click()
    print(f"✅ Đã chia sẻ audio với email: {email} và quyền truy cập là: {auth_user}")
        
#  CHECK USER AUTHORIZATION
# Check user không được phân quyền
def check_user_no_auth(driver, wait, share_url):
    driver.get(share_url)
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "img[src='/memobot-v2/logo-memo.png']")))
    page_text = driver.find_element(By.TAG_NAME, "body").text
    if "Bạn không có quyền truy cập trang này" in page_text:
        print("🚫User chưa được chia sẻ không có quyền xem audio này.")
    else:
        print("✅User có quyền truy cập.")

# check tất cả user có quyền xem
def check_user_only_see(driver, wait, share_url):
    driver.get(share_url)
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "img[src='/memobot-v2/logo-memo.png']")))

    element = driver.find_element(By.CSS_SELECTOR, "div[contenteditable]")  

    # Lấy giá trị thuộc tính
    contenteditable_value = element.get_attribute("contenteditable")

    page_text = driver.find_element(By.TAG_NAME, "body").text
    #check the audio's name in the page text
    if ("internet" in page_text) and contenteditable_value == "false":
        print("✅User có quyền truy cập và chỉ có thể xem audio này.")
    else:
        print("🚫User chưa được chia sẻ không có quyền xem audio này.")

# check tất cả user có quyền xem và edit
def check_user_edit(driver, wait, share_url):
    driver.get(share_url)
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "img[src='/memobot-v2/logo-memo.png']")))

    element = driver.find_element(By.CSS_SELECTOR, "div[contenteditable]") 

    # Lấy giá trị thuộc tính
    contenteditable_value = element.get_attribute("contenteditable")

    page_text = driver.find_element(By.TAG_NAME, "body").text
    #check the audio's name in the page text
    if ("internet" in page_text) and contenteditable_value == "true":
        print("✅User có quyền truy cập và có thể chỉnh sửa audio này.")
    else:
        print("🚫User chưa được chia sẻ không có quyền xem audio này.")

if __name__ == "__main__":
    email_host = 'memo17@mailinator.com'
    pass_host = 'Abcd@12345'
    email_user = 'memo16@mailinator.com'
    pass_user = 'Abcd@12345'

    # Khởi tạo 2 trình duyệt
    driverHost = setupDriver.setupWebdriver()
    waitHost = WebDriverWait(driverHost, 15)

    # Đăng nhập tài khoản user1 và user2
    driverUser = setupDriver.setupWebdriver()
    waitUser = WebDriverWait(driverUser, 15)

    login.check_login(driverHost, waitHost, email_host, pass_host)
    login.check_login(driverUser, waitUser, email_user, pass_user)

    invite_only_option = "Chỉ những người đùng được mời"
    view_only_option = "Bất kì ai có link đều có thể xem"
    edit_option = "Bất kì ai có link đều có thể xem và chỉnh sửa"

    # Chuyển đến trang audio và lấy link chia sẻ
    share_url = get_share_audio_link(driverHost, waitHost)
    # share = 'https://app.memobot.io/memobot-v2/#!/doc-colab/731e_1747131111581'

    # Check mặc định -> user chưa được phân quyền
    check_user_no_auth(driverUser, waitUser, share_url)

    # Check user chỉ có quyền xem
    setup_shared_user(driverHost, waitHost, view_only_option)
    check_user_only_see(driverUser, waitUser, share_url)

    # Check user có quyền xem và chỉnh sửa
    setup_shared_user(driverHost, waitHost, edit_option)
    check_user_edit(driverUser, waitUser, share_url)

    # Check quyền truy cập cho user cụ thể bằng email

    email_view_only_option = "Chỉ xem"
    email_edit_option = "Chỉnh sửa"
    email_cancel_option = "Hủy truy cập"
    share = 'https://app.memobot.io/memobot-v2/#!/doc-colab/731e_1747131111581'
    # check quyền chỉ xem cho user email
    setup_shared_user_by_email(driverHost, waitHost, email_user, email_view_only_option)
    check_user_only_see(driverUser, waitUser, share)
    # check quyền chỉnh sửa cho user email
    setup_shared_user_by_email(driverHost, waitHost, email_user, email_view_only_option)
    check_user_edit(driverUser, waitUser, share)
    # check quyền hủy truy cập cho user email 
    setup_shared_user_by_email(driverHost, waitHost, email_user, email_cancel_option)
    check_user_no_auth(driverUser, waitUser, share)



   

    





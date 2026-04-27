from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginHandler:
    def __init__(self, browser_controller):
        self.browser = browser_controller
        self.driver = browser_controller.driver
        self.wait = browser_controller.wait

    def handle_login(self):
        print("开始处理登录流程...")
        
        try:
            self._wait_for_login_modal()
            phone_number = self._get_phone_number()
            self._enter_phone_number(phone_number)
            self._check_privacy_agreement()
            self._click_get_verification_code()
            verification_code = self._get_verification_code()
            self._enter_verification_code(verification_code)
            self._click_login_button()
            
            if self._check_login_success():
                print("登录成功！")
                return True
            else:
                print("登录失败，请检查验证码是否正确。")
                return False
                
        except Exception as e:
            print(f"登录过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _wait_for_login_modal(self):
        print("等待登录弹框出现...")
        try:
            phone_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='输入手机号']"))
            )
            print("登录弹框已出现。")
            return phone_input
        except Exception as e:
            print(f"等待登录弹框超时: {e}")
            raise

    def _get_phone_number(self):
        phone_number = input("请输入手机号: ")
        while not self._is_valid_phone_number(phone_number):
            print("手机号格式不正确，请重新输入。")
            phone_number = input("请输入手机号: ")
        return phone_number

    def _is_valid_phone_number(self, phone_number):
        return phone_number and len(phone_number) == 11 and phone_number.isdigit()

    def _enter_phone_number(self, phone_number):
        print(f"正在输入手机号: {phone_number}")
        try:
            phone_input = self.driver.find_element(By.XPATH, "//input[@placeholder='输入手机号']")
            phone_input.clear()
            phone_input.send_keys(phone_number)
            print("手机号输入完成。")
        except Exception as e:
            print(f"输入手机号失败: {e}")
            raise

    def _check_privacy_agreement(self):
        print("正在勾选隐私协议...")
        try:
            privacy_checkbox = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div[3]/div[3]/span/div')
                )
            )
            
            if not privacy_checkbox.is_selected():
                privacy_checkbox.click()
                print("隐私协议已勾选。")
            else:
                print("隐私协议已处于勾选状态。")
        except Exception as e:
            print(f"勾选隐私协议失败: {e}")
            raise

    def _click_get_verification_code(self):
        print("正在点击获取验证码按钮...")
        try:
            get_code_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/label[2]/span')
                )
            )
            get_code_button.click()
            print("获取验证码按钮已点击，请等待短信。")
        except Exception as e:
            print(f"点击获取验证码按钮失败: {e}")
            raise

    def _get_verification_code(self):
        verification_code = input("请输入收到的验证码: ")
        while not self._is_valid_verification_code(verification_code):
            print("验证码格式不正确，请重新输入。")
            verification_code = input("请输入收到的验证码: ")
        return verification_code

    def _is_valid_verification_code(self, code):
        return code and len(code) == 6 and code.isdigit()

    def _enter_verification_code(self, verification_code):
        print(f"正在输入验证码: {verification_code}")
        try:
            code_input = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/label[2]/input')
            code_input.clear()
            code_input.send_keys(verification_code)
            print("验证码输入完成。")
        except Exception as e:
            print(f"输入验证码失败: {e}")
            raise

    def _click_login_button(self):
        print("正在点击登录按钮...")
        try:
            login_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/button')
                )
            )
            login_button.click()
            print("登录按钮已点击，等待页面响应...")
            time.sleep(3)
        except Exception as e:
            print(f"点击登录按钮失败: {e}")
            raise

    def _check_login_success(self):
        print("检查登录状态...")
        try:
            current_url = self.driver.current_url
            if "xiaohongshu.com" in current_url and "login" not in current_url:
                time.sleep(2)
                return True
            return False
        except Exception as e:
            print(f"检查登录状态失败: {e}")
            return False

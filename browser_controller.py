from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowserController:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None

    def init_browser(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()

    def open_url(self, url):
        if not self.driver:
            self.init_browser()
        self.driver.get(url)

    def wait_for_element(self, by, value, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_element_clickable(self, by, value, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def get_current_url(self):
        return self.driver.current_url

    def get_page_source(self):
        return self.driver.page_source

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

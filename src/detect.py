import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from link import *

def detect_xss(driver,url, payloads, headless):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    for payload in payloads:

        driver.get(url)

        input_elements = driver.find_elements(By.CSS_SELECTOR, 'input:not([type="submit"]):not([type="button"]):not([type="reset"]):not([type="hidden"]), textarea')

        for input_index, input_element in enumerate(input_elements):
            input_element.send_keys(payload)
            for inputfill in input_elements:
                if not input_elements.index(input_element) == input_index :
                    inputfill.send_keys("testfill")

        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        time.sleep(1)
        # Wait for the alert to appear
        wait = WebDriverWait(driver, 2)
        alert_present = EC.alert_is_present()(driver)

        if alert_present:
            return payload

        # print(payload+" False")

    driver.quit()

    return None
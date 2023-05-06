import argparse
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# Customized XSS Detector

def detect_xss(url, payloads):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    tested_payloads = 0
    correct_payload = ""
    with tqdm(total=len(payloads), desc="Progress", unit="payload") as pbar:
        for payload in payloads:
            tested_payloads += 1
            pbar.set_postfix({"Payload": payload, "Tested": tested_payloads})
            pbar.update(1)

            driver.get(url)

            input_elements = driver.find_elements(By.CSS_SELECTOR, 'input:not([type="submit"]):not([type="button"]):not([type="reset"]):not([type="hidden"]), textarea')

            for input_element in input_elements:
                input_element.send_keys(payload)

            driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
            time.sleep(1)
            # Wait for the alert to appear
            wait = WebDriverWait(driver, 2)
            alert_present = EC.alert_is_present()(driver)

            if alert_present:
                correct_payload=payload
                break

    driver.quit()

    return correct_payload

def run(url) -> None:
    print("########### XSS Shigeno ⚾ ###########")

    # The list of payloads is a portion of payloads from https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt
    with open('xss-payload-list.txt', 'r') as f:
        payloads: List[str] = f.read().splitlines()

    payload = detect_xss(url, payloads)

    if payload=="":
        print("\nNot vulnerable to XSS")
    else:
        print("\nXSS Detected :"+payload)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Custom Reflected XSS Detector')
    parser.add_argument('-s', '--site', type=str, help='URL of the vulnerable site', required=True)
    args = parser.parse_args()
    run(args.site)

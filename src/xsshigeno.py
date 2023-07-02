import argparse
from detect import *
from link import *

def run(url, headless) -> None:
    print("########### XSS Shigeno ⚾ ###########")

    # The list of payloads is a portion of payloads from https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt
    with open('xss-payload-list.txt', 'r') as f:
        payloads = f.read().splitlines()

    driver = link(headless)
    print("Searching...")
    payload = detect_xss(driver, url, payloads, headless)

    if payload==None:
        print("\nNot vulnerable to XSS")
    else:
        print("\nXSS Detected : "+payload)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Custom Reflected XSS Detector')
    parser.add_argument('-s', '--site', type=str, help='URL of the vulnerable site', required=True)
    parser.add_argument('-b', '--browser', action='store_true', help='Run in browser mode (non-headless)')
    args = parser.parse_args()
    headless= not args.browser
    run(args.site, headless)

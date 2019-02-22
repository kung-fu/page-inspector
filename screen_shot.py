# -*- coding: utf-8 -*-

import os
from selenium import webdriver

# set Chrome Driver path
import chromedriver_binary

import requests
from urllib.parse import urlparse

# TODO 外部ファイルにする
URL = [
    "https://quad.co.jp/",
    "https://www.yahoo.co.jp/",
]
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out/')


def main():
    # TODO マルチプロセスにする？
    for i, url in enumerate(URL):
        status = check_status(url)

        parsed = urlparse(url)
        path = parsed.path.replace('/', '_')
        out = OUT_PATH + "{}-{}-{}.png".format(i, status, path)

        capture(url, out)


def check_status(url):
    r = requests.get(url)
    return r.status_code


def capture(url, out):
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1')
    driver = webdriver.Chrome(options=options)

    # w = driver.execute_script('return document.body.scrollWidth')
    # h = driver.execute_script('return document.body.scrollHeight')

    # Screen size of iPhone X
    w, h = 375, 812

    driver.set_page_load_timeout(15)
    driver.set_window_size(w, h)

    try:
        driver.get(url)
        driver.save_screenshot(out)
    except:
        print("time out")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

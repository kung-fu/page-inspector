# -*- coding: utf-8 -*-

import os
import time

from selenium import webdriver

# set Chrome Driver path
import chromedriver_binary

from urllib.parse import urlparse

import http_status
import screen_size
import user_agent
from stop_watch import stop_watch

IN_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'input/urls.txt')
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/')

TIMEOUT = 60


def main():
    with open(IN_FILE, "r") as f:
        urls = [line.strip() for line in f]

    for i, url in enumerate(urls):
        process_one_url(i, url)


@stop_watch
def process_one_url(i, url):
    try:
        status_code = http_status.check_status(url)
    except Exception as e:
        print(e)
        return

    parsed = urlparse(url)
    path = parsed.path.replace('/', '_')
    out = OUT_PATH + "{}-{}-{}.png".format(i + 1, status_code, path)

    options = set_option(sp=True)
    capture(url, options, out)


def set_option(sp=False):
    options = webdriver.ChromeOptions()
    if sp:
        options.add_argument(user_agent.IPHONE)

    options.add_argument('--headless')
    options.add_argument('--disk-cache=false')

    return options


def capture(url, options, out):
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(TIMEOUT)

    # w = screen_size.HD_LONG.w
    # h = screen_size.HD_LONG.h
    w = screen_size.IPHONE_7_LONG.w
    h = screen_size.IPHONE_7_LONG.h

    try:
        driver.get(url)
        driver.set_window_size(w, 3000)
        time.sleep(1)
        driver.save_screenshot(out)
    except Exception:
        print(out + "time out")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

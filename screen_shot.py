# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from urllib.parse import urlparse
from urllib.request import urlopen
from stop_watch import stop_watch

# set Chrome Driver path
import chromedriver_binary

IN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input/urls.txt')
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/')

USER_AGENT_IPHONE = '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) ' \
                    'AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1'

# Screen size of iPhone X
SCREEN_W, SCREEN_H = 375, 812


def main():
    # TODO マルチプロセスにする？

    with open(IN_FILE, "r") as f:
        urls = [line.strip() for line in f.readlines()]

    for i, url in enumerate(urls):
        process_one_url(i, url)


@stop_watch
def process_one_url(i, url):
    status_code = check_status(url)

    parsed = urlparse(url)
    path = parsed.path.replace('/', '_')
    out = OUT_PATH + "{}-{}-{}.png".format(i, status_code, path)

    capture(url, out)


def check_status(url):
    r = urlopen(url)
    return r.getcode()


def capture(url, out):
    options = webdriver.ChromeOptions()
    options.add_argument(USER_AGENT_IPHONE)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)
    driver.set_window_size(SCREEN_W, SCREEN_H)

    try:
        driver.get(url)
        driver.save_screenshot(out)
    except:
        print("time out")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

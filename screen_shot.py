# -*- coding: utf-8 -*-

import os

from selenium import webdriver
# set Chrome Driver path
import chromedriver_binary

from urllib.parse import urlparse
from urllib.request import urlopen
import urllib.error

import user_agent
from stop_watch import stop_watch

IN_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'input/urls.txt')
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output/')

# Screen size of iPhone 7
SCREEN_W, SCREEN_H = 375, 668

TIMEOUT = 60


def main():
    with open(IN_FILE, "r") as f:
        urls = [line.strip() for line in f]

    for i, url in enumerate(urls):
        process_one_url(i, url)


@stop_watch
def process_one_url(i, url):
    try:
        status_code = check_status(url)
    except Exception as e:
        print(e)
        return

    parsed = urlparse(url)
    path = parsed.path.replace('/', '_')
    out = OUT_PATH + "{}-{}-{}.png".format(i + 1, status_code, path)

    capture(url, out)


def check_status(url):
    try:
        r = urlopen(url)
        return r.getcode()
    except urllib.error.HTTPError as e:
        print(e.reason)
        return e.code
    except urllib.error.URLError as e:
        print(e.reason)
        raise e
    except Exception as e:
        raise e


def capture(url, out):
    options = webdriver.ChromeOptions()
    options.add_argument(user_agent.IPHONE)
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(TIMEOUT)
    driver.set_window_size(SCREEN_W, SCREEN_H)

    try:
        driver.get(url)
        driver.save_screenshot(out)
    except Exception:
        print(out + "time out")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

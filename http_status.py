# -*- coding: utf-8 -*-

from urllib.request import urlopen
import urllib.error


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

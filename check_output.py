# -*- coding: utf-8 -*-

import glob


def check_lack():
    files = glob.glob("output/*")
    line_numbers = sorted(
        [int(file.split('/')[1].split('-')[0]) for file in files])

    k = None
    for j in line_numbers:
        if j == 1:
            k = j
            continue

        if j != k + 1:
            print(k + 1)
        k = j


def check_status():
    files = glob.glob("output/*")
    line_numbers = {
        file.split('/')[1].split('-')[0]: file.split('/')[1].split('-')[1]
        for file in files
    }

    for k, v in line_numbers.items():
        if v != "200":
            print("{} : {}".format(k, v))


if __name__ == "__main__":
    check_status()

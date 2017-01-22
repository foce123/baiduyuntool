#coding:utf-8

from __future__ import division
import sys
import time


def view_bar(num, total):
    rate = num/total
    rate_num = int(rate * 100)
    r = '\r[%s%s]%d%%' % ("=" * num, " " * (50 - num), rate_num,)
    sys.stdout.write(r)
    sys.stdout.flush()


if __name__ == '__main__':
    for i in range(0, 51):
        time.sleep(0.1)
        view_bar(i, 50)

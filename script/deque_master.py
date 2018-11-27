#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from multiprocessing import Manager
from multiprocessing import Queue
import sys
sys.path.append("../")
from conf import serverconf


class FileFlush(object):
    def __init__(self):
        # self.slot = Manager().dict()
        self.slot = dict()
        self.lock = threading.Lock()
        self.fd = None

    def write_file(self):
        while 1:
            self.fd = open(serverconf.LOG_FIL, "a+")
            # print self.slot
            for topic in self.slot.keys():
                buf = self.slot[topic]["que"]
                if buf.qsize() > 20480 or self.slot[topic]["con"] > 15:
                    while 1:
                        try:
                            temp = buf.get(timeout=0.003)
                            self.fd.write(temp)
                        except:
                            break
                else:
                    self.slot[topic]["con"] += 1
            print "finish write"
            self.fd.close()
            time.sleep(0.5)

    def get_buffer(self, topic):
        if topic not in self.slot:
            self.lock.acquire()
            self.slot[topic] = dict()
            self.slot[topic]["que"] = Queue(maxsize=1024 * 50)
            self.slot[topic]["con"] = 0
            self.lock.release()

        return self.slot[topic]["que"]

    def test(self):
        # fil_wri = threading.Thread(target=self.write_file)
        #
        # for loop in xrange(4):
        #     addr = self.get_buffer(str(loop))
        #     for each in xrange(50000):
        #         addr.put(str(each))
        # fil_wri.start()
        # time.sleep(3)
        # self.get_buffer("233")
        # print "finish"
        pass

    def run(self):
        fil_wri = threading.Thread(target=self.write_file)
        fil_wri.start()
        print "File queue finish initialization."


if __name__ == "__main__":
    f = FileFlush()
    f.test()

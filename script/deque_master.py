#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from multiprocessing import Manager
from multiprocessing import Queue
from multiprocessing import Process
from multiprocessing import Lock
import sys
sys.path.append("../")
from conf import serverconf


class FileFlush(object):
    def __init__(self):
        # self.slot = Manager().dict()
        self.slot = dict()
        self.lock = Lock()
        self.fd = None

    def write_file(self):
        while 1:
            self.fd = open(serverconf.LOG_FIL, "a+")
            print self.slot
            for topic in self.slot.keys():
                buf = self.slot[topic]["que"]
                buf.qsize()
                if buf.qsize() > 10240 or self.slot[topic]["con"] > 6:
                    while 1:
                        try:
                            temp = buf.get(timeout=0.003)
                            self.fd.write(temp)
                        except:
                            break
                    self.slot[topic]["con"] = 0
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
        # fil_wri = Process(target=self.write_file)
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
        #self.get_buffer("log")
        fil_wri.start()
        print "File queue finish initialization."


if __name__ == "__main__":
    f = FileFlush()
    f.test()

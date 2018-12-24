#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import functools
import sys
import os
import re
import lz4.frame
from struct import pack
from agentnet import NetTransport
sys.path.append("../")
from conf import agentconf


class _CheckPoint(object):
    def __init__(self):
        self.fil = None

    def check_point(self, fd):
        """
        # Recover from the lastest readed.
        :param fd:
        :return:
        """
        fil_name = agentconf.CHECK_POINT_PATH + str(os.fstat(fd.fileno()).st_ino)
        print "check_point", fil_name
        try:
            self.fil = open(fil_name, "r")
            pre_location = self.fil.readline()[:-1]
            if pre_location != "":
                fd.seek(int(pre_location))
                self.fil.close()
        except:
            pass
        self.fil = open(fil_name, "w", buffering=0)
        return

    def flush(self, offset):
        self.fil.seek(0)
        self.fil.write(str(offset) + '\n')

    def stop(self):
        self.fil.close()


class Agent(object):
    def __init__(self):
        self.net = NetTransport()
        self.check = _CheckPoint()

    def time_count(fun):  # fun = world
        #  @functools.wraps(fun) 的作用就是保留原函数信息如__name__, __doc__, __module__
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            """
            this is wrapper function
            :param args:
            :param kwargs:
            :return:
            """
            start_time = time.time()
            temp = fun(*args, **kwargs)  # world(a=1, b=2)
            end_time = time.time()
            print("%s函数运行时间为%s" % (fun.__name__, end_time - start_time))
            return temp

        return wrapper

    def hard_link(self):
        log_fil = []
        print "log path setting is ", agentconf.LOG_SET
        for each in agentconf.LOG_SET:
            # loading the log path setup
            path_list = agentconf.LOG_SET[each]["path"]
            rule = agentconf.LOG_SET[each]["rule"]
            topic = each
            check_point_path = agentconf.CHECK_POINT_PATH
            over_time = agentconf.OVER_TIME

            for path in path_list:
                for fil in os.listdir(path):
                    if re.match(rule, fil):
                        fil_name = "".join([path, fil])
                        log_fil.append(fil_name)
                        link_name = "".join([check_point_path, str(os.stat(fil_name).st_ino), ".link"])
                        check_point_name = "".join([check_point_path, str(os.stat(fil_name).st_ino)])
                        if os.path.exists(link_name):
                            # Delect the link when the link over OVER_TIME without modify and Agent push all data.
                            if time.time() - os.stat(fil_name).st_mtime > over_time and os.path.exists(
                                    check_point_name):
                                with open(check_point_name, "r") as f:
                                    temp = f.readline().split("\n")[0]
                                    if temp != "" and os.stat(check_point_name).st_size == int(temp):
                                        os.unlink(link_name)

                        else:
                            print fil_name, link_name
                            os.link(fil_name, link_name)

        return log_fil

    @time_count
    def collect(self, fil_path):
        """
        Collect each log fil by the way such as linux tail.
        :param fil_path: 
        :return: 
        """
        f = open(fil_path, "r")
        self.check.check_point(f)

        while 1:
            data = "".join(f.readlines(32*1024))

            if data != "":
                # Three step to send a data.
                # 1.It must send the length of data to server in 4 bytes long.
                # 2.Just push the data to the server.
                # 3. Flush the check-point. Notice Notice Notice , check-point should be write after send
                #  so that we will not miss any log.
                data = lz4.frame.compress(data)
                self.net.send(pack("i", len(data)))
                self.net.send(data)
                self.check.flush(f.tell())
            else:
                self.check.flush(f.tell())
                self.check.stop()
                f.close()
                self.net.send(pack("i", len("exit")))
                self.net.send("exit")
                print "exit"
                break

    def run(self):
        log_fil = self.hard_link()
        for fil_path in log_fil:
            self.collect(fil_path)


if __name__ == "__main__":
    s = Agent()
    s.run()

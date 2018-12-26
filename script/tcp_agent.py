#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import functools
import sys
import os
import re
import json
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
        fil_path = agentconf.CHECK_POINT_PATH + str(os.fstat(fd.fileno()).st_ino)
        print "check_point", fil_path
        if os.path.exists(fil_path):
            self.fil = open(fil_path, "r")
            pre_location = self.fil.readline()[:-1]
            if pre_location != "":
                fd.seek(int(pre_location))
                self.fil.close()
        self.fil = open(fil_path, "w", buffering=0)
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

    def time_count(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            """
            :param args:
            :param kwargs:
            :return:
            """
            start_time = time.time()
            temp = fun(*args, **kwargs)
            end_time = time.time()
            print("%s函数运行时间为%s" % (fun.__name__, end_time - start_time))
            return temp

        return wrapper

    def hard_link(self):
        log_list = []
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
                        fil_path = "".join([path, fil])
                        link_path = "".join([check_point_path, str(os.stat(fil_path).st_ino), ".link"])
                        check_point_name = "".join([check_point_path, str(os.stat(fil_path).st_ino)])
                        # The hard link life cycle need three element : over time,hard link file, offset file.
                        # That means it will be eight situation appear in logic.
                        # However , the potential situation are as follow.
                        # 1. below over time, hard link and offset doesn't exists.
                        # 2. over over time , hard link and offset doesn't exists.
                        # 3. below over time, hard link and offset is exists.
                        # 4. below over time, hard link dismiss but offset is exists.
                        # 5. over over time, hard link and offset is exists.
                        # 6. over over time, hard link dismiss but offset is exists.

                        # situation 1 and 2
                        if os.path.exists(link_path) == False and os.path.exists(check_point_name) is False:
                            os.link(fil_path, link_path)
                        # situation 4
                        elif os.path.exists(link_path) == False and os.path.exists(check_point_name) == True and (time.time() - os.stat(fil_path).st_mtime) < over_time:
                            os.remove(check_point_name)
                            os.link(fil_path, link_path)
                        # situation 5
                        elif os.path.exists(link_path) == True and os.path.exists(check_point_name) == True and (time.time() - os.stat(fil_path).st_mtime) > over_time:
                            # unlink till the log collection finish.
                            with open(check_point_name, "r") as f:
                                temp = f.readline().split("\n")[0]
                                if temp != "" and os.stat(check_point_name).st_size == int(temp):
                                    os.unlink(link_path)
                                    continue
                        # situation 6
                        elif os.path.exists(link_path) == False and os.path.exists(check_point_name) == True and (time.time() - os.stat(fil_path).st_mtime) > over_time:
                            continue
                        log_list.append((link_path, topic))
        return log_list

    @time_count
    def collect(self, fil_path, topic):
        """
        :param fil_path: The log path .
        :param topic: The topic of the log.
        :return:
        """
        f = open(fil_path, "r")
        self.check.check_point(f)

        while 1:
            offset = f.tell()
            data = "".join(f.readlines(32*1024))

            if data != "":
                data = lz4.frame.compress(data)

                # Three step to send a data.
                # 1.It must send the length of data to server in 4 bytes long.
                # 2.Just push the data to the server.
                # 3. Flush the check-point. Notice Notice Notice , check-point should be write after send
                #  so that we will not miss any log.
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
        log_list = self.hard_link()
        for each in log_list:
            print each
            self.collect(*each)


if __name__ == "__main__":
    s = Agent()
    s.run()

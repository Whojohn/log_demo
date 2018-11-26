#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import functools
import sys
import os
import re
from agentnet import NetTransport
sys.path.append("../")
from conf import agentconf


class _CheckPoint(object):
    def __init__(self):
        self.fil = None

    def check_point(self, fd):
        """
        #Recover from the lastest readed.
        :param fd:
        :return:
        """
        fil_name = agentconf.CHECK_POINT_PATH+str(os.fstat(fd.fileno()).st_ino)
	print "check_point",fil_name
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

    def time_count( fun):  # fun = world
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
	print "check_path",agentconf.CHECK_PATH
        for fil in os.listdir(agentconf.CHECK_PATH):
            if re.match(agentconf.CHECK_RULE, fil):
                fil_name = "".join([agentconf.CHECK_PATH, fil])
                log_fil.append("".join([agentconf.CHECK_PATH, fil]))
                link_name = "".join([agentconf.CHECK_POINT_PATH, str(os.stat(fil_name).st_ino), ".link"])
                checkpoint_name = "".join([agentconf.CHECK_POINT_PATH, str(os.stat(fil_name).st_ino)])
                if os.path.exists(link_name):
                    # Delect the link when the link over OVER_TIME without modify and Agent push all data.
                    if time.time() - os.stat(fil_name).st_mtime > agentconf.OVER_TIME and os.path.exists(checkpoint_name):
                        with open(checkpoint_name, "r") as f:
                            temp = f.readline().split("\n")[0]
			    if temp != "" and os.stat(checkpoint_name).st_size == int(temp):
                                os.unlink(link_name)

                else:
                    #print fil_name, link_name
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

        # Avoid the overload the agent cpu and disk.
        # __loop = 0
        while 1:
            temp = f.readline()
            #print temp[:-1]

            # Avoid the overload the agent cpu and disk.
            # if __loop%1000 == 0:
            #   time.sleep(0.003)

            if temp != "":
                # Push the data to the server.
                self.net.send(temp)
                # Flush the check-point
                self.check.flush(f.tell())
            else:
                self.check.flush(f.tell())
                self.check.stop()
                f.close()
                self.net.send("exit")
                break

    def run(self):
        log_fil = self.hard_link()
	for fil_path in log_fil:
            self.collect(fil_path)

if __name__ == "__main__":
    s = Agent()
    s.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
sys.path.append("../")
from conf import agentconf


def hard_link():
    log_fil = []
    for fil in os.listdir(agentconf.CHECK_PATH):
        if re.match(agentconf.CHECK_RULE, fil):
            log_fil.append("".join([agentconf.CHECK_PATH, r"/", fil]))
            link_name = "".join([agentconf.CHECK_POINT_PATH, fil, ".link"])
            checkpoint_name = "".join([agentconf.CHECK_POINT_PATH, str(os.stat(fil).st_ino)])
            if os.path.exists(link_name):
                # Delect the link when the link over OVER_TIME without modify and Agent push all data.
                if time.time() - os.stat(fil).st_mtime > agentconf.OVER_TIME and os.path.exists(checkpoint_name):
                    with open(checkpoint_name, "r") as f:
                        if os.stat(checkpoint_name).st_size == int(f.readline().split("\n")[0]):
                            os.unlink(link_name)

            else:
                # os.link(fil, link_name)
                pass
    return log_fil

if __name__ == "__main__":
    print hard_link()

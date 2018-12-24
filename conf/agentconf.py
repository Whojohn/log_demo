#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup the Agent network
SERVER_IP = "127.0.0.1"
PORT = 9999

CHECK_POINT_PATH = "../check_point/"

# Key is topic valude is the path way and rule is the regex rule.
LOG_SET = {
            "log3":{"rule":".*log$","path":["../../"]},
            "log4":{"rule":".*log$","path":["../"]},
              }

# The hard link live time.If the log file don not change over the time and push all data it will
# delet the log file hard link.
OVER_TIME = 86400

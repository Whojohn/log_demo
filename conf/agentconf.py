#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup the Agent network
SERVER_IP = "127.0.0.1"
PORT = 9999

CHECK_POINT_PATH = "../check_point/"

# setup the Agent search which log dir and search which log by regex.
CHECK_RULE = ".*log$"
CHECK_PATH = "../../"
TOPIC = "log"

# The hard link live time.If the log file don not change over the time and push all data it will
# delet the log file hard link.
OVER_TIME = 86400

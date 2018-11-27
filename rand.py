#!/usr/bin/env python
# -*- coding: utf-8 -*-
with open("log", "w") as f:
    for each in xrange(300):
        f.write(str(each)+'\n')
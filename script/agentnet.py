#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
sys.path.append("../")
from conf import agentconf


class NetTransport(object):
    def __init__(self):
        self.__open_socket()
        self.label = 0

    def __open_socket(self):
        ip_port = (agentconf.SERVER_IP, agentconf.PORT)
        self.sk = socket.socket()
        self.sk.connect(ip_port)

    def __close_socket(self):
        #self.sk.shutdown(2)
        self.sk.close()

    def send(self, data):
        if self.label ==1:
            self.__open_socket()
            self.label = 0
        self.sk.sendall(data)
        if data == 'exit':
            self.__close_socket()
            self.label = 1
            print "break"
            return
        #try:
            #data = self.sk.recv(1024)
        #except:
            #pass
        #print 'receive:', data

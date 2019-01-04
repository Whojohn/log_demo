# !/usr/bin/env python
# -*- coding:utf-8 -*-
import SocketServer
import sys
import deque_master
import lz4.frame
import time
import json
from struct import unpack
sys.path.append("../")
from conf import serverconf


class MyServer(SocketServer.BaseRequestHandler ,object):
    def __init__(self, *args, **kw):
        super(MyServer, self).__init__(*args, **kw)

    def recv(self, conn, length):
        data = ""
        pre_len = 0
        amount = 0
        while len(data) < length:
            data += conn.recv(length-len(data))
            if pre_len == len(data):
                time.sleep(0.05)
                amount += 1
                if amount > 50:
                    raise IOError
                    break
        return data

    def handle(self):
        # print self.request,self.client_address,self.server
        fd = False 
        conn = self.request
        # print "get fd ok"
        while 1:
            try:
                meat_len = unpack("i", self.recv(conn, 4))[0]
                meat_data = json.loads(self.recv(conn, meat_len))
                data = self.recv(conn, meat_data["length"])
            except IOError:
                print "agent network error happend"
                break
            if data == 'exit':
                print "quiet"
                break
            else:
                if fd == False: 
                    fd = self.server.buf.get_buffer(meat_data["topic"])
                # fd.put(lz4.frame.decompress(data))
                fd.put(data)


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer((serverconf.IP, serverconf.PORT), MyServer)
    server.buf = deque_master.FileFlush()
    server.buf.run()
    print dir(server.buf)
    server.serve_forever()

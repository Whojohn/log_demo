# !/usr/bin/env python
# -*- coding:utf-8 -*-
import SocketServer
import sys
import deque_master
import lz4.frame
from struct import unpack
sys.path.append("../")
from conf import serverconf


class MyServer(SocketServer.BaseRequestHandler ,object):
    def __init__(self, *args, **kw):
        super(MyServer, self).__init__(*args, **kw)

    def recv(self, conn, length):
        data = ""
        while len(data)<length:
            data += conn.recv(length-len(data))
        return data

    def handle(self):
        # print self.request,self.client_address,self.server
        fd = self.server.buf.get_buffer("log")
        conn = self.request
        # print "get fd ok"
        server_log=open("ser","w")
        while 1:
            data_len = unpack("i", self.recv(conn, 4))[0]
            data = self.recv(conn, data_len)
            if data == 'exit':
                print "quiet"
                break
            else:
                fd.put(lz4.frame.decompress(data))
                # fd.put(data)




if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer((serverconf.IP, serverconf.PORT), MyServer)
    server.buf = deque_master.FileFlush()
    server.buf.run()
    print dir(server.buf)
    server.serve_forever()

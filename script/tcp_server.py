# !/usr/bin/env python
# -*- coding:utf-8 -*-
import SocketServer
import sys
import deque_master
from struct import unpack
sys.path.append("../")
from conf import serverconf


class MyServer(SocketServer.BaseRequestHandler ,object):
    def __init__(self, *args, **kw):
        super(MyServer, self).__init__(*args, **kw)

    def handle(self):
        # print self.request,self.client_address,self.server
        fd = self.server.buf.get_buffer("log")
        conn = self.request
        # print "get fd ok"
        server_log=open("ser","w")
        while 1:
            data_len = unpack("i", conn.recv(4))[0]
            data = conn.recv(data_len)
            if data == 'exit':
                print "quiet"
                break
            else:
                fd.put(data.decode("zlib"))
                # fd.put(data)




if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer((serverconf.IP, serverconf.PORT), MyServer)
    server.buf = deque_master.FileFlush()
    server.buf.run()
    print dir(server.buf)
    server.serve_forever()

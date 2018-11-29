# !/usr/bin/env python
# -*- coding:utf-8 -*-
import SocketServer
import sys
import deque_master

sys.path.append("../")
from conf import serverconf


class MyServer(SocketServer.BaseRequestHandler ,object):
    def __init__(self, *args, **kw):
        super(MyServer, self).__init__(*args, **kw)

    def handle(self):
        # print self.request,self.client_address,self.server
        Flag = True
        fd = self.server.buf.get_buffer("log")
        conn = self.request
        print "get fd ok"
        while Flag:
            data = conn.recv(32*1024)
            if data == 'exit' or data == "":
                print "quiet"
                Flag = False
                break
                # else:
                #     conn.sendall('请输入.')
            fd.put(data) 


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer((serverconf.IP, serverconf.PORT), MyServer)
    server.buf = deque_master.FileFlush()
    server.buf.run()
    print dir(server.buf)
    server.serve_forever()

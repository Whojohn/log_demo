#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import SocketServer
#
# class MyTCPHandler(SocketServer.BaseRequestHandler,object):
#     def __init__(self, *args, **kw):
#         super(MyTCPHandler, self).__init__(*args, **kw)
#
#
#     def handle(self):
#         # self.request is the TCP socket connected to the client
#         self.data = self.request.recv(1024).strip()
#         print "{} wrote:".format(self.client_address[0])
#         print self.data
#         # just send back the same data, but upper-cased
#         self.request.sendall("1")
#
#
# if __name__ == "__main__":
#     HOST, PORT = "localhost", 9999
#
#     # Create the server, binding to localhost on port 9999
#     server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
#
#     # Activate the server; this will keep running until you
#     # interrupt the program with Ctrl-C
#     server.serve_forever()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import SocketServer
import sys
sys.path.append("../")
from conf import serverconf


class MyServer(SocketServer.BaseRequestHandler,object):
    def __init__(self, *args, **kw):
        super(MyServer, self).__init__( *args, **kw)

    def handle(self):
        # print self.request,self.client_address,self.server
        conn = self.request
        Flag = True
        while Flag:
            data = conn.recv(1024)
            print data
            if data == 'exit':
                Flag = False
		break
            else:
                conn.sendall('请输入.')


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer((serverconf.IP,serverconf.PORT),MyServer)
    server.serve_forever()

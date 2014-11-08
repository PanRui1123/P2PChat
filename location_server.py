#!/usr/bin/env python
# coding: utf-8

import json
import SocketServer

__author__ = {
    'name':'Rui Pan',
    'email':'joshuapanrui@live.cn',
}



class LocationHandler(SocketServer.BaseRequestHandler):
    _BUF_SIZE = 1024

    def handle(self):
        users = self.server.active_users

        data = self.request.recv(LocationHandler._BUF_SIZE)
        user_cmd = json.loads(data.strip())

        #print("# server recv: %s" % user_cmd)

        if user_cmd[0] == 'add':
            users[user_cmd[1]] = user_cmd[2]
        elif user_cmd[0] == 'del' and users.has_key(user_cmd[1]):
            del users[user_cmd[1]]
        else:
            pass

        self.request.sendall(json.dumps(users))

class LocationServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address):
        SocketServer.TCPServer.__init__(self, server_address, LocationHandler)
        self.active_users = {}

def main():
    addr = ("",9026)

    server = LocationServer(addr)
    server.serve_forever()

if __name__ == '__main__':
    main()

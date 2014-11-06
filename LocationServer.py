import json
import traceback
import SocketServer

__author__ = {	'name':'Rui Pan',
'email':'joshuapanrui@live.cn',
}


g_active_user = {}

class LocationHandler(SocketServer.BaseRequestHandler):
	m_bufSize = 1024

	def handle(self):
		global g_active_user
		while True:
			try:

				user_cmd = json.loads(self.request.recv(LocationHandler.m_bufSize).strip())

				if user_cmd[0] == 'add':
					g_active_user[user_cmd[1]] = user_cmd[2]
				elif user_cmd[0] == 'del':
					del g_active_user[user_cmd[1]]
				else:
					pass

				toSend = json.dumps(g_active_user)
				self.request.sendall(toSend)
				
				self.request.close()

				break
			except:

				traceback.print_exc()
				break


def main():
	addr = ("",9026)

	server = SocketServer.TCPServer(addr, LocationHandler)
	server.serve_forever()

if __name__ == '__main__':
	main()
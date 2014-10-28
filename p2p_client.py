import threading
import sys
import socket
import time
import Tkinter

root_window = 0
username = 0
passwd = 0
name_addr_dic = {}
name_socket_dic = {}
locationServerAddr = (123,456)


__author__ = {	'name':'Rui Pan',
'email':'joshuapanrui@live.cn',
'phone':'13684027112',
'stunum':'201421060430'}

class CReceiver(threading.Thread):
	def __init__(self, Socket, ChatBoard, chatWndow, Remotename):
		self.m_socket = Socket
		self.m_chatboard = ChatBoard
		self.m_remote = Remotename
		self.chatwindow = chatWndow

	def run(self):
		while not self.thread_stop:
			recv_msg = self.m_socket.recv(1024)
			if recv_msg == "":
				print 'remote is closed'

				self.chatwindow.destroy()
				name_socket_dic[remote].close()
				name_socket_dic[remote] = None
				self.stop()
			else:
				self.m_chatboard.insert(Tkinter.CURRENT,self.m_remote + time.strftime(' %m-%d-%H %I:%M:%S\n',time.localtime(time.time())), 'blue')
				self.m_chatboard.insert(Tkinter.CURRENT,recv_msg)				

class CListener(threading.Thread):
	def __init__(self):
		self.m_socket = socket.socket(AF_INET, SOCK_STREAM)
		self.default_port = 8888
		while True:
			try:
				self.m_socket.bind(("",self.default_port))
				break;
			except Exception,e:
				self.default_port += 1
		self.m_socket.listen(10)

	def getaddr():
		return (gethostname(),self.default_port)

	def run(self):
		global root_window
		global name_addr_dic
		while(True):
			(conn_socket,addr) = self.m_socket.accept()
			
			if addr == locationServerAddr:
				#update table
				continue

			remotename = ''
			for k in name_addr_dic.keys():
				if name_addr_dic[k] == addr:
					remotename = k
					break

			create_chat_window(remotename)



def on_error(msg):
	print msg

def on_log_up_action(regname , regpasswd):


	print regname.get(),regpasswd.get()

def on_log_up(root):
	print 'log up'
	cWinLogUp = Tkinter.Toplevel(root)
	cWinLogUp.title('Log up')
	cWinLogUp.geometry('400x150')

	regname = Tkinter.StringVar()
	regpasswd = Tkinter.StringVar()
	regname.set('username')
	regpasswd.set('passwd')

	input_name = Tkinter.Entry( cWinLogUp, textvariable = regname, width=40)
	input_key = Tkinter.Entry( cWinLogUp, textvariable = regpasswd, width=40)

	input_key.bind("<Return>", lambda: on_log_up_action(regname, regpasswd))
	input_name.pack(pady = 20, side = Tkinter.TOP)
	input_key.pack(pady = 0, side = Tkinter.TOP)

	bottonname_2 = Tkinter.StringVar()
	bottonname_2.set('Regist')
	confilm_button_2 = Tkinter.Button(cWinLogUp, textvariable = bottonname_2, command =lambda: on_log_up_action(regname, regpasswd))
	confilm_button_2.pack()	


def on_exit():
	print 'exit'
	login_window.destroy()

def sendmessage(text_msg, chatboard, remote):
	global username
	global name_socket_dic
	msg = text_msg.get('1.0',Tkinter.END)
	text_msg.delete(0.0, Tkinter.END)	
	print 'send',msg
	chatboard.insert(Tkinter.CURRENT,username.get() + time.strftime(' %m-%d-%H %I:%M:%S\n',time.localtime(time.time())), 'green')
	chatboard.insert(Tkinter.CURRENT,msg)

	socket = name_socket_dic[remote]
	socket.send(msg)

def on_chat(lb,event):
	global root_window

	remote = lb.get(lb.curselection()) 
	conn = socket.socket(AF_INET, SOCK_STREAM)
	conn.connect(name_addr_dic(remote))
	name_socket_dic[remote] = conn

	return create_chat_window(remote)

def create_chat_window(remote):

	global root_window
	global name_socket_dic

	chat_window = Tkinter.Toplevel(root_window)
	chat_window.title(' chatting with '+ remote)

	frame_left_top = Tkinter.Frame(chat_window, width=380, height=270, bg='white')
	frame_left_center = Tkinter.Frame(chat_window, width=380, height=100, bg='white')
	frame_left_bottom = Tkinter.Frame(chat_window, width=380, height=20)
	frame_right = Tkinter.Frame(chat_window, width=170, height=400, bg='white')

	text_msglist = Tkinter.Text(frame_left_top)
	text_msglist.bind("<KeyPress>", lambda e : "break")	

	text_msg = Tkinter.Text(frame_left_center);
	button_sendmsg = Tkinter.Button(frame_left_bottom, text='send',command= lambda: sendmessage(text_msg, text_msglist, remote))	
	text_msglist.tag_config('green', foreground='#00B800')
	text_msglist.tag_config('blue', foreground='blue')
	
	frame_left_top.grid(row=0, column=0, padx=2, pady=5)
	frame_left_center.grid(row=1, column=0, padx=2, pady=5)
	frame_left_bottom.grid(row=2, column=0)
	frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)
	frame_left_top.grid_propagate(0)
	frame_left_center.grid_propagate(0)
	frame_left_bottom.grid_propagate(0)

	text_msglist.grid()
	text_msg.grid()
	button_sendmsg.grid(sticky=Tkinter.E)

	receiver = CReceiver(name_socket_dic[remote], text_msglist, chat_window, remote)
	receiver.start()

	return chat_window

def on_log_in(login_window, event = None):
	global root_window
	global username
	global passwd	

	print username.get(),passwd.get()

	listener = CListener()
	myaddr = listener.getaddr()
	RegistToLocationServer(myaddr)

	friends = name_addr_dic.keys()

	lb = Tkinter.Listbox(root_window,selectmode = Tkinter.EXTENDED)
	for i in range(len(friends)):
	    lb.insert(Tkinter.END,friends[i])

	lb.bind('<Double-Button-1>',lambda event: on_chat(lb,event))

	lb.pack(side = Tkinter.LEFT)
	root_window.attributes("-alpha",1)
	root_window.attributes("-topmost",1)	

	login_window.destroy()	

	listener.start()

def RegistToLocationServer(myaddr):
	#regist to location server

def main():
	global root_window
	global username
	global passwd

	root_window = Tkinter.Tk()
	root_window.attributes("-alpha",0)
	root_window.title('P2PChat contacts')
	root_window.geometry('200x400')
	login_window = Tkinter.Toplevel(root_window)
	login_window.title('P2PChat Login')
	login_window.geometry('400x150')

	menubar = Tkinter.Menu(login_window)

	log_up = Tkinter.Menu(menubar,tearoff = 0)
	log_up.add_command(label = 'log up', command =lambda: on_log_up(login_window))
	log_up.add_command(label = 'Exit', command = on_exit)
	menubar.add_cascade(label = 'more control',menu = log_up)

	login_window.config(menu = menubar)

	username = Tkinter.StringVar()
	passwd = Tkinter.StringVar()
	username.set('username')
	passwd.set('passwd')

	input_name = Tkinter.Entry( login_window, textvariable = username, width=40)
	input_key = Tkinter.Entry( login_window, textvariable = passwd, width=40)

	input_key.bind("<Return>", lambda event: on_log_in(login_window,event))
	input_name.pack(pady = 20, side = Tkinter.TOP)
	input_key.pack(pady = 0, side = Tkinter.TOP)

	bottonname = Tkinter.StringVar()
	bottonname.set('confilm')
	confilm_button = Tkinter.Button(login_window, textvariable = bottonname, command =lambda: on_log_in(login_window))
	confilm_button.pack(padx = 100,side = Tkinter.LEFT)

	bottonname_2 = Tkinter.StringVar()
	bottonname_2.set('Regist')
	confilm_button_2 = Tkinter.Button(login_window, textvariable = bottonname_2, command =lambda: on_log_up(root = login_window))
	confilm_button_2.pack(side = Tkinter.LEFT)


	root_window.mainloop()

if __name__ == '__main__':
	main()
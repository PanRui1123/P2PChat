import threading
import sys
import socket
import time
import Tkinter

root_window = 0
username = 0
passwd = 0

__author__ = {	'name':'Rui Pan',
				'email':'joshuapanrui@live.cn',
				'phone':'13684027112',
				'stunum':'201421060430'}


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

def sendmessage(text_msg, chatboard):
	global username
	msg = text_msg.get('1.0',Tkinter.END)
	text_msg.delete(0.0, Tkinter.END)	
	print 'send',msg
	chatboard.insert(Tkinter.CURRENT,username.get() + time.strftime(' %m-%d-%H %I:%M:%S\n',time.localtime(time.time())), 'green')
	chatboard.insert(Tkinter.CURRENT,msg)

def on_chat(lb,event):
	remote = lb.get(lb.curselection()) 
	chat_window = Tkinter.Toplevel(root_window)
	chat_window.title(' chatting with '+ remote)

	frame_left_top = Tkinter.Frame(chat_window, width=380, height=270, bg='white')
	frame_left_center = Tkinter.Frame(chat_window, width=380, height=100, bg='white')
	frame_left_bottom = Tkinter.Frame(chat_window, width=380, height=20)
	frame_right = Tkinter.Frame(chat_window, width=170, height=400, bg='white')

	text_msglist = Tkinter.Text(frame_left_top)
	text_msglist.bind("<KeyPress>", lambda e : "break")	

	text_msg = Tkinter.Text(frame_left_center);
	button_sendmsg = Tkinter.Button(frame_left_bottom, text='send',command= lambda: sendmessage(text_msg, text_msglist))	
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


def on_log_in(login_window, event = None):
	global root_window
	global username
	global passwd	

	print username.get(),passwd.get()
	friends = ['jack','pony','robin','pan','bill','jobs']

	lb = Tkinter.Listbox(root_window,selectmode = Tkinter.EXTENDED)
	for i in range(len(friends)):
	    lb.insert(Tkinter.END,friends[i])

	lb.bind('<Double-Button-1>',lambda event: on_chat(lb,event))


	lb.pack(side = Tkinter.LEFT)
	root_window.attributes("-alpha",1)
	root_window.attributes("-topmost",1)	

	login_window.destroy()	

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
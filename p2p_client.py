#!/usr/bin/env python
# coding: utf-8

import threading
import sys
import socket
import time
import Tkinter
import json
import ttk
import Tkinter as tk

root_window = 0
username = 0
passwd = 0
name_addr_dic = {}
name_socket_dic = {}
locationServerAddr = ('localhost',9026)



create_name = 0
chat_remote = 0
chat_msg = 0
chat_board = 0

class CReceiver(threading.Thread):
    def __init__(self, Socket, ChatBoard, chatWndow, Remotename):
        threading.Thread.__init__(self)
        self.m_socket = Socket
        self.m_chatboard = ChatBoard
        self.m_remote = Remotename
        self.chatwindow = chatWndow
        self.thread_stop = False;

    def run(self):
        global name_socket_dic
        global root_window

        global chat_board
        global chat_remote
        global chat_msg

        while not self.thread_stop:
            print "start recving"
            recv_msg = self.m_socket.recv(1024)
            if recv_msg == "":
                print 'remote is closed'

                self.chatwindow.destroy()
                name_socket_dic[remote].close()
                name_socket_dic[remote] = None
                self.stop()
            else:

                print "recvmsg:",recv_msg
                chat_board = self.m_chatboard
                chat_remote = self.m_remote
                chat_msg = recv_msg

                print chat_board
                print chat_remote
                print chat_msg

                root_window.event_generate("<<UpdateChatBoard>>",when = "tail")
    def stop(self):
        self.thread_stop = True;

def on_update_chat_board(event):
    global chat_board
    global chat_remote
    global chat_msg

    print chat_board
    print chat_remote
    print chat_msg

    if chat_board != 0:
        chat_board.insert(Tkinter.END,chat_remote + time.strftime(' %m-%d-%H %I:%M:%S\n',time.localtime(time.time())), 'blue')
        chat_board.insert(Tkinter.END,chat_msg)

class CListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.default_port = 8888
        while True:
            try:
                self.m_socket.bind(("",self.default_port))
                break;
            except Exception,e:
                self.default_port += 1
        self.m_socket.listen(10)

    def getaddr(self):
        return (socket.gethostbyname(socket.gethostname()),self.default_port)

    def run(self):
        global root_window
        global name_addr_dic
        global create_name
        while(True):
            (conn_socket,addr) = self.m_socket.accept()

            remotename = conn_socket.recv(1024).strip()

            print "remotename :",remotename
            name_socket_dic[remotename] = conn_socket
            create_name = remotename

            root_window.event_generate("<<CreateChatWindow>>",when = "tail")

def on_create_chat_window(event):
    global create_name
    create_chat_window(create_name)

def on_query(cmd , address = 0):

    global username
    global name_addr_dic

    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect(locationServerAddr)
    info = [cmd]
    if address == 0:
        info = info + [username.get()]
    else: info = info + [username.get()] + [address]

    toSend = json.dumps(info);

    fd.send(toSend)
    recved = json.loads(fd.recv(1024).strip())

    name_addr_dic = recved
    print('# client recv: %s' % name_addr_dic)

    fd.close()


def on_error(msg):
    print msg

def on_sign_up_action(regname , regpasswd):


    print regname.get(),regpasswd.get()

def on_sign_up(root):
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

    input_key.bind("<Return>", lambda: on_sign_up_action(regname, regpasswd))
    input_name.pack(pady = 20, side = Tkinter.TOP)
    input_key.pack(pady = 0, side = Tkinter.TOP)

    bottonname_2 = Tkinter.StringVar()
    bottonname_2.set('Regist')
    signup_btn = Tkinter.Button(cWinLogUp, textvariable = bottonname_2, command =lambda: on_sign_up_action(regname, regpasswd))
    signup_btn.pack()


def on_exit():
    print 'exit'
    login_window.destroy()

def sendmessage(text_msg, chatboard, remote):
    global username
    global name_socket_dic
    msg = text_msg.get('1.0',Tkinter.END)
    text_msg.delete(0.0, Tkinter.END)
    print 'send',msg
    chatboard.insert(Tkinter.END,username.get() + time.strftime(' %m-%d-%H %I:%M:%S\n',time.localtime(time.time())), 'green')
    chatboard.insert(Tkinter.END,msg)

    sock = name_socket_dic[remote]
    print sock
    sock.send(msg)

def on_chat(lb,event):
    global root_window
    global name_socket_dic
    global username

    remote = lb.get(lb.curselection())
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(tuple(name_addr_dic[remote]))
    name_socket_dic[remote] = conn

    conn.sendall(username.get())

    return create_chat_window(remote)

def create_chat_window(remote):

    global root_window
    global name_socket_dic

    chat_window = Tkinter.Toplevel(root_window)
    chat_window.title(' chatting with '+ remote)

    print "comes here"

    frame_left_top = Tkinter.Frame(chat_window, width=380, height=270, bg='white')
    frame_left_center = Tkinter.Frame(chat_window, width=380, height=100, bg='white')
    frame_left_bottom = Tkinter.Frame(chat_window, width=380, height=30)
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

def on_update_chat_table(lb,event = None):
    global name_addr_dic
    global username
    on_query("update")

    print("# client update friend list: %s" % name_addr_dic)
    friends = name_addr_dic.keys()

    lb.delete(0,Tkinter.END)
    for i in range(len(friends)):
        if friends[i] != username.get():lb.insert(Tkinter.END,friends[i])

def on_log_in(login_window, event = None):
    global root_window
    global username
    global passwd

    print("# client on log in: %s::%s" % (username.get(), passwd.get()))

    listener = CListener()
    myaddr = listener.getaddr()
    notify_location_server(myaddr)

    root_window.deiconify()
    root_window.attributes("-topmost", 1)


    lb = tk.Listbox(root_window, selectmode=Tkinter.EXTENDED)
    lb.bind('<Double-Button-1>', lambda event: on_chat(lb,event))
    lb.pack(fill=tk.BOTH, expand=1)

    update_btn = Tkinter.Button(root_window, text='Update',
            command =lambda: on_update_chat_table(lb))
    update_btn.pack(fill=tk.X)

    login_window.destroy()

    listener.start()

def notify_location_server(myaddr):
    #regist to location server
    on_query("add",myaddr)
    pass

def main():
    global root_window
    global username
    global passwd

    root_window = tk.Tk()
    root_window.title('P2PChat contacts')
    root_window.geometry('200x250')
    root_window.withdraw()

    root_window.event_add("<<CreateChatWindow>>", "<F1>")
    root_window.event_add("<<UpdateChatBoard>>", "<F2>")
    root_window.bind("<<CreateChatWindow>>", lambda event: on_create_chat_window(event))
    root_window.bind("<<UpdateChatBoard>>", lambda event: on_update_chat_board(event))


    login_window = tk.Toplevel(root_window)
    login_window.title('P2PChat Login')
    login_window.geometry('200x110')
    login_window.resizable(width=tk.FALSE, height=tk.FALSE)
    login_window.protocol('WM_DELETE_WINDOW', root_window.quit)


    menubar = tk.Menu(login_window)
    menu = tk.Menu(menubar, tearoff=0)
    menu.add_command(label='Exit', command=root_window.quit)
    menubar.add_cascade(label='Menu', menu=menu)
    login_window.config(menu = menubar)


    username = tk.StringVar()
    username.set('username')
    username_ent = ttk.Entry(login_window, textvariable = username)
    username_ent.pack(fill=tk.BOTH,
                      padx=5,
                      pady=5,
                      side=tk.TOP,
                      expand=1)

    passwd = tk.StringVar()
    passwd.set('password')
    passwd_ent = ttk.Entry(login_window, textvariable = passwd)
    passwd_ent.bind("<Return>", lambda event: on_log_in(login_window,event))
    passwd_ent.pack(fill=tk.BOTH,
                    padx=5,
                    pady=5,
                    side=tk.TOP,
                    expand=1)

    login_btn = ttk.Button(login_window, text='Log in',
                           command=lambda: on_log_in(login_window))
    login_btn.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT, expand=1)

    signup_btn = ttk.Button(login_window, text='Sign up',
                            command=lambda: on_sign_up(login_window))
    signup_btn.pack(fill=tk.X, padx=5, pady=5, side=tk.RIGHT, expand=1)


    root_window.mainloop()

if __name__ == '__main__':
    main()
    on_query("del")

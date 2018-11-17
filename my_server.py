import tkinter as tk
from tkinter import messagebox
import time
import datetime
from socket import *
import time
from time import ctime
import _thread




LARGE_FONT= ("Verdana", 12)

def my_server(show_1,HOST,PORT):


    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(5)
    currentDT = datetime.datetime.now()


    while True:
        show_1.insert(tk.END,"waiting for connection...")
        show_1.insert(tk.END,"\n")
        #print ('waiting for connection...')

        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()

        #print ('...connected from:', addr)
        show_1.insert(tk.END,"connected {}".format(addr))
        show_1.insert(tk.END,"\n")

        filename='Tux.png'
        f = open(filename,'rb')
        l = f.read(1024)

        while (l):
            tcpTimeClientSock.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)

        f.close()
        print('Done sending')
        tcpTimeClientSock.send('Thank you for connecting')
        tcpTimeClientSock.close()



        '''while True:
            data = tcpTimeClientSock.recv(BUFSIZE)
            if not data:
                break

            tcpTimeClientSock.send(bytes(currentDT.strftime("%I:%M:%S %p"),'utf-8'))

            show_1.insert(tk.END,data.decode('utf-8'))
            show_1.insert(tk.END,"\n")
            print(data.decode('utf-8'))

        tcpTimeClientSock.close()
    tcpTimeSrvrSock.close()'''

class Page(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        l_title=tk.Label(self, text="Server Software",
                         font="Arial,12")
        l_title.grid(row=0,column=0,columnspan=3, sticky="NSEW",padx=30,pady=30)

        label_username = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        entry_username = tk.Entry(self,show="*")

        entry_password = tk.Entry(self, show="*")

        label_username.grid(row=2, column=0, sticky='NSEW',padx=10,pady=10)
        label_password.grid(row=3, column=0, sticky='NSEW',padx=10,pady=10)
        entry_username.grid(row=2, column=1,sticky='NSEW',padx=10,pady=10)
        entry_password.grid(row=3, column=1,sticky='NSEW',padx=10,pady=10)

        checkbox = tk.Checkbutton(self, text="Keep me logged in")
        checkbox.grid(row=4, column=1,sticky='NSEW',padx=10,pady=10)

        logbtn = tk.Button(self, text="Login", bg="BlACK", fg="White",command=lambda: login_btn_clicked())
        logbtn.grid(row=5, column=1,sticky='NSEW', padx=10, pady=10)

        def login_btn_clicked():
            # print("Clicked")
            username = entry_username.get()
            password = entry_password.get()

            if len(username) and len(password) > 2:
                # print(username, password)

                if username == "admin" and password == "admin":
                    controller.show_frame(PageOne)
                # display a ,essage if username and password is incorrect!
                else:
                    messagebox.showinfo(self,"Invalid username or password ! ")

            else:
                messagebox.showinfo(self,"Enter Username and Password")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True

        clock = tk.Label(self, font=('times', 18, 'bold'), bg='green',fg="white")
        clock.grid(row=0,column=2, sticky="NSNESWSE",padx=8,pady=8)

        def tick():
            time2=time.strftime('%H:%M:%S')
            clock.config(text=time2)
            clock.after(200,tick)
        tick()

        label = tk.Label(self, text="Server Software ", font="Arial,16",bg="black",fg="White")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        l_host=tk.Label(self,text="Enter Host NAME")
        l_host.grid(row=1, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_host=tk.Entry(self)
        e_host.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_host.insert(tk.END,'127.0.0.1')


        l_port=tk.Label(self,text="Enter Port")
        l_port.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_port=tk.Entry(self)
        e_port.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_port.insert(tk.END,12121)

        message_label=tk.Label(self,text="Client Message",font=("Arial,12"))
        message_label.grid(row=3,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")


        scrollbar_y = tk.Scrollbar(self)
        scrollbar_y.grid(row=4, column=3,rowspan=6)

        show_1=tk.Text(self,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="Grey",fg="White")
        show_1.grid(row=4, column=0,rowspan=3,columnspan=3,sticky="NSEW")

        b_connect=tk.Button(self,text=" Connect",command=lambda: connect())
        b_connect.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")

        b_disconnect=tk.Button(self,text=" disconnect",command=lambda: disconnec())
        b_disconnect.grid(row=14,column=1,padx=10,pady=10,sticky="nsew")


        def runner():
            global after_id
            global secs
            secs += 1
            if secs % 2 == 0:  # every other second
                e_host_v=e_host.get()
                e_port_v=int(e_port.get())

            #after_id = self.after(1000, runner)  # check again in 1 second

        def connect():
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            #start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0
            #runner()  # start repeated checking


        def disconnec():
            global after_id
            if after_id:
                self.after_cancel(after_id)
                after_id = None







app = Page()
app.mainloop()

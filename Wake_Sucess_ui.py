import os
import time
from datetime import datetime
import re
import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askdirectory
import threading
from tkinter import scrolledtext
from main import handle

import logging
import logging.config
CON_LOG='config\\log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()

def cut_email(email):
    email_list=re.split('[, ：; ]',email.strip())
    return email_list

def _ui():
    root=Tk()
    root.title("智能音箱唤醒成功率自动化测试工具")

    sw=root.winfo_screenwidth()
    sh=root.winfo_screenheight()

    ww=100
    wh=100
    # x=(sw-ww)/2
    # y=((sh-wh)/5)*3
    x = 700
    y = 600

    root.geometry("%dx%d+%d+%d"%(x,y,ww,wh))

    title=Label(root,text="    智能音箱唤醒成功率测试工具V1.0",compound=CENTER,font=("微软雅黑",20))
    title.grid(row=0,columnspan=3,sticky=E+W)


    deviceid=StringVar()
    deviceid_label=Label(root,text="设备id",foreground="white",background="blue")
    deviceid_label.grid(sticky=E,padx=20,pady=20)
    deviceid_entry=Entry(root,textvariable=deviceid,width=70)
    deviceid_entry.grid(row=1,column=1,sticky=W)

    test_times=IntVar(value=100)
    test_times_label=Label(root,text="测试次数",foreground="white",background="blue")
    test_times_label.grid(sticky=E,padx=20,pady=20)
    test_times_entry=Entry(root,textvariable=test_times,width=70)
    test_times_entry.grid(row=2,column=1,sticky=W)


    test_space=IntVar(value=60)
    test_space_label=Label(root,text="测试间隔（s）",foreground="white",background="blue")
    test_space_label.grid(sticky=E,padx=20,pady=20)
    test_space_entry=Entry(root,textvariable=test_space,width=70)
    test_space_entry.grid(row=3,column=1,sticky=W)

    wake_path = StringVar()
    wake_path_label = Label(root, text="唤醒词路径", foreground="white", background="blue")
    wake_path_label.grid(sticky=E,padx=10,pady=10)
    wake_path_entry=Entry(root,textvariable=wake_path,width=70)
    wake_path_entry.grid(row=4,column=1,sticky=W)
    def selecctPath():
        path_=askdirectory()
        wake_path.set(path_)
    Button(root,text="路径选择",command=selecctPath).grid(row=4,column=2)


    email=StringVar(value="319910390@qq.com")
    email_label=Label(root,text="Email ",foreground="white",background="blue")
    email_label.grid(sticky=E,padx=20,pady=20)
    email_entry=Entry(root,textvariable=email,width=70)
    email_entry.grid(row=5,column=1,sticky=W)

    text = scrolledtext.ScrolledText(root, width=80, height=10)
    text.grid(row=6, column=1, columnspan=2, sticky=W)
    # text.insert(INSERT,'wew\n')

    def click():
        logging.info("点击开始测试按钮，开始测试")
        deviceid=deviceid_entry.get()
        logging.info("获取到的设备id: "+deviceid)

        test_times=test_times_entry.get()
        logging.info("获取到的测试次数是： "+str(test_times))

        test_space=test_space_entry.get()
        logging.info("获取到的测试间隔是： "+str(test_space))

        wake_path=wake_path_entry.get()
        logging.info("获取到的唤醒词路径是： "+str(wake_path))

        email=email_entry.get()
        logging.info("获取到的邮箱是： "+str(email))

        # 添加一个线程去处理
        th = threading.Thread(target=handle, args=(text,deviceid,test_times,wake_path,email,test_space))

        th.setDaemon(True)  # 设置守护线程，主线程结束后，该线程也要结束
        th.start()


    click_btn = Button(root, text="开始测试", command=click)
    click_btn.grid(row=7, column=0)




    root.mainloop()


if __name__=="__main__":
    _ui()















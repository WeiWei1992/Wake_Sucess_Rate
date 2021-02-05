from public import play_wav,load_log,get_log_time_after,log_check,load_audio
import os
import time
import re
import logging
import logging.config
from tkinter import *
CON_LOG = 'config\\log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()

import random
from operate_excel import creat_excel,write_excel
from send_result import my_send_email
import time
from datetime import datetime
def handle_wakepath(wake_path):
    logging.info("开始处理唤醒词路径组装")
    wake_wavs = []
    root = ''
    files_1 = []
    for tmp_root, dirs, files_tmp in os.walk(wake_path):
        if tmp_root:
            root = tmp_root
        if files_tmp:
            files_1.append(files_tmp)
    files = files_1[0]
    # print("len(files): ",len(files))
    # print("files: ",files)
    for file in files:
        wake_wav = os.path.join(root, file)
        wake_wavs.append(wake_wav)
    return wake_wavs
def get_wavs(wake_wavs):
    logging.info("随机使用一个唤醒词语料")
    wake_wavs_len = len(wake_wavs)
    num = random.randint(0, wake_wavs_len - 1)
    wav=wake_wavs[num]
    logging.info("随机使用的唤醒语料是： "+str(wav))
    return wav

def handle_deviceids(deviceids):
    #print("==============")
    # print(deviceids)
    logging.info("处理输入的设备ids")
    deviceidsList=re.split('[,:;；]',deviceids)
    logging.info(deviceidsList)
    # print(type(deviceidsList))
    return deviceidsList

def handle_emails(email):
    logging.info("处理输入的emails")
    emailList=re.split('[,:;；]',email)
    logging.info(emailList)
    return emailList

def handle(text,deviceids,num,wake_path,email,wait_time):

    deviceidsList=handle_deviceids(deviceids)

    error_num=0
    allnum = 0
    sucess_num=0

    logging.info("开始处理")

    logging.info("创建excel文件")
    excel_file=creat_excel()
    logging.info("创建的excel文件是: "+str(excel_file))

    #输入参数：deviceid,num测试次数，唤醒词路径，email
    wake_wavs=handle_wakepath(wake_path)
    logging.info("处理后的唤醒词： "+str(wake_wavs))
    wake_wavs_len=len(wake_wavs)
    logging.info("唤醒词个数： "+str(wake_wavs_len))
    num_wav=random.randint(0,wake_wavs_len-1)
    num=int(num)
    wait_time=int(wait_time)

    for i in range(num):
        try:
            i = i + 1
            logging.info("测试第     "+str(i)+"      次")
            t = time.time()
            j="测试第 "+str(i)+"  次\n"
            text.insert(END,j)
            tt = int(round(t * 1000))
            logging.info("当前的时间戳是： " + str(tt))

            time.sleep(30)

            wav=get_wavs(wake_wavs)
            logging.info("要播放的唤醒语料是： "+str(wav))
            play_wav(wav)
            # logging.info("等待(s)..."+str(wait_time))
            # time.sleep(wait_time)

            time.sleep(20)


            dt = datetime.now()
            #这个now_time是用来标注日志名称的
            now_time = dt.strftime('%Y_%m_%d_%H_%M_%S')

            for deviceid in deviceidsList:
                logging.info("拉取日志和audio文件")

                allnum=allnum+1

                filepath, filter_log_path,audio_path = load_log(device_id=deviceid,now_time=now_time)
                load_audio(deviceid, audio_path)


                logging.info("原始日志路径： "+str(filepath))
                logging.info("截取后的日志保存路径： "+str(filter_log_path))
                logging.info("截取时间戳 "+str(tt)+"  之后的日志")
                try:
                    after_time_log = get_log_time_after(filepath, filter_log_path, tt)
                except Exception as e:
                    logging.error("日志截取出现异常")
                    logging.error("进入下一轮")
                    continue
                logging.info("截取时间戳之后的日志路径是： "+str(after_time_log)+" ,该路径应该是和上面输入的路径是一致的 ")

                logging.info("日志检查是否有误唤醒....")
                res = log_check(after_time_log)
                logging.info("检查结果： "+str(res))
                if res==False:
                    error_num=error_num+1
                    # allnum = allnum + 1
                    logging.error(str(deviceid)+"--------------未唤醒----------------")
                    text.insert(END, str(deviceid)+"----未唤醒----\n")
                    # load_audio(deviceid,audio_path)
                else:
                    # allnum = allnum + 1
                    sucess_num=sucess_num+1
                    logging.info(str(deviceid)+"...............唤醒了................")
                    text.insert(END, str(deviceid)+"----唤醒了----\n")
                logging.info("结果保存excel")
                write_excel(excel_file,i,res,filepath,after_time_log,audio_path,deviceid)



            #还是这这个地方设置等待吧，因为如果等待时间太长，可能会导致日志和audio文件被冲掉
            logging.info("等待(s)..." + str(wait_time))
            for j in range(int(wait_time/10)):
                logging.info("等待第.... "+str((j+1)*10)+" s ")
                time.sleep(10)
        except:
            logging.info("出现了异常，继续下一个循环")
        else:
            continue

    text.insert(END,"测试结束发送邮件\n")
    #msg_to = ['1508691067@qq.com', 'wei_wei1992@yeah.net']
    email_list=handle_emails(email)
    my_send_email(email_list,excel_file,allnum,sucess_num)

    text.insert(END, "邮件发送完成,结束..........\n")
        # print()
        # if i%2==0:
        #     write_excel(excel_file,i,True)
        # else:
        #     write_excel(excel_file,i,False)


if __name__=="__main__":
    deviceids='JYZ7519'
    num=10
    wake_path="C:\\Users\\weiwei\\Desktop\\语音\\xiaoyou"
    email= ['1508691067@qq.com', 'wei_wei1992@yeah.net']
    wait_time=20
    handle(deviceid,num,wake_path,email,wait_time)



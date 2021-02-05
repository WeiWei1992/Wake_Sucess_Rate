import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr,formataddr
import datetime
from openpyxl import load_workbook
import os
import logging
import logging.config
CON_LOG='config\\log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()

def my_send_email(msg_to,file_path,test_times,sucess_nums):
    logging.info("开始发送邮件")
    now_time = datetime.datetime.now()
    year = now_time.year
    month = now_time.month
    day = now_time.day
    mytime = str(year) + " 年 " + str(month) + " 月 " + str(day) + " 日 "
    msg_from = '1508691067@qq.com'  # 发送方邮箱
    passwd = 'fgaplzfksqsihdbe'

    subject = '语音唤醒成功率结果'

    Success_rate=float(sucess_nums/test_times)
    #print(Success_rate)
    rata = '%.2f%%' % (Success_rate * 100)
    logging.info("唤醒成功率： "+str(rata))

    # 构造要发送的内容格式
    content = '''
                        <html>
                        <body>
                            <h1 align="center">智能音箱唤醒成功率测试结果</h1>
                            <p><strong>您好：</strong></p>
                            <blockquote><p><strong>测试次数: {test_times}</strong></p></blockquote>
                            <blockquote><p><strong>唤醒成功次数: {sucess_nums}</strong></p></blockquote>
                            <blockquote><p><strong>唤醒成功率: {rata}</strong></p></blockquote>
                            <blockquote><p><strong>附件是语音唤醒测试结果,请查收！</strong></p></blockquote>


                            <p align="right">{mytime}</p>
                        <body>
                        <html>
                        '''.format(test_times=test_times, sucess_nums=sucess_nums,rata=rata,mytime=mytime)
    #构建Html对象
    msg=MIMEMultipart()
    msg.attach(MIMEText(content,'html','utf-8'))

    att1=MIMEText(open(file_path,'rb').read(),'base64','utf-8')
    att1['Content-Type']='application/octet-stream'
    #file_base_path = os.path.dirname(file_path)  # 获取路径
    file_base_name = os.path.basename(file_path)  # 获取文件名称
    att1['Content-Disposition'] = 'attachment;filename=' + file_base_name
    msg.attach(att1)

    # 放入邮件主题
    msg['Subject'] = subject

    # 放入发件人,这是展示在邮件里面的，和时间的发件人没有关系
    msg['From'] = msg_from
    try:
        # 通过ssl方式发送，服务器地址，端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        # print("邮件发送成功")
        logging.info("邮件发送成功")
    except Exception as e:
        # print(e)
        logging.error("发送邮件失败")
        logging.error(e)
    finally:
        logging.info("结束发送邮件")
        s.quit()


if __name__=="__main__":
    Success_rate = 1 - float(1 / 18)
    print(Success_rate)
    rata='%.2f%%'%(Success_rate*100)
    print(rata)
    msg_to = ['1508691067@qq.com','wei_wei1992@yeah.net']



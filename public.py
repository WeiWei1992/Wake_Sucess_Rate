import logging
import logging.config

CON_LOG = 'config\\log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()
import os
import time
from datetime import datetime
import re
import pyaudio
import wave


def play_wav(filepath):
    # 播放wav文件
    chunk = 1024
    # 从目录中读取语音
    wf = wave.open(filepath, 'rb')
    #print("wf: ",wf)
    data = wf.readframes(chunk)
    #print("data: ",data)
    # 创建播放器
    p = pyaudio.PyAudio()

    # 获得语音文件的各个参数
    FORMAT = p.get_format_from_width(wf.getsampwidth())
    CHANELS = wf.getnchannels()
    RATE = wf.getframerate()
    # print('FORMAF:{} \nCHANELS: {}\nRATE: {}'.format(FORMAT,CHANELS,RATE))
    str_tmp = 'FORMAF:{} \nCHANELS:{}\nRATE:{}'.format(FORMAT, CHANELS, RATE)
    logging.info("播放的系统参数\n" + str_tmp)
    # 打开音频流，output=True表示音频输出
    stream = p.open(format=FORMAT,
                    channels=CHANELS,
                    rate=RATE,
                    frames_per_buffer=chunk,
                    output=True)
    # while data !='':
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
    # print("播放结束")
    logging.info("播放结束")


def save_txt(line, pathfile):
    # print("保存txt: ",line,filter_log_path)
    if pathfile == None:
        logging.error("保存结果的文件路径是空，请检查")
        return None
    try:
        # print("保存路径...",pathfile)
        with open(pathfile, 'a', encoding='utf-8') as f:
            f.write(line)
            #f.write('\n')
    except:
        # print("文件写入错误")
        logging.error("文件写入错误")
        return None
    else:
        return pathfile


def conver_log(pathfile1,pathfile2):
    #转换日志格式，要不然无法正则
    lineNumbers = 0
    with open(pathfile1,'rb') as f:
        while True:
            try:
                line = f.readline()
                lineNumbers=lineNumbers+1
                if not line:
                    logging.info("日志转换到了结尾")
                    break
            except UnicodeDecodeError:
                logging.error("出现了编码错误")
                logging.error("出现错误的行是:  "+str(lineNumbers))
            else:
                line = line.decode('utf-8', 'ignore')  #转换编码格式
                save_txt(line, pathfile2)


def load_log(device_id,now_time):

    # dt = datetime.now()
    # global now_time
    # now_time = dt.strftime('%Y_%m_%d_%H_%M_%S')  # 得用下划线，用： 号无法截图保存
    # global my_path

    my_path = os.path.abspath(os.getcwd())
    # if filepath == None:
    filepath = my_path + '/Logs/original_log/uai_log_%s_%s' % (now_time,device_id)
    resultpath=my_path + '/Logs/result_log/uai_result_log_%s_%s' % (now_time,device_id)
    audiopath=my_path+'/Logs/audio/audio_%s_%s'%(now_time,device_id)

    adbshell = 'adb -s ' + str(device_id) + ' pull /data/uai_log.txt ' + filepath
    #adbaudioshell='adb -s ' + str(device_id) + ' pull /tmp/audio  ' + audiopath

    logging.info("adb拉取日志 命令：" + adbshell)
    #logging.info("adb 拉取audio命令： "+adbaudioshell)
    result = os.path.exists(filepath)
    if result:  # 如果该文件夹存在
        os.system(adbshell)
    else:  # 如果不存在，先新建
        os.mkdir(filepath)
        os.system(adbshell)

    #audio_result=os.path.exists(audiopath)
    # if audio_result: #如果audio文件夹存在，
    #     os.system(adbaudioshell)
    # else:
    #     logging.info("创建audio文件夹并拉取pcm文件")
    #     os.mkdir(audiopath)
    #     os.system(adbaudioshell)

    result_log=os.path.exists(resultpath)
    if result_log:
        pass
    else:
        os.mkdir(resultpath)

    filepath_log=filepath+'\\uai_log.txt'
    result_log_path=resultpath+'\\uai_log_convert.txt'

    file_path_1 = filepath + '\\uai_log.txt'
    file_path_2 = resultpath + '\\uai_log_convert.txt'
    #file_path_3=audiopath+''

    time.sleep(3)
    print("file_path_1:  ",file_path_1 )
    print("file_path_2:  ",file_path_2)
    logging.info("file_path_1: "+str(file_path_1))
    logging.info("file_path_2: "+str(file_path_2))

    #2020-08-24新增，使用的过程中，出现了一次拉取出来的日志是空，转换后的路径是空，导致异常，可以在日志中加入一行无关紧要的日志。
    tmp_txt='this is conver log ,because of if the log is none,the program will be error,so I add this line ---weiwei \n\n'
    save_txt(tmp_txt,file_path_2)

    time.sleep(3)
    return file_path_1, file_path_2,audiopath

    # #日志格式转换，再这里展示不需要转换，因为在正则的时候使用rb模式
    # conver_log(file_path_1,file_path_2)
    # return file_path_2
    #return file_path_1,file_path_2

def load_audio(deviceid,audiopath):
    logging.info("提取audio文件")
    adbaudioshell = 'adb -s ' + str(deviceid) + ' pull /tmp/audio  ' + audiopath
    logging.info("提取audio文件的命令： "+str(adbaudioshell))

    audio_result=os.path.exists(audiopath)
    if audio_result: #如果audio文件夹存在，
        os.system(adbaudioshell)
    else:
        logging.info("创建audio文件夹并拉取pcm文件")
        os.mkdir(audiopath)
        os.system(adbaudioshell)




def filter_time(line):
    # print("检查是否是时间")
    # print(line)
    # print("type(line):", type(line))
    line = str(line)
    # print(line)
    # print("这里检查是否是时间行，是的话就返回True，否则返回False")
    # print("type(line):",type(line))
    '''
    使用正则，查看是否是时间行
    :param line: 读取的字符串行
    :return: False or True
    '''
    # 正式使用时，该正则要放到外面，是个全局的，这样就只初始化一次了就
    # pattern = re.compile(r'\d{4}(\-\|\/|.)(\s)\d{1,2}\1\d{1,2}')  # 时间的正则,\s表示空格
    pattern = re.compile(r'b\'\d{4}(\-\|\/|.)(\s)\d{1,2}\1\d{1,2}')  # 时间的正则,\s表示空格 \1标识和第一个()里面的一样
    line = line.strip('\n')  # 去掉换行符
    # line=line.strip('\n')
    time_result = pattern.match(line)
    # pattern.search:可以在字符串任何位置匹问配
    # pattern.match:是从字符百串开头进行度匹配

    pattern1 = re.compile(r'b\'\d{4}(\-\|\/|.)\d{1,2}\1\d{1,2}')  # 时间的正则,\s表示空格


    time_result1 = pattern1.match(line)

    if (time_result is None) and (time_result1 is None):
        # print("时间行没有匹配上")
        return False
    else:
        # print("时间行匹配上了")
        return True


def transform_log_time(line):
    # 转换中的时间，转换为毫秒级时间戳
    # 输入参数是日志中的时间字符串
    # print("输入要检测的时间行： ",line)
    #print("输入的时间行：",line)
    line = str(line)
    # 这几行是因为读入是以二进制读入的，需要特殊处理一下
    line = line.replace('\'', '')
    line = line.replace('b', '')
    line = line.strip('\n')
    line = line.replace('\\', '')
    line = line.replace('n', '')
    line=line.replace('r','')

    # print("处理后的时间行")
    #print("转换日志时间戳: ",line)
    try:
        datetime_obj = datetime.strptime(line, "%Y- %m-%d %H:%M:%S.%f")
        #print("datetime_obj: ",datetime_obj)
        obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    except Exception as e:
        # logging.error("第一个时间正则失败，使用第二个正则")
        # logging.error(str(e))
        # print("日志中输入的时间不对，请检查")
        #logging.error("日志中输入的时间不对，请检查")
        #logging.info("换一个正则继续提取日志时间戳")
        try:
            datetime_obj = datetime.strptime(line, "%Y-%m-%d %H:%M:%S.%f")
            # print("datetime_obj: ",datetime_obj)
            obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
        except Exception as e:
            logging.error("日志中输入的时间不对,应该是正则不对，继续适配")
            logging.error(str(e))
            return None
        else:
            return obj_stamp
    else:
        # print("转换成功")
        return obj_stamp


def get_log_time_after(filepath, filter_log_path, mytime=None):
    '''
    提取在某个时间戳之后的日志
    :param filepath: 日志文件路径
    :param mytime: 毫米级时间戳，该时间之后的日志会被提取,在播放音频之前就要计算出时间戳
    :return:
    '''
    upline = ''
    log = []
    lineNumbers = 0
    if mytime == None:
        # print("没有输入日志截取的时间戳")
        logging.error("没有输入日志截取的时间戳")
        return None
    is_time_up = False
    number_kongge = 0
    with open(filepath, 'rb') as f:
        # is_time_up=False
        while True:
            try:
                line = f.readline()
                #print("line: ",line)
                if not line:
                    # print(upline)
                    # print(line)
                    logging.info(line)
                    # print("结束了")
                    logging.info("日志读取结束了")
                    break
            except UnicodeDecodeError:
                # print("这里出现了编码错误，出现编码错误的行是： ", lineNumbers)
                # print("上一行是：",upline)
                # print("这一行是：",line)
                logging.error("这里出现了编码错误，出现编码错误的行是： " + str(lineNumbers))
                logging.error("上一行是： " + str(upline))
                continue
            else:
                # print(line)
                upline = line
                lineNumbers = lineNumbers + 1
                # print('lineNumbers:', lineNumbers)
                # if 'recogniationText' in str(line):
                #     print("找到了 ===================")
                if is_time_up == True:  # 如果找到了时间节点，就直接保存
                    #
                    # if 'recogniationText' in str(line):
                    #     # print("找到了 recogniationText===================")
                    #     logging.info("找到了 recogniationText===================")

                    log.append(line)
                    # line=str(line)
                    # 达到时间节点之后，转换一下格式进行保存
                    line = line.decode('utf-8', 'ignore')
                    save_txt(line, filter_log_path)

                if is_time_up == False:  # 如果还没有找到时间节点，才继续查找，找到了就不要在执行了
                    is_time_line = filter_time(line)
                    if is_time_line:
                        # 如果该行是时间行，转换成毫秒级的时间戳
                        log_tmp_time = transform_log_time(line)
                        #print("log_tmp_time: ",log_tmp_time)
                        # print('log_tmp_time:', log_tmp_time)
                        # print("mytime: ", mytime)
                        #log_tmp_time=int(log_tmp_time)
                        if log_tmp_time >= mytime:
                            is_time_up = True
                            # print("找到了时间隔离点")
                            # print(line)
                            # print(lineNumbers)
                            # print("==================")
                        else:
                            continue
    # print('lineNumbers: ', lineNumbers)
    logging.info("总行数 lineNumbers: " + str(lineNumbers))
    time.sleep(5)
    #return log
    return filter_log_path


def log_check(filepath):
    '''
    需要返回的是：唤醒词是否识别到 True/False          is_wake
                唤醒词所在的行内容,没有唤醒返回''    wake_line
                识别是否成功   True/False           is_indenty
                识别成的字符串                       identy_str
                配置文件中读取的与语音词               real_str
    '''
    is_wake = False
    wake_line = ''

    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = str(line)
            line = line.strip('\n')
            # 提取唤醒关键词
            pattern_wakeup = re.compile(r'.*?uaibot(.*?)\[app\]\[onWakeup\]\sapp\s\-\swakeup\:\sxiaoyouxiaoyou')
            matchObj_wakeup = re.match(pattern_wakeup, line)
            if matchObj_wakeup:
                # print("matchObj_wakeup.group: ",matchObj_wakeup.group())
                # print("matchObj_wakeup.group(1): ", matchObj_wakeup.group(1))
                # print("----------------------")
                # print(line)
                logging.info("正则匹配到了")
                logging.info("matchObj_wakeup.group:" + str(matchObj_wakeup.group()))
                #logging.info("matchObj_wakeup.group(1): " + str(matchObj_wakeup.group(1)))
                logging.info("输出该行： " + str(line))
                is_wake = True
                wake_line = line
    return is_wake
    # 返回的参数分别是：唤醒词是否识别到、唤醒词所在的行、交互是否识别成功、交互识别成的字符、配置文件中读取到的字符




if __name__=="__main__":
    #filepath="C:\\Users\\weiwei\\Desktop\\语料合成\\语料\\1.mp3"
    # filepath = "C:\\Users\\weiwei\\Desktop\\语料合成\\语料\\1_0-cvt.wav"
    # play_wav(filepath)
    filepath,filter_log_path=load_log(device_id='JYZ9337')
    #filter_log_path="1.txt"
    mytime="1598608250000"
    mytime=int(mytime)
    after_time_log=get_log_time_after(filepath, filter_log_path, mytime)
    res=log_check(filter_log_path)
    print("res； ",res)
    # print("===============")
    # print(len(after_time_log))
    # for i in after_time_log:
    #     print(i)


from public import play_wav
import os
import time
import logging
import logging.config
CON_LOG='config\\log.conf'
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()
def get_file_all(jiaohu_path=None):
    jiaohu_path_wav=[]
    if jiaohu_path==None:
        my_path=os.path.abspath(os.getcwd())
        jiaohu_new_path=my_path+"/yuliao/"
        print(jiaohu_new_path)

        for a,b,c in os.walk(jiaohu_new_path):
            print(a)
            print(b)
            print(c)
            for j in c:
                file=os.path.splitext(j)
                filename,type=file
                if type=='.wav':
                    jiaohu_path_wav_allpath=jiaohu_new_path+j
                    jiaohu_path_wav.append(jiaohu_path_wav_allpath)
                else:
                    continue
    return jiaohu_path_wav

if __name__=="__main__":
    jiaohu_path_wav=get_file_all()
    logging.info(jiaohu_path_wav)
    logging.info(len(jiaohu_path_wav))

    for wav in jiaohu_path_wav:
        logging.info("播放.....")
        logging.info(str(wav))
        play_wav(wav)
        logging.info("等待30s...")
        time.sleep(30)

    # print(len(jiaohu_path_wav))
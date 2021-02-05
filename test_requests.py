import requests
import time
res=requests.get(url='http://www.baidu.com')
print(res.status_code)
print(res.text)
time.sleep(20)
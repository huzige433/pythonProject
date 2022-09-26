# coding=utf-8
import re

import requests

#第一个检测green的url
from LinuxUtil import LinuxUtil


search_url1="https://www.****.com/srarch1.html"
#第二个检测green的url
search_url2="https://www.****.com/srarch2.html"

#固定9个ip
ipList=["12.345.67.890","12.345.67.891","12.345.67.892","12.345.67.893","12.345.67.894","12.345.67.895",
        "12.345.67.896","12.345.67.897","12.345.67.898"]

#服务器配置
host="192.168.111.111"
port=22
user="root"
pwd="root123"


def getstateone(): #页面一检测
    url1_text=requests.get(search_url1)
    url1_text.encoding=url1_text.apparent_encoding
    if "yellow" in url1_text.text :
        print "页面状态为yellow"
        return False
    else :
        return True



def getstatetwo(): #页面二检测取得ip
    ips=[]
    url1_text=requests.get(search_url2)
    url1_text.encoding=url1_text.apparent_encoding
    returnlist = url1_text.text.strip().splitlines()
    for row in returnlist:
        try:
            ip=re.findall(r"\d+\.\d+\.\d+\.\d+",row)[0]
            ips.append(ip)
        except:pass
    notiniplist=[item for item in  ipList if item not in ips] #不在页面中出现的ip列表
    return notiniplist

def start():
    if not getstateone():
        notiniplist=getstatetwo()
    if len(notiniplist) >0:
        # 假设命令为ping
        lineml=""
        for ip in notiniplist:
            #开始输入连接服务器运行命令
            linuxUtil = LinuxUtil(ip , port , user , pwd)
            printtxt=linuxUtil.execCmd("ping www.baidu.com") #这里修改命令.多命令用;分割
            for ttt in printtxt:
                print ttt
            linuxUtil.close()

if __name__=="__main__":

    start()

# coding=utf-8
import re
import paramiko
import requests


class LinuxUtil:
    def __init__(self, ip, port, name, pwd):
        """
        连接Linux服务器 并执行命令
        :param ip:
        :param port:
        :param name:
        :param pwd:
        """
        # 创建SSHClient实例对象
        self.ssh = paramiko.SSHClient()
        # 调用方法，标识没有远程机器的公钥，允许访问
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接远程机器 地址端口用户名密码
        self.ssh.connect(ip, port, name, pwd)

    def execCmd(self, cmdStr):
        """
        执行命令
        :param cmdStr: 多个命令用分号隔开
        :return:
        """
        # 执行命令（多个命令用分号隔开）
        stdin, stdout, stderr = self.ssh.exec_command(cmdStr)

        # 获取屏幕上的每行数据
        return stdout.read().decode().split('\n')

    def close(self):
        self.ssh.close()



#第一个检测green的url
search_url1="https://www.****.com/srarch1.html"
#第二个检测green的url
search_url2="https://www.****.com/srarch2.html"

#固定9个ip和对应的密码
ipdict={"12.345.67.890":"pwd1","12.345.67.891":"pwd2","12.345.67.892":"pwd3","12.345.67.893":"pwd1","12.345.67.894":"pwd1"
        ,"12.345.67.895":"pwd1","12.345.67.896":"pwd1","12.345.67.897":"pwd1","12.345.67.898":"pwd1"}

#服务器配置
port=22
user="root"


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
    notiniplist=[item for item in  ipdict.items() if item[0] not in ips] #不在页面中出现的ip键值对
    return notiniplist

def start():
    notiniplist=None
    if not getstateone():
        notiniplist=getstatetwo()
    if len(notiniplist) >0:
        # 假设命令为ping
        lineml=""
        for ip,pwd in notiniplist:
            #开始输入连接服务器运行命令
            linuxUtil = LinuxUtil(ip , port , user , pwd)
            printtxt=linuxUtil.execCmd("ping www.baidu.com") #这里修改命令.多命令用;分割
            for ttt in printtxt:
                print ttt
            linuxUtil.close()

if __name__=="__main__":
    start()

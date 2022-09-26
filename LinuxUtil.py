# -*- coding: utf-8 -*-

"""
@Time    ：2022/3/31 23:00
@Author  ：
@File    ：LinuxUtil.py
@Version ：1.0
@Function：

pip install paramiko -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
"""
import paramiko


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


if __name__ == '__main__':
    linuxUtil = LinuxUtil("", 22, "root", "")
    contexts= linuxUtil.execCmd("cd /;ls -l")
    for i in contexts:
        print i
    linuxUtil.close()
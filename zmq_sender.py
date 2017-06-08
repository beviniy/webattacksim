#-*- coding:utf-8 -*-

"""
@created on 2017-06-06
@auther:Ziv Xiao
"""

import zmq
import sys
from tomorrow import threads

"""添加了tomorrow支持异步发送消息，避免了pcap文件太大导致主界面卡顿"""

context = zmq.Context()     #获取zmq上下文
socket = context.socket(zmq.REQ)    #这里用zmq最简单的模式，REQ,REP


def connect(host="tcp://localhost:5299"):
    """连接字符串"""
    global socket
    socket.connect(host)

@threads(10)    #异步发送
def send(data):
    socket.send(data)   # 发送
    response = socket.recv()    # 接收返回信息
    return response

if __name__ == "__main__":
    """测试"""

    while True:
        data = raw_input("input your data:")
    
        if data == 'q':
            sys.exit()
    
        socket.send(data)
    
        response = socket.recv()
        print response

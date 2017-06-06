#-*- coding:utf-8 -*-

"""
@created on 2017-06-06
@auther:Ziv Xiao
"""

import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.REQ)

def connect(host="tcp://localhost:9527"):
    global socket

    socket.connect(host)
    
def send(data):
    socket.send(data)
    response = socket.recv()
    return response

if __name__ == "__main__":

    # connect()
    while True:
        data = raw_input("input your data:")
    
        if data == 'q':
            sys.exit()
    
        socket.send(data)
    
        response = socket.recv()
        print response

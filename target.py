#-*- coding:utf-8 -*-

"""
@created on 2017-06-06
@auther:Ziv Xiao
"""

import time
import zmq

import argparse

context = zmq.Context()

socket = context.socket(zmq.REP)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help='remote addr', default="tcp://*:5299", type=str)
    
    args = parser.parse_args() 
    socket.bind(args.target)
    while True:
        message = socket.recv()
        print message
        time.sleep(1)
        socket.send("server response!")
    
#!/usr/bin/env python
# encoding: utf-8

"""
@version: 3.6
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: client.py
@time: 2018/2/22 上午10:12
"""
import socket
import threading

token = '05d6617a'


def send(sock):
    while True:
        try:
            print('----开始-----')
            send_msg = input('_:')
            sock.send(send_msg.encode())
        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed!')


def accept(sock):
    while True:
        try:
            accept_msg = sock.recv(1024)
            if accept_msg:
                print(accept_msg.decode())
            else:
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 首次连接认证
    sock.connect(('127.0.0.1', 8080))
    sock.send(token.encode())
    # 输入游客名
    name = input('请输入你的名字: ')
    sock.send(name.encode())

    th1 = threading.Thread(target=send, args=(sock,))
    th2 = threading.Thread(target=accept, args=(sock,))
    threads = [th1, th2]
    for t in threads:
        t.start()
    # 阻塞等待接受信息
    t.join()


if __name__ == '__main__':
    run()

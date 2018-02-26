#!/usr/bin/env python
# encoding: utf-8

"""
@version: 3.6
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: server.py
@time: 2018/2/22 上午10:12
"""

import socket
import threading

connect_dict = dict()  # 所有客户端的所有用户信息
connect_list = list()  # 所有在线客户端的链接列表

token = '05d6617a'


def main(connection):
    """
    线程创建方法
    :param connection:
    :return:
    """
    connect_id = connection.fileno()
    nickname = connection.recv(1024).decode()
    connect_dict[connect_id] = nickname
    # 加入在线列表
    connect_list.append(connection)
    # 发布欢迎语
    welcome_str = '欢迎加入聊天室!目前在线人数为%d' % (len(connect_list))
    connection.sendall(welcome_str.encode())

    # 通知其他用户有新人加入聊天室
    pub_msg = '欢迎游客%s加入聊天室' % (connect_dict[connect_id])
    pub_other_msg(connect_id, pub_msg)

    while True:
        try:
            accept_msg = connection.recv(1024).decode()
            if accept_msg:
                msg = '游客%s:%s' % (connect_dict[connect_id], accept_msg)
                pub_other_msg(connect_id, msg)

        except:
            # 发送退出消息
            rm_msg = '【系统提示：' + connect_dict[connect_id] + ' 离开聊天室】'
            pub_other_msg(connect_id, rm_msg)
            # 移除列表
            connect_list.remove(connection)
            connect_dict.pop(connection.fileno())
            #关闭
            connection.close()
            return


def pub_other_msg(connect_id, msg):
    """
    推送给其他人消息
    :param connect_id:
    :param msg:
    :return:
    """
    for connect in connect_list:
        if connect.fileno() != connect_id:
            try:
                connect.send(msg.encode())
            except:
                print('推送给用户%s消息出错' % connect_dict[connect.fileno])


def run():
    """
    主程序
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 8080))
    sock.listen(5)

    while True:
        connection, addr = sock.accept()
        try:
            # 判断是否是同一个聊天室
            code = connection.recv(1024).decode()
            if code == token:
                # 创建连接
                thread = threading.Thread(target=main, args=(connection,))
                thread.setDaemon(True)
                thread.start()

            else:
                connection.send('你来错地方啦'.encode())
                connection.close()
        except:
            connection.close()


if __name__ == '__main__':
    run()

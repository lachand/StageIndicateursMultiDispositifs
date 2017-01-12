#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import select
import socket
from socket import error as SocketError

import demjson as json


class Serveur:
    """
    A class implementing a server for the table
    """

    def __init__(self, table, ip, port):
        """
        Initialize the server
        :param table: application running on the table
        """
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind((ip, int(port)))
        self.srvsock.listen(4)
        self.descriptors = [self.srvsock]
        self.parent = table

    def run_server(self):
        """
        Thread for parsing incoming messages and to send messages
        """
        while 1:
            (sread, swrite, sexc) = select.select(self.descriptors, [], [])
            for sock in sread:
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    try:
                        str = sock.recv(1000)
                        if str == '':
                            host, port = sock.getpeername()
                            str = 'Client left %s:%s\n' % (host, port)
                            self.broadcast_msg(str, sock)
                            sock.close
                            self.descriptors.remove(sock)
                            for user in self.parent.group.users:
                                if user.socket == sock:
                                    self.parent.remove_user(user)
                        else:
                            data = json.decode(str)
                            if data.has_key("Criterion"):
                                text = data["Criterion"]
                                creator = self.parent.get_user(int(data["IdUser"]))
                                fusionneurs = []
                                for fusionneur in data["Fusionneurs"]:
                                    fusionneurs.append(self.parent.get_user(int(fusionneur["IdUser"])))

                                text_type = data["TextType"]
                                criterion = self.parent.new_criterion(text, creator, fusionneurs, text_type=text_type)
                                for link in data["Links"]:
                                    criterion.add_link(int(link["IdImage"]), int(link["IdUser"]), float(link["Distance"]),
                                                       float(link["Angle"]))
                                    self.parent.get_animal(int(link["IdImage"])).remove_user()


                            if data.has_key("Animal"):
                                self.parent.get_animal(int(data["Animal"])).remove_user()

                            if data.has_key("User"):
                                for user in self.parent.group.users:
                                    if user.socket == sock:
                                        for zone in self.parent.user_zones:
                                            if zone.user.identifier == user.identifier:
                                                zone.set_name(data["User"])

                    except SocketError as e:
                        print e

    def accept_new_connection(self):
        """
        Accept incoming connections
        """
        newsock, (remhost, remport) = self.srvsock.accept()
        self.descriptors.append(newsock)

        user = self.parent.connect_user(newsock)

        newsock.send(
            '{"Color" : {"r" : "' + str(user.color[0]) + '", "g" : "' + str(user.color[1]) + '", "b" : "' + str(
                user.color[2]) + '"}, "User" : "' + str(user.identifier) + '"}\n')
        msg = '{"Users" : [ '
        for usr in self.parent.group.users:
            msg += '{"Id" : "' + str(usr.identifier) + '", "Color" : {"r" : "' + str(usr.color[0]) + '", "g" : "' + str(
                usr.color[1]) + '", "b" : "' + str(usr.color[2]) + '"}},'
        msg = msg[:-1]
        msg += ']}\n'
        newsock.send(msg)

    def broadcast_msg(self, str, omit_sock):
        """
        Send a message to all socket
        :param str: the message
        :param omit_sock: socket to omit
        """
        for sock in self.descriptors:
            if sock != self.srvsock and sock != omit_sock:
                sock.send(str)

    def send_msg(self, str, socket):
        """
        Send a message to a specified socket
        :param str: the message
        :param socket: the socket to send the message
        """
        if socket is not None:
            socket.send(str.encode('utf8'))

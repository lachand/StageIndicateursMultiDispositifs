#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import telnetlib

import demjson as json

IP_TABLE = "10.42.0.1"
PORT_TABLE = "8080"


class Client:
    """
    A class implementing a client for tablet
    """

    def __init__(self, tablette, ip=IP_TABLE, port=PORT_TABLE):
        """
        Initialize the server for the tabelet
        :param tablette: the main window
        :param ip: ip of server
        :param port: port of server
        """
        self.parent = tablette
        self.telnet = telnetlib.Telnet()
        print ip.__class__
        print port.__class__
        ip = IP_TABLE
        port = PORT_TABLE
        print ip.__class__
        print port.__class__
        self.telnet.open(ip, port)
        msg = self.telnet.read_until("\n")
        msg = msg.replace("\n", "")
        data = json.decode(msg)
        r = float(data["Color"]["r"])
        g = float(data["Color"]["g"])
        b = float(data["Color"]["b"])
        identifier = int(data["User"])
        self.parent.set_color([r, g, b])
        self.parent.set_user(identifier, [r, g, b])

    def connect(self):
        """
        Connect to the tabletop
        """
        msg = '{"User" : "' + self.parent.name +'"}'
        self.send_msg(msg)

    def send_msg(self, msg):
        """
        send a message to the tabletop
        """
        self.telnet.write(msg.encode('utf-8') + '\n')

    def on_stop(self):
        """
        Disconnect from the tabletop
        """
        print('Closing')
        self.telnet.close()

    def run_client(self):
        """
        Main thread
        """
        self.connect()
        while 1:
            msg = self.telnet.read_until('\n')
            msg = msg.replace('\n', "")
            print msg
            data = json.decode(msg.encode('utf8'))
            print data
            if data.has_key("Image"):
                self.parent.add_animal(data["Image"], data["ID"])
            if data.has_key("Users"):
                for usr in data["Users"]:
                    self.parent.add_user(int(usr["Id"]),
                                         [float(usr["Color"]["r"]), float(usr["Color"]["g"]), float(usr["Color"]["b"])])
            if data.has_key("Criterion"):
                text = data["Criterion"]
                creator = self.parent.get_user(int(data["IdUser"]))
                text_type = data["TextType"]
                fusionneurs = []
                for fusionneur in data["Fusionneurs"]:
                    fusionneurs.append(self.parent.get_user(int(fusionneur["IdUser"])))
                self.parent.edit_criterion(text, creator,fusionneurs,text_type)
#!/usr/local/bin/python
#  -*- coding: utf-8 -*-

import datetime

class Logger:
    """
    A class representing a data logger for our application
    """

    def __init__(self):
        """
        Initialize the logger
        """
        now = datetime.datetime.now()
        self.log_file_path = "logs/"+str(now.strftime("%Y_%m_%d_%H_%M"))
        self.file = open(self.log_file_path+".csv", "w")
        msg = "log_type;log_source;time;value_1;value_2;value_3;value_4;value_5\n"
        self.file.write(msg)
        msg = "create_critere;-1\ncreate_link;-1\ndestroy_link;-1\ninitialization;-1\nupdate_objective;-1\nvote;-1\n"
        self.file.write(msg)
        msg = "initialization;all;0\n"
        self.file.write(msg)
        self.time = datetime.datetime.now()

    def write(self, log_type, log_source, values):
        """
        Write a message on the logger
        :param log_type: the type of the message
        :param log_source: the source of the message
        :param values: the values of the message
        """
        diff = datetime.datetime.now() - self.time
        msg = str(log_type) + ";" + str(log_source) + ";" + str(diff.total_seconds())
        for value in values:
            msg += ";" + str(value)
            self.file.write(msg + "\n")

    def close(self):
        """
        Close the log file
        """
        pass
        #self.file.close()

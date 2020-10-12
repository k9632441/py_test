import socket
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_class = uic.loadUiType("test.ui")[0]


class client_socket():
    def __init__(self, _serverIP='localhost'):
        bindIP = 'localhost'
        serverIP = _serverIP

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((bindIP, 0))
        self.sock.connect((serverIP, 5500))

    def send_data(self, _msg):
        sbuff = bytes(_msg, encoding='utf-8')
        self.sock.send(sbuff)
        print("msg [{0}] send".format(_msg))

    def recv_data(self):
        rbuff = self.sock.recv(1024)
        data = str(rbuff, encoding='utf-8')
        print("msg [{0}] receive".format(data))


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connector = client_socket()

        self.run_btn.clicked.connect(self.run_shell)
        self.flag = 0
        self.l_flag = 0

        self.run_btn_2.clicked.connect(self.run_lidar_shell)
        self.run_btn_3.clicked.connect(self.run_all_stop_shell)

    def run_lidar_shell(self):
        if self.l_flag == 0:
            self.connector.send_data("lidar_run")
            self.l_flag = 1
        elif self.l_flag == 1:
            self.connector.send_data("lidar_stop")
            self.l_flag = 0

    def run_all_stop_shell(self):
        self.connector.send_data("all_stop")
        self.flag = 0
        self.l_flag = 0


    def run_shell(self):
        if self.flag == 0:
            self.connector.send_data("run_hello")
            self.flag = 1
        elif self.flag == 1:
            self.connector.send_data("stop_hello")
            self.flag = 0

    def __del__(self):
        self.connector.send_data("stop")
        self.connector.sock.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()

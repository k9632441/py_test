#! /usr/bin/env python

import socketserver
import sys
import os
import subprocess
from multiprocessing import Process
import time

def shell_run():
    cmd = "~/catkin_ws/devel/test_sh.sh"
    subprocess.run(cmd, shell = True)


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.process_list = {}
        print("Connect Clinet: {0} ".format(self.client_address[0]))

        self.sock = self.request

        recv_data = self.receive_data()
        
        while True:
            data = recv_data.__next__()
            print(data)
            if data == 'run_hello':
                data = None
                cmd = "~/catkin_ws/devel/test_sh.sh"
                self.process_list["hello"] = subprocess.Popen(cmd, shell = True)
            elif data == 'stop':
                break
            time.sleep(5)
        self.sock.close()
        exit(0)

    def receive_data(self):
        while True:
            rbuff = self.sock.recv(1024)
            data = str(rbuff, encoding='utf-8')
            print("process-a = " + data)
            
            yield data
            
            if data == 'hello_stop':
                self.process_list["hello"].terminate()
                self.process_list.pop("hello")
            elif data == 'lidar_stop':
                self.process_list["lidar"].terminate()
                self.process_list.pop("lidar")
            elif data == 'all_stop':
                for proc in self.process_list.items():
                    proc[1].terminate()
                self.process_list.clear
            elif data == 'stop':
                break


if __name__ == '__main__':
    bindIP = 'localhost'
    bindPort = 5500

    server = socketserver.TCPServer((bindIP, bindPort), MyTCPHandler)

    print("start server..")

    server.serve_forever()


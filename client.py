import sys,time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QSplitter, QComboBox, QVBoxLayout, QDialog, QWidget, QPushButton,
    QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit, QLineEdit,
    QHBoxLayout,
)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from socket import AF_INET, socket, SOCK_STREAM
import argparse
from threading import Thread
from socketserver import ThreadingMixIn

status='status'
tcpClientA=None

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.flag=0
        self.label = QLabel(status, self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {color: blue;}")
        self.chatTextField=QLineEdit(self)
        self.chatTextField.resize(350,100)
        self.chatTextField.move(10,350)
        self.btnSend=QPushButton("Send",self)
        self.btnSend.resize(350,30)
        self.btnSendFont=self.btnSend.font()
        self.btnSendFont.setPointSize(12)
        self.btnSend.setFont(self.btnSendFont)
        self.btnSend.move(10,360)
        self.btnSend.setStyleSheet("{background-color: #000080, color: silver;}")
        self.btnSend.clicked.connect(self.send)

        self.cb = QComboBox()
        self.cb.addItem("C")
        self.cb.addItem("C++")
        self.cb.addItems(["Java", "C#", "Python"])
        self.cb.currentIndexChanged.connect(self.combo_population)

        self.btnConn=QPushButton("Connect",self)
        self.btnConn.resize(350,30)
        self.btnConnFont=self.btnConn.font()
        self.btnConnFont.setPointSize(12)
        self.btnConn.setFont(self.btnConnFont)
        self.btnConn.move(10,360)
        self.btnConn.setStyleSheet("{background-color: #000080, color: silver;}")
        self.btnConn.clicked.connect(self.send)

        self.chatBody=QVBoxLayout(self)
        # self.chatBody.addWidget(self.chatTextField)
        # self.chatBody.addWidget(self.btnSend)
        # self.chatWidget.setLayout(self.chatBody)
        splitter=QSplitter(QtCore.Qt.Vertical)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400,100])

        splitter2=QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(self.cb)
        splitter2.addWidget(self.btnSend)
        splitter2.addWidget(self.btnConn)
        splitter2.addWidget(self.label)
        splitter2.setSizes([30, 30, 30, 10])


        splitter3=QSplitter(QtCore.Qt.Vertical)
        splitter3.addWidget(splitter)
        splitter3.addWidget(splitter2)
        splitter3.setSizes([200,10])

        self.chatBody.addWidget(splitter3)


        self.setWindowTitle("Slac chat")
        self.resize(500, 500)

    def combo_population(self, index):
        print(index)


    def send(self):
        text=self.chatTextField.text()
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted='{:>80}'.format(text)
        self.chat.append(textFormatted)
        tcpClientA.send(text.encode())
        self.chatTextField.setText("")

class ClientThread(Thread):
    def __init__(self,window):
        Thread.__init__(self)
        self.window=window

    def run(self):
       #host = socket.gethostname()
       host = "127.0.0.1"
       port = 33002
       BUFFER_SIZE = 2048
       global tcpClientA
       tcpClientA = socket(AF_INET, SOCK_STREAM)
       tcpClientA.connect((host, port))

       while True:
           data = tcpClientA.recv(BUFFER_SIZE)
           window.chat.append(data.decode("utf-8"))
       tcpClientA.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    clientThread=ClientThread(window)
    clientThread.start()
    window.exec()
    sys.exit(app.exec_())

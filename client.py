#!/usr/bin/env python3

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QSplitter, QComboBox, QVBoxLayout, QDialog, QWidget, QPushButton,
    QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit,
    QLineEdit, QHBoxLayout, QInputDialog
)
from PyQt5.QtCore import Qt
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.flag = 0
        self.user = ""
        self.status = "offline"

        self.label = QLabel(self.user, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {color: blue;}")

        self.status = QLabel(self.status, self)
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("QLabel {color: grey;}")

        self.btnSend = QPushButton("Send",self)
        self.btnSendFont = self.btnSend.font()
        self.btnSend.clicked.connect(self.send)

        self.btnConn = QPushButton("Connect",self)
        self.btnConnFont = self.btnConn.font()
        self.btnConn.clicked.connect(self.connect)

        self.btnDisconn = QPushButton("Disconnect",self)
        self.btnDisonnFont = self.btnDisconn.font()
        self.btnDisconn.clicked.connect(self.disconnect)

        self.cb = QComboBox()
        self.cb.addItem("Flor")
        self.cb.addItems(["Rick", "Caro", "John"])
        self.cb.currentIndexChanged.connect(self.combo_population)

        self.chatBody = QVBoxLayout(self)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chatTextField = QLineEdit(self)

        self.splitter = QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.chat)
        self.splitter.addWidget(self.chatTextField)
        self.splitter.setSizes([400, 100])

        self.splitter1 = QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.label)
        self.splitter1.addWidget(self.status)

        self.splitter2 = QSplitter(QtCore.Qt.Horizontal)
        self.splitter2.addWidget(self.cb)
        self.splitter2.addWidget(self.btnSend)
        self.splitter2.addWidget(self.btnConn)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setSizes([30, 30, 30, 10])

        self.splitter3 = QSplitter(QtCore.Qt.Vertical)
        self.splitter3.addWidget(self.splitter)
        self.splitter3.addWidget(self.splitter2)
        # splitter3.setSizes([200,10])

        self.chatBody.addWidget(self.splitter3)
        self.setWindowTitle("Slac chat")
        self.resize(500, 500)

    def login(self):
        text, okPressed = QInputDialog.getText(self, "Login", "Your name:",)
        if okPressed and text != '':
            self.user = text
        else:
            print("No valid user. system closed.")
            sys.exit(app.exec_())

    def combo_population(self, index):
        print(index)

    def send(self):
        try:
            text = self.chatTextField.text()
            if not text:
                QMessageBox.about(self, "Error", "Add a message to send")
        except ValueError as e:
            print(e)
        font = self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted = '{:>80}'.format(text)
        self.chat.append(textFormatted)
        self.chatTextField.setText("")
        return text

    def connect(self):
        self.status.setText('Online')
        self.splitter2.replaceWidget(2, self.btnDisconn)

    def disconnect(self):
        self.status.setText('Offline')
        self.splitter2.replaceWidget(2, self.btnConn)


class ClientThread(Window, Thread):
    def __init__(self):
        super().__init__()
        Thread.__init__(self)
        self.login()
        self.connect()

    def connect(self):
        host = "127.0.0.1"
        port = 33002
        self.tcpclient = socket(AF_INET, SOCK_STREAM)
        self.tcpclient.connect((host, port))
        cmd = '{REGISTER}' + str(self.user)
        self.tcpclient.send(cmd.encode())
        super().connect()
        self.start()

    def disconnect(self):
        self.tcpclient.close()
        super().disconnect()

    def send(self):
        text = super().send()
        self.tcpclient.send(text.encode())

    def run(self):
        # host = socket.gethostname()
        BUFFER_SIZE = 2048
        while True:
            msg = self.tcpclient.recv(BUFFER_SIZE)
            msg = msg.decode()
            if msg.startswith('{CLIENTS}'):
                clients = msg.split('}')[0]
                clients = [user for user in clients.split('|')]
                self.combo_population(clients)
                continue

            else:
                window.chat.append(msg)

        self.tcpclient.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientThread()
    window.exec()
    sys.exit(app.exec_())

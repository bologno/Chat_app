#!/usr/bin/env python3

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QSplitter,
    QComboBox,
    QVBoxLayout,
    QDialog,
    QWidget,
    QPushButton,
    QApplication,
    QMainWindow,
    QAction,
    QMessageBox,
    QLabel,
    QTextEdit,
    QLineEdit,
    QHBoxLayout,
    QInputDialog,
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

        self.btnSend = QPushButton("Send", self)
        self.btnSendFont = self.btnSend.font()
        self.btnSend.clicked.connect(self.send)

        self.btnConn = QPushButton("Connect", self)
        self.btnConnFont = self.btnConn.font()
        self.btnConn.clicked.connect(self.connect)

        self.btnDisconn = QPushButton("Disconnect", self)
        self.btnDisonnFont = self.btnDisconn.font()
        self.btnDisconn.clicked.connect(self.disconnect)

        #cbFlag makes sure that all client list is added once
        #Then updated one at the time on new or left users.
        self.cbFlag = True
        self.cb = QComboBox()
        self.cb.addItem('ALL')
        # self.cb.currentIndexChanged.connect(self.defineTarget)

        self.chatBody = QVBoxLayout(self)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chatTextField = QLineEdit(self)
        self.target = ""

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
        text, okPressed = QInputDialog.getText(self, "Login", "Your name:")
        if okPressed and text != "":
            self.user = text
        else:
            print("No valid user. system closed.")
            sys.exit(app.exec_())

    def combo_population(self, clients):
        if len(clients) > 0:
            self.cb.addItems(clients)
            self.cbFlag = False

    def send(self):
        try:
            text = self.chatTextField.text()
            if not text:
                QMessageBox.about(self, "Error", "Add a message to send")
        except ValueError as e:
            print(e)
        #font = self.chat.font()
        #font.setPointSize(13)
        #self.chat.setFont(font)
        #textFormatted = "{:>80}".format(text)
        #message gets header from combobox
        header=self.cb.currentText()
        message = '{'+header+'}' + text
        print('message about to leave')
        print(message)
        #self.tcpclient.send(message.encode())
        #self.chat.append(text)
        self.chatTextField.setText("")
        return message

    def connect(self):
        self.status.setText("Online")
        self.splitter2.replaceWidget(2, self.btnDisconn)

    def disconnect(self):
        self.status.setText("Offline")
        self.splitter2.replaceWidget(2, self.btnConn)

    def defineTarget(self):
        pass


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
        cmd = "{REGISTER}" + str(self.user)
        self.tcpclient.send(cmd.encode())
        super().connect()
        self.start()

    def disconnect(self):
        self.tcpclient.send('{QUIT}'.encode())
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
            if self.cbFlag and msg.startswith("{CLIENTS}"):
                clients = msg.split("}")[1]
                clients = [user for user in clients.split("|")]
                clients.remove(self.user)
                self.combo_population(clients)
                continue

            if not self.cbFlag and msg.startswith("{UPD}"):
                msg = msg.split("}")[1]
                client = msg.split()[0]
                if 'left' in msg:
                    self.cb.removeItem(client)
                else:
                    self.cb.addItem(client)
            #else:
            #    print('msg')
            #    print(msg)

            if len(msg.split('}')) > 1:
                window.chat.append(msg.split("}")[1])
            else:
                window.chat.append(msg)

        self.disconnect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientThread()
    window.exec()
    sys.exit(app.exec_())

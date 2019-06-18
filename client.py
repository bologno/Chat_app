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
        # Flags points if the connection is open for this user name
        self.reg = False
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

        self.btnLink = QPushButton("Disconnect", self)
        self.btnLinkFont = self.btnLink.font()
        self.btnLink.clicked.connect(self.disconnect_socket)

        # cbFlag makes sure that all client list is added once
        # Then updated one at the time on new or left users.
        self.cbFlag = True
        self.cblist = []
        self.cb = QComboBox()
        self.cb.addItem('ALL')

        self.chatBody = QVBoxLayout(self)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chatTextField = QLineEdit(self)
        self.target = ""

        self.splitter1 = QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.chat)
        self.splitter1.addWidget(self.chatTextField)
        self.splitter1.addWidget(self.status)

        self.splitter2 = QSplitter(QtCore.Qt.Horizontal)
        self.splitter2.addWidget(self.cb)
        self.splitter2.addWidget(self.btnSend)
        self.splitter2.addWidget(self.btnLink)

        self.splitter3 = QSplitter(QtCore.Qt.Vertical)
        self.splitter3.addWidget(self.splitter1)
        self.splitter3.addWidget(self.splitter2)

        self.chatBody.addWidget(self.splitter3)
        self.resize(500, 500)

    def login(self):
        text, okPressed = QInputDialog.getText(self, "Login", "Your name:")
        if okPressed and text != "":
            self.user = text
            self.setWindowTitle("Slac chat. User: "+self.user)
        else:
            print("No valid user. system closed.")
            sys.exit(app.exec_())

    def combo_population(self, clients):
        if len(clients) > 0:
            for client in clients:
                self.cblist.append(client)
            self.cb.addItems(clients)
            self.cbFlag = False

    def send(self):
        try:
            text = self.chatTextField.text()
            if not text:
                QMessageBox.about(self, "Error", "Add a message to send")
        except ValueError as e:
            print(e)
        # message gets header from combobox
        header = self.cb.currentText()
        message = '{'+header+'}' + text
        self.chatTextField.setText("")
        return message

    def connect(self):
        self.status.setText("Online")
        self.btnLink.setText("Disconnect")
        self.reg = True
        self.splitter2.refresh()
        print('self.reg when connect button')
        print(self.reg)

    def disconnect(self):
        self.status.setText("Offline")
        self.btnLink.setText("Connect")
        self.reg = False
        self.splitter2.refresh()
        print('self.reg when disconnect button')
        print(self.reg)

    def defineTarget(self):
        pass


class ClientThread(Window, Thread):
    def __init__(self):
        super().__init__()
        Thread.__init__(self)
        self.login()
        self.connect_socket()

    def connect_socket(self):
        if not self.reg:
            self.reg = True
            host = "127.0.0.1"
            port = 33002
            self.tcpclient = socket(AF_INET, SOCK_STREAM)
            self.tcpclient.connect((host, port))
            cmd = "{REGISTER}" + str(self.user)
            self.tcpclient.send(cmd.encode())
            super().connect()
            self.start()
        else:
            self.disconnect_socket()
            # self.tcpclient.send("".encode())

    def disconnect_socket(self):
        print('logging of. Empty msg sent to server')
        self.tcpclient.send(" ".encode())
        # self.tcpclient.shutdown(1)
        # self.tcpclient.close()
        # self.interrupt()
        # ssuper().disconnect()

    def send(self):
        # Not bradcasted messages go with private message label into chat
        text = super().send()
        if not text.startswith("{ALL}"):
            window.chat.append(self.user+': (private) '+text.split("}")[1])
        self.tcpclient.send(text.encode())

    def run(self):
        # host = socket.gethostname()
        BUFFER_SIZE = 2048
        while True:
            msg = self.tcpclient.recv(BUFFER_SIZE)
            msg = msg.decode('utf-8')
            print('received from server ', msg)
            if self.cbFlag and msg.startswith("{CLIENTS}"):
                clients = msg.split("}")[1]
                clients = [user for user in clients.split("|")]
                clients.remove(self.user)
                self.combo_population(clients)
                continue

            if not self.cbFlag and msg.startswith("{UPD}"):
                msg = msg.split("}")[1]
                client = msg.split()[0]
                print('client {}'.format(client))
                print('client type {}'.format(type(client)))
                if 'left' in msg:
                    self.cb.removeItem(self.cblist.index(client)+1)
                    self.cblist.remove(client)
                else:
                    self.cb.addItem(client)
                    self.cblist.append(client)

            if msg.startswith("{CLIENTS}"):
                pass
            elif len(msg.split('}')) > 1:
                window.chat.append(msg.split("}")[1])
                if msg.startswith("{OFF}"):
                    print("Shook hands with server, about to logoff")
                    self.tcpclient.shutdown(1)
                    self.tcpclient.close()
                    super().disconnect()
            else:
                window.chat.append(msg)

        self.disconnect()


def run():
    app = QApplication(sys.argv)
    window = ClientThread()
    window.exec()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()

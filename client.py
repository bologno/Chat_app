import sys,time
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QSplitter, QComboBox, QVBoxLayout, QDialog, QWidget, QPushButton,
    QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit, QLineEdit,
    QHBoxLayout,
)
from PyQt5.QtCore import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

status='status'
tcpClientA=None
connection_state = False

class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.flag=0

        self.label = QLabel(status, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {color: blue;}")

        self.chatTextField=QLineEdit(self)

        self.btnSend=QPushButton("Send",self)
        self.btnSendFont=self.btnSend.font()
        self.btnSend.setStyleSheet("{background-color: #000080, color: silver;}")
        self.btnSend.clicked.connect(self.send)

        self.cb = QComboBox()
        self.cb.addItem("Flor")
        self.cb.addItems(["Rick", "Caro", "John"])
        self.cb.currentIndexChanged.connect(self.combo_population)

        self.btnConn=QPushButton("Connect",self)
        self.btnConnFont=self.btnConn.font()
        self.btnConn.setStyleSheet("{background-color: #000080, color: silver;}")
        self.btnConn.clicked.connect(self.connect)

        self.chatBody=QVBoxLayout(self)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        splitter=QSplitter(QtCore.Qt.Vertical)
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
        try:
            text=self.chatTextField.text()
            if not text:
                QMessageBox.about(self, "Error", "Add a message to send")
        except ValueError as e:
            print(e)
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted='{:>80}'.format(text)
        self.chat.append(textFormatted)
        tcpClientA.send(text.encode())
        self.chatTextField.setText("")

    def connect(self):
        clientThread=ClientThread(window)
        clientThread.start()

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

    window.exec()
    sys.exit(app.exec_())

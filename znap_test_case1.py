
"""
Test Case #1:
Title: Welcome message to User.
Description: New user gets welcome message from server after succesfull login.
Preconditions: *Server is up and running.
Steps: *Client starts a session. *Server sends a greeting message to user.
Expected results: User gets welcome message on his thread input/ also on UI.
Actual result:
Automatable: Yes
"""

import unittest
import server
from threading import Thread
import time
import random
from socket import AF_INET, socket, SOCK_STREAM
import re


test_name = " Welcome message"

def _server():
    print("Setting up server")
    while True:
        print("Server running")
        time.sleep(10)


def _send_message(conn, msg):
    msg = "{}\n".format(msg)
    conn.send(msg.encode())


def _client(user):
    host = "127.0.0.1"
    port = 33002
    tcpclient = socket(AF_INET, SOCK_STREAM)
    tcpclient.connect((host, port))

    _send_message(tcpclient, "{REGISTER} %s" % user)
    # print(tcpclient.recv(2048))
    return check(tcpclient, "welcome")

    #print("Goodbye message received in client side: " +str(check(tcpclient, "Bye")))
    # _send_message(tcpclient, " ")


def check(socket, pattern):
    BUFFER_SIZE = 2048
    # host = socket.gethostname()
    while True:
        msg = socket.recv(BUFFER_SIZE)
        msg = msg.decode("utf-8")
        print("CLIENT "+ msg)
        return re.search(pattern, msg.lower())


def main():
    user = "Pedro"
    chat_server = Thread(target=server.run)
    chat_server.start()
    return _client(user)


if __name__ == "__main__":
    main()

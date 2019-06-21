"""
Test Case #2:
Title: Goodbye message to User.
Description: user gets goodbye message from server after clicking logout button.
Preconditions: *Server is up and running.
Steps: *Client starts a session. *User logs in. *User clicks logput button.
Expected results: User gets dissconected and recieves a goodbye message.
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

test_name = "Goodbye message"
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

    _send_message(tcpclient, "{QUIT}")
    return check(tcpclient, "goodbye")

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
    # candidates = [client, server]
    # hilos=[thread(target=node.run) for node in candidates]
    #
    # for node in hilos:
    #     node.start()
    #     time.sleep(1)
    #
    # for node in hilos:
    #     node.join()
    user = "Pedro"
    chat_server = Thread(target=server.run)
    chat_server.start()

    return _client(user)

if __name__ == "__main__":
    main()

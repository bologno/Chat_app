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

import server
# import client
from threading import Thread
import time
import random
from socket import AF_INET, socket, SOCK_STREAM



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
    _send_message(tcpclient, "{ALL} hello")

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

    _client(user)

if __name__ == "__main__":
    main()

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
import client_lite





def main():
    user = input("Enter client name")
    chat_server = Thread(target=server.run)
    chat_server.start()
    time.sleep(1)
    print("{} test positive result: ", client_lite.run("goodbye"))


if __name__ == "__main__":
    main()

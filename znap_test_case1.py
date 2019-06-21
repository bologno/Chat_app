
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
import client_lite





def main():
    user = input("Enter client name")
    chat_server = Thread(target=server.run)
    chat_server.start()
    time.sleep(1)
    print("{} test positive result: ", client_lite.run("welcome"))


if __name__ == "__main__":
    main()

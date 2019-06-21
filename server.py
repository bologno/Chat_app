#!/usr/bin/env python3

import argparse
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

"""
Here's how it works. Qt marks the thread which creates the first QApplication
instance as the "main thread". You won't get a warning the first time.
When you destroy that QApplication, Qt does not release all resources.
For example, there will still be a hidden global QPixmapCache which needs to be
accessed from the QApplication's original thread.

When you start another thread to create a new QApplication, Qt checks the
thread. If Qt detects that you're using a different thread from the first
QApplication's thread, then it will give you a warning.

To avoid the warning and to avoid corruption, you must make sure that the same
thread creates the QApplication every time.

Alternatively, you can create only one QApplication and never destroy it.
Every time you want to create a new PDF, do it in that thread.
"""


class ChatServer(object):
    def __init__(self, host, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host, port))
        self.clients = {}
        self.bufsize = 2048
        self.counter = 1

        try:
            self.socket.listen(5)
            # self.socket.settimeout(0.5)
            print("Server Started at {}:{}".format(host, port))
            print("Waiting for connection...")
            ACCEPT_THREAD = Thread(target=self.fire)
            ACCEPT_THREAD.start()
            ACCEPT_THREAD.join()
            self.socket.close()
        except KeyboardInterrupt:
            print("Interrupted")
            ACCEPT_THREAD.interrupt()

    def fire(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.socket.accept()
            print("%s:%s has connected." % client_address)
            # addresses[client] = client_address
            client.settimeout(5)
            client_thread = Thread(target=self.handle_client, args=(client,))
            client_thread.start()

    def handle_client(self, client):  # Takes client socket as argument.
        """Handles a single client connection."""
        name = ""
        prefix = ""

        while True:
            # Buffer sometimes saves two messages in the same buffer variableself
            # Specially when server sends hello message and the online users list.
            msgs = client.recv(self.bufsize).decode()

            # print("new message arrived {}".format(msgs))
            if not msgs or msgs == " ":
                print("About to unplug {}.".format(name))
                break
            else:

                for msg in msgs.strip().split("\n"):
                    print("msg=%s" % msg)
                    if msg == " ":
                        print("About to kill user {}.".format(name))
                        msg = "{QUIT}"

                    # Avoid messages before registering
                    if msg.startswith("{ALL}") and name:
                        new_msg = msg.replace("{ALL}", "{MSG}" + prefix)
                        self.send_message(new_msg, broadcast=True)
                        continue

                    if msg.startswith("{REGISTER}"):
                        name = msg.split("}")[1].strip()
                        welcome = "{%s}Welcome %s!" % (name, name)
                        self.send_message(welcome, destination=client)
                        msg = "{UPD}%s has joined the chat!" % name
                        self.send_message(msg, broadcast=True)
                        self.clients[client] = name
                        prefix = name + ": "
                        self.send_clients()
                        continue

                    if msg == "{QUIT}":
                        # print("saying goodbye.")
                        self.send_message("{OFF}Goodbye %s" % name, destination=client)
                        # self.send_message(
                        #     "{UPD}%s has left the chat." % name, broadcast=True
                        # )
                        # self.send_clients()
                        client.close()
                        try:
                            del self.clients[client]
                        except KeyError:
                            pass
                        if name:
                            self.send_message(
                                "{UPD}%s has left the chat." % name, broadcast=True
                            )
                            self.send_clients()
                        return

    def send_clients(self):
        self.send_message("{CLIENTS}" + self.get_clients_names(), broadcast=True)

    def get_clients_names(self, separator="|"):
        names = []
        for _, name in self.clients.items():
            names.append(name)
        return separator.join(names)

    def find_client_socket(self, name):
        for cli_sock, cli_name in clients.items():
            if cli_name == name:
                return cli_sock
        return None

    def send_message(self, msg, prefix="", destination=None, broadcast=False):
        print("message about depart {}".format(msg))
        send_msg = bytes(prefix + msg, "utf-8")
        self.counter -= 1
        # if broadcast:
        #     for sock in self.clients:
        #         """Broadcasts a message to all the clients."""
        #         sock.send(send_msg)
        # else:
        if destination:
            # ADD particular message header
            #
            try:
                destination.send(send_msg)
            except:
                raise IOError("destination error")


def run():

    clients = {}
    addresses = {}

    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument("--host", help="Host IP", default="127.0.0.1")
    parser.add_argument("--port", help="Port Number", default=33002)

    server_args = parser.parse_args()

    server = ChatServer(server_args.host, server_args.port)


if __name__ == "__main__":
    run()

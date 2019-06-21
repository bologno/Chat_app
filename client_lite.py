from socket import AF_INET, socket, SOCK_STREAM
import re


messages_test = {
    "welcome": '_send_message(tcpclient, "{REGISTER} %s" % user)',
    "goodbye": '_send_message(tcpclient, "{QUIT}")',
}


def _send_message(conn, msg):
    msg = "{}\n".format(msg)
    conn.send(msg.encode())


def run(message_key):
    assert message_key in messages_test, "Bad test validation message identifier."
    host = "127.0.0.1"
    port = 33002
    user = input("Enter client name: ")
    tcpclient = socket(AF_INET, SOCK_STREAM)
    tcpclient.connect((host, port))
    exec(messages_test[message_key])
    if check(tcpclient, message_key):
        return True
    else:
        return False
    # pick your message_test Key to execute desired test. ecex(messages_test["example"])


def check(socket, pattern):
    BUFFER_SIZE = 2048
    # host = socket.gethostname()
    while True:
        msg = socket.recv(BUFFER_SIZE)
        msg = msg.decode("utf-8")
        print("CLIENT " + msg)
        return re.search(pattern, msg.lower())


if __name__ == "__main__":
    run()

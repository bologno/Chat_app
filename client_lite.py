from socket import AF_INET, socket, SOCK_STREAM


def _send_message(conn, msg):
    msg = "{}\n".format(msg)
    conn.send(msg.encode())


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 33002
    user = "Ale"
    tcpclient = socket(AF_INET, SOCK_STREAM)
    tcpclient.connect((host, port))
    _send_message(tcpclient, "{REGISTER} %s" % user)
    _send_message(tcpclient, "{ALL} hello")
    _send_message(tcpclient, "{QUIT}")

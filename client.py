import socket

if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(("localhost", 8088))
    sock.sendall("hahah\n")
    sock.sendall('heiheihei')
    sock.close()
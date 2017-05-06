import socket
import siftsolve as ss


class Server:
    def __init__(self):
        self.siftSolve = ss.SiftSolve()

    def handle_request(self, client):
        while True:
            buf = client.recv(1024, 0)
            s = str(buf).strip("\n")
            print "recieve   " + s
            # s = client.makefile().readline().strip("\n")
            index = s.index("eof")
            if index != -1:
                s = s[0:index].strip("\n")
            if s == "":
                break
            try:
                result = self.siftSolve.main(s.split(" "))
                client.send("success\n")
                for res in result:
                    client.send(res + "\n")
                client.send("eof\n")
            except Exception as e:
                print e
                client.send("fail\neof\n")
                print "================================================"
            if index != -1:
                break
            print s
        print "stop the read"

    def main(self):
        sock = socket.socket()
        sock.bind(("localhost", 10001))
        sock.listen(5)
        while True:
            try:
                conn, address = sock.accept()
                print "recieve"
                self.handle_request(conn)
                conn.close()
            except Exception as e:
                print e


if __name__ == '__main__':
    Server().main()






















import socket, sys, select

addr = sys.argv[1]
port = int(sys.argv[2])
usr = sys.argv[3]

def client():
    clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    clisock.connect((addr, port))
    print("Connection established")

    while True:
        socket_list = [clisock, sys.stdin]
        iread, iwrite, error = select.select(socket_list, [], [])

        for s in iread:
            if s == clisock:
                data = s.recv(1024)
                if data:
                    sys.stdout.write(data)
                else:
                    print("Connection lost")
                    sys.exit()

            else:
                msg = sys.stdin.readline()
                clisock.send(msg)

if __name__ == "__main__":
    sys.exit(client())

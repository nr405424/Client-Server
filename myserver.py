import sys, select, socket

host = ''
port = sys.argv[1]

def server():
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.bind((host, port))
    serversock.listen(5)

    inputs = [serversock]
    clientlist = []

    while running:
        iread, iwrite, error = select.select[inputs, [], []]
        for s in iread:
            if s == serversock:
                client, addr = serversock.accept()
                inputs.append(client)
                clientlist.append(client)
            else:
                msg = s.recv()
                for client in clientlist:
                    client.send(msg)

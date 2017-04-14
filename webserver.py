import sys, select, socket, signal

HOST = ''
PORT = int(sys.argv[1])
PORTWEB = int(sys.argv[2])
inputs = []
weblist = []

# creer un socket server
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind((HOST, PORT))
serversock.listen(5)

# creer un socket pour le client web
websock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
websock.bind((HOST, PORTWEB))
websock.listen(5)


# pour qu'un utilisateur n'utilise pas "Me" comme username
def cleanlog():
    namelist = open("log.txt", "w")
    namelist.write("Me")
    namelist.close()



# pour reagir si l'utilisateur tape Ctrl-C
def handler(signum, frame):
    serversock.close()
    websock.close()
    sys.exit("\n ** Server disconnected. ** \n")
    
def myserver():
    cleanlog()
    inputs.append(serversock)
    inputs.append(websock)
    print("** Connected to server on port " + str(PORT) + " ** \n")

    while True:
        # pour gerer le Ctrl-C
        signal.signal(signal.SIGINT, handler)
        iread, iwrite, error = select.select(inputs, [], [])
        
        for s in iread:
            # si c'est une demande de connection
            if s == serversock:
                clisock, addr = serversock.accept()
                inputs.append(clisock)
                

            # si c'est un client web
            elif s == websock:
                webclisock, waddr = websock.accept()
                webmsg = """\
    HTTP/1.1 200 OK

    <!DOCTYPE html>
    <html>
    <header> <h3> LAST CHAT MESSAGES: </h3> </header>
    <body>
    <ul>
        <li>{}</li>
        <li>{}</li>
        <li>{}</li>
        <li>{}</li>
        <li>{}</li>
    </ul>
    </body>
    </html>
""".format(weblist[-5], weblist[-4], weblist[-3], weblist[-2], weblist[-1])
                
                webclisock.sendall(webmsg)
                webclisock.close()

            # si c'est un message par un client
            else:
                try:
                    msg = s.recv(4096)
                    if msg:
                        # pour montrer le msg de client dans le sortie standard du server
                        print(msg)
                        weblist.append(msg)
                        spread_msg(serversock, s, "\n" + msg)
                except:
                    s.close()
                    inputs.remove(s)
                    continue
                
    serversock.close()


# fonction utilise pour diffuser les messages des utilisateurs
def spread_msg(serversock, sock, mesg):
    for socket in inputs:
        # pour ne pas envoyer ni au client qui a envoye le msg, ni au socket server, ni au socket web
        if socket != serversock and socket != sock and socket != websock:
            try:
                socket.send(mesg)
            except:
                socket.close()
                if socket in clientlist:
                    inputs.remove(socket)

if __name__ == "__main__":
    sys.exit(myserver())

import sys, select, socket, signal

HOST = ''
PORT = int(sys.argv[1])
PORTWEB = int(sys.argv[2])
inputs = []
weblist = []
irclist = []
msglist = []

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



# pour avoir les bons arguments
def initargs():
    if len(sys.argv) != 3:
        print("[*] ERROR: python webserver.py <<PORT>> <<PORTWEB>>")
        sys.exit()

def webresp():
    msg = ""
    if (len(msglist) >= 5):
        for i in range(-5, 0):
            msg = msg + "\n <li>" + str(msglist[i]) + "</li>"
    else:
        for i in range(len(msglist),0,-1):
            msg = msg + "\n <li>" + str(msglist[-i]) + "</li>"
    return msg
    
def myserver():
    initargs()
    cleanlog()
    inputs.append(serversock)
    irclist.append(serversock)
    inputs.append(websock)
    weblist.append(websock)
    
    print("** Connected to server on port " + str(PORT) + " ** \n")

    while True:
        iread, iwrite, error = select.select(inputs, [], [])
        
        for s in iread:
            # si c'est une demande de connection
            if s == serversock:
                clisock, addr = serversock.accept()
                inputs.append(clisock)
                irclist.append(clisock)
                

            # si c'est un client web
            elif s == websock:
                webclisock, waddr = websock.accept()
                inputs.append(webclisock)
                weblist.append(webclisock)

            else:
                if s in weblist:
                    try:
                        webmsg = str(s.recv(4096))
                        if webmsg[:14] == "GET / HTTP/1.1" :
                            response = """\
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
<header> <h3> LAST CHAT MESSAGES: </h3> </header>
    <body>
    <ul>
        {}
    </ul>
    </body>
</html>
""".format(webresp())


                        else:
                            response = """\
HTTP/1.1 200 OK

<!DOCTYPE html>
    <html>
    <header> <h3> ERROR 404: Page not found. </h3> </header>
    </html>
"""
                
                        for wsock in weblist:
                            webclisock.sendall(response)
                            webclisock.close()
                            
                        

                    except:
                        s.close()
                        inputs.remove(s)
                        weblist.remove(s)
                        continue

                # si c'est un message par un client
                elif s in irclist:
                    try:
                        msg = s.recv(4096)
                        if msg:
                            # pour montrer le msg de client dans le sortie standard du server
                            print(msg)
                            msglist.append(msg)
                            spread_msg(serversock, s, "\n" + msg)
                    except:
                        s.close()
                        inputs.remove(s)
                        irclist.remove(s)
                        continue
                    
    serversock.close()
    websock.close()


# fonction utilise pour diffuser les messages des utilisateurs
def spread_msg(serversock, sock, mesg):
    for socket in irclist:
        # pour ne pas envoyer ni au client qui a envoye le msg, ni au socket server, ni au socket web
        if socket != serversock and socket != sock:
            try:
                socket.send(mesg)
            except:
                socket.close()
                if socket in irclist:
                    inputs.remove(socket)
                    irclist.remove(socket)



if __name__ == "__main__":
    sys.exit(myserver())

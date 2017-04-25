import socket, sys, select, signal

host = sys.argv[1]
port = int(sys.argv[2])
usr = []

#creer un socket client
clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
clisock.connect((host, port))


def intargs():
    if len(sys.argv) != 4:
        print("[*] ERROR: python myclient.py <<host>> <<port>> <<username>>")
        sys.exit()

# pour stocker le nom utilise dans un fichier "log.txt"
def addname(usr):
    name = usr
    f_in = open("log.txt", "r")
    # pour recuperer la liste des noms utilises et les mettre dans la variable namelist
    namelist = f_in.read().split()
    f_in.close

    # si le nom est deja utilise
    while name in namelist:
        name = raw_input("[*] This username is already taken. Please choose another one : ")

    # si le nom est bon, on l'ajoute dans le fichier "log.txt"
    f_name = open("log.txt", "a")
    f_name.write("\n" + name)
    f_name.close()

    return name


# pour enlever le nom du fichier txt (quand le client se deconnecte par exemple)
def rmvname():
    f_in = open("log.txt", "r")
    namelist = f_in.read().split()
    f_in.close()

    f_out = open("log.txt", "w")
    # enlever le nom qui correspond au client
    namelist.remove(usr[0])

    for name in namelist:
        # on met a jour le fichier "log.txt"
        f_out.write(name + "\n")
    f_out.close()

    
# pour reagir si le client tape Ctrl-C
def handler(signum, frame):
    print("\n" + "** You have left the chat room. ** \n")
    clisock.send("** " + usr[0] + " has left the chat room. ** \n")
    rmvname()
    clisock.close()
    sys.exit("\n ** Chat disconnected. **")
    

def client():
    intargs()
    print("** Connection established. **")
    sys.stdout.write("< Me > : "); sys.stdout.flush()
    usrname = sys.argv[3]
    usr.append(addname(usrname))
    clisock.send("** " + usr[0] + " entered the chat room. ** \n")

    # pour gerer le Ctrl-C
    while True:
        signal.signal(signal.SIGINT, handler)
        
        socket_list = [clisock, sys.stdin]
        iread, iwrite, error = select.select(socket_list, [], [])

        for s in iread:
            # si c'est un message
            if s == clisock:
                data = s.recv(4096)
                if data:
                    sys.stdout.write(data)
                    sys.stdout.write("< Me > : "); sys.stdout.flush()
                else:
                    print("\n ** Connection lost. **")
                    clisock.send("** " + usr[0] + " was disconnected. ** \n")
                    rmvname()
                    sys.exit()

            # si c'est le client qui est en train d'ecrire
            else:
                try:
                    msg = sys.stdin.readline()
                    clisock.send(usr[0] + " : " + msg)
                    sys.stdout.write("< Me > : "); sys.stdout.flush()
                except:
                    print("\n ** Connection lost. **")
                    clisock.send("** " + usr[0] + " was disconnected. ** \n")
                    rmvname()
                    sys.exit()


if __name__ == "__main__":
    sys.exit(client())

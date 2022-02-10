from socket import *
from threading import Thread
import sys
from time import sleep
from random import randint

def login(_socket, _address):
    _socket.send("Inserisci il tuo nome: ".encode("utf-8"))
    _name = _socket.recv(2048).decode("utf-8")
    _socket.send("logged-in".encode("utf-8"))
    return _socket, _address, _name

# cazzate = []
# chat_file = open("tordoaker.txt", mode="r")
# for l in chat_file:
#     line = l[23:]
#     if l.__contains__("Givanni Monea:"):
#         cazzate.append(l[37:])
# chat_file.close()
# print(len(cazzate))

commandInfo = {
    "[Utility]":"",
    "/help":"Visualizza una lista di tutti i comandi.",
    "/w <nome> <messaggio>":"Scrivi ad un solo giocatore",
    "/clear":"Ripulisci lo schermo",
    "/logout":"Esci dal gioco.",
    "/list":"Visulaizza una lista dei giocatori online al momento.",
    "[Altri comandi]":"",
    "/sino <domanda>":"No need to explain.",

    "/rettiliani":"Visualizza la probabilità che ciascun giocatore sia rettiliano"
}

#     "/gio":"Spara una cazzata.",

def helpcmd():
    prompt = ""
    for c in commandInfo:
        prompt = prompt + " -  {}  :  {}\n".format(c, commandInfo[c])
    return prompt
def broadcast(msg):
    for c in openConnections:
        openConnections[c][0].send(msg.encode("utf-8"))
def chat(sender, msg):
    for c in openConnections:
        if c != sender:
            openConnections[c][0].send("[{}] {}".format(sender, msg).encode("utf-8"))
def whisper(sender, recipient, message):
    if recipient in openConnections:
        openConnections[recipient][0].send("{}-->@you: {}".format(sender, message).encode("utf-8"))
    else:
        openConnections[sender][0].send("[Server] L'utente '{}' non è presente.".encode("utf-8"))
def sino():
    answer = ""
    if randint(0,1) == 0:
        answer = "Si"
    else:
        answer = "No"
    broadcast("[SINO] {}".format(answer))

openConnections = {}

def userlistener(user, sock):
    while True:
        message = sock.recv(2048).decode("utf-8")
        print("[{}] {}".format(user, message))
        if message.lower() == "/help":
            sock.send(helpcmd().encode("utf-8"))
        elif message.lower() == "/clear":
            sock.send("clear".encode("utf-8"))
        elif message.lower() == "/logout":
            sock.send("fin".encode("utf-8"))
            openConnections.pop(user)
            sock.close()
            broadcast("[Server] {} si è disconnesso. ({} utenti online)".format(user, len(openConnections)))
            break
        elif message.lower() == "/list":
            list = "[Giocatori online]\nAdmin: "
            for p in openConnections:
                list = list + p + "\n"
            sock.send(list.encode("utf-8"))
        elif message.split()[0].lower() == "/w":
            if len(message.split()) < 3:
                sock.send("[Server] Errore: ricontrolla la sintassi del comando".encode("utf-8"))
            else:
                splitmsg = message.split()
                splitmsg.pop(0)
                splitmsg.pop(0)
                msg = ""
                for m in splitmsg:
                    msg = msg + m + " "
                whisper(user, message.split()[1], msg)
        elif message.split()[0].lower() == "/sino":
            splitmsg = message.split()
            splitmsg.pop(0)
            msg = ""
            for m in splitmsg:
                msg = msg + m + " "
            chat(user, msg)
            sino()
        # elif message.lower() == "/gio":
        #     broadcast("[Gio] {}".format(cazzate[randint(0,len(cazzate))]))
        else:
            chat(user, message)


serverAddress = '127.0.0.1'
serverPort = 51140
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(3)
print("Server is online")

def newConnectionHandler(sock, addr):
    print("Nuova connessione con", addr)
    sock, addr, name = login(sock, addr)
    print("[Nuovo giocatore]",name)
    openConnections[name] = (sock, addr)
    sock.send("clear".encode("utf-8"))
    sleep(0.4)
    broadcast("[Server] {} si è unito alla partita ({} utenti online)".format(name, len(openConnections)))
    sock.send("[Server] Digita '/help' per una lista dei comandi.\n[Server] Per favore usa '/logout' se desideri uscire.".encode("utf-8"))
    listener = Thread(target=userlistener, args=[name,sock])
    listener.start()
    # thread per gestire gli eventi di gioco

# Game initialization
while True:
    newSocket, clientAddress = serverSocket.accept()
    thread = Thread(target=newConnectionHandler, args=[newSocket,clientAddress])
    thread.start()

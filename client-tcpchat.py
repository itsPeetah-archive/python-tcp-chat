from socket import *
from threading import Thread
from os import system, name as OSNAME
from tkinter import *

# window = Tk()
# e = Entry(window)
# e.focus_set()

# def entrycallback():
#     print (e.get()) # This is the text you may want to use later
#     e.delete(0, 'end')

# b = Button(window, text = "Invia", width = 10, command = entrycallback)
# e.pack(side=LEFT, expand=True, fill="x")
# b.pack(side=LEFT)

# def startInputWindow():
#     window.mainloop()

# windowthread = Thread(target=window.mainloop)
# windowthread.start()

def clear():
    if OSNAME == 'nt': # for windows
        system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        system('clear')

def login(_sock):
    while True:
        message = _sock.recv(2048).decode("utf-8")
        if  message == "logged-in":
            break
        else:
            print(message)
            _sock.send(input().encode("utf-8"))

def listen(clientSocket):
    while True:
        message = clientSocket.recv(2048).decode("utf-8")
        if message == "fin":
            clientSocket.close()
            print("\nTi sei disconnesso dal server")

            break;
        elif message == "clear":
            clear()
        else:
            print(message)
    clientSocket.close()

def speak(clientSocket):
    while True:
        message = input()
        clientSocket.send(message.encode("utf-8"))

serverAddress = '127.0.0.1'
serverPort = 51140

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverAddress, serverPort))

login(clientSocket)
listener = Thread(target=listen, args=[clientSocket])
listener.start()
speaker = Thread(target=speak, args=[clientSocket])
speaker.start()

import socket
import threading

HOST = "127.0.0.1"
PORT = 3000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

nome = input("Digite seu nome: ")
cliente.sendall(nome.encode("utf-8"))

#loop de envio de mensagens
while True:
    msg = input("> ")
    if msg:
        cliente.sendall(msg.encode("utf-8"))



    


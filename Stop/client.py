import socket

HOST = "127.0.0.1"
PORT = 3000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

while True:

    msg = cliente.recv(1024).decode("utf-8")
            
    if msg.endswith(": "):
        resposta = input(msg)
        cliente.sendall(resposta.encode("utf-8"))
    else:
        if msg:
            print(msg)




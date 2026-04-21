import socket

HOST = "127.0.0.1"
PORT = 3000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

#identificação
cliente.recv(1024)
cliente.sendall("Espectador".encode("utf-8"))
    
#loop de recebimento de mensagens
while True:
    msg_bytes = cliente.recv(1024)
    if msg_bytes:
        msg_texto = msg_bytes.decode("utf-8")
        print(msg_texto)


import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 3000

clientes = [] #lista de clientes conectados
semaforo = threading.Semaphore(1) #controlador de acesso a lista

def transmitir(mensagem):
    semaforo.acquire() #bloqueia a lista
    for cliente in clientes:
        try:
            cliente.sendall(mensagem.encode("utf-8"))
        except: 
            #em caso de erro ao enviar menagem ao cliente o remove da lista
            clientes.remove(cliente)
    semaforo.release() #libera a lista

def ligar_ao_chat(conn, addr):
    try:
        #identificação do cliente
        conn.sendall("Digite seu nome: ".encode("utf-8"))
        nome = conn.recv(1024).decode("utf-8")
        nome = nome.upper()
        
        #anuncio de conexão do cliente
        if nome != "Espectador":
            anuncio = f"[SERVER] {nome} entrou no chat!"
            print(anuncio)
            transmitir(anuncio)

        #loop de recebimento de mensagens do cliente
        while True:
            msg_bytes = conn.recv(1024)
            if msg_bytes:
                hora = datetime.now().strftime("%H:%M:%S")  
                msg_texto = msg_bytes.decode("utf-8")
                transmitir(f"{nome}, {addr}, {hora}: {msg_texto}")
            else:
                #caso o cliente se desconecte da conexão ele manda null
                break
    finally:
        #em caso de qualquer coisa que acabe com o loop infinito o cliente eh desconectado
        if conn in clientes:
            semaforo.acquire()
            clientes.remove(conn)
            semaforo.release()
        conn.close()
        

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para evitar o erro de porta em uso
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor de chat online na porta: {PORT}")

    while True:
        conn, addr = server.accept()

        semaforo.acquire()
        clientes.append(conn)
        semaforo.release()

        thread = threading.Thread(
            target=ligar_ao_chat,
            args=(conn, addr),
            daemon=True) #define que ao finalizar o codigo as threads também serão finalizadas
        thread.start()
    

if __name__ == "__main__":
    iniciar_servidor()
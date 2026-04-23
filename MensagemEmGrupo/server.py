import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 3000

clientes = [] #guarda as conexões que iram receber mensagens no servidor/espectadores
fila_mensagens = [] #fila de mensagens recebidas dos usuarios

semaforo_fila = threading.Semaphore(1) #para controlar o acesso das threads a fila de mensagens
itens_na_fila = threading.Semaphore(0) #para sinalizar se a algo na fila de mensgame
semaforo_clientes = threading.Semaphore(1) #para controlar a lista de conexões

#uma thread ficara nessa função esperando ateh q consiga dar um acquire em itens_na_fila = ter alguma mensagem na fila e enviara a mensagem a todos os espectadores
def processar_fila():
    while True:
        itens_na_fila.acquire()

        with semaforo_fila:
            msg = fila_mensagens.pop(0)

        with semaforo_clientes:
            for cliente in clientes:
                try:
                    cliente.sendall(msg.encode("utf-8"))
                except:
                    clientes.remove(cliente)


def atender_cliente(conn, addr):
    try:
        nome = conn.recv(1024).decode("utf-8").strip()

        #caso o nome do cliente seja espectador ele entrara no vetor de clientese esta pronto para receber mensagens
        if nome == "ESPECTADOR":
            with semaforo_clientes:
                clientes.append(conn)
            print(f"[SERVER] Cliente de RECEBIMENTO conectado: {addr}")

            while True:
                if not conn.recv(1024):
                    break
        #caso o nome seja qualquer outra coisa sera um cliente de envio, assim apenas podendo enviar mensagens ao servidor
        else:
            nome = nome.upper()
            print(f"[SERVER] Cliente de ENVIO conectado: {nome} {addr}")

            while True:
                msg_bytes = conn.recv(1024)
                if not msg_bytes:
                    break
                    
                msg_texto = msg_bytes.decode("utf-8")
                hora = datetime.now().strftime("%H:%M:%S")

                msg_final = f"[{hora}] {nome} ({addr[0]}): {msg_texto}"
                
                with semaforo_fila:
                    fila_mensagens.append(msg_final)

                itens_na_fila.release()
    #se o cliente espectador se desconectarem são removidos da lista
    finally:
        with semaforo_clientes:
            if conn in clientes:
                clientes.remove(conn)
        conn.close()
 

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para evitar o erro de porta em uso
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor de chat online na porta: {PORT}")

    thread_fila = threading.Thread(target=processar_fila, daemon=True)
    thread_fila.start()

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True)
        thread.start()
    

if __name__ == "__main__":
    iniciar_servidor()
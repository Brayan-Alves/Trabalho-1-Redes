import socket
import threading
import random
import string
import time

HOST = "127.0.0.1"
PORT = 3000
NUMERO_JOGADORES = 2
NUMERO_RODADAS = 2
ALFABETO = list(string.ascii_uppercase)

clientes = [] 
letras_sorteadas = []

nome = [None] * (NUMERO_JOGADORES + 1)
cep = [None] * (NUMERO_JOGADORES + 1)
fruta = [None] * (NUMERO_JOGADORES + 1)
pontos = [0] * (NUMERO_JOGADORES + 1)

semaforo = threading.Semaphore(1)
barreira = threading.Barrier(NUMERO_JOGADORES)
letra_atual = ""

def trasmitir(mensagem):
    for cliente in clientes:
        cliente.sendall(mensagem.encode("utf-8"))

def sortear_letra():
    letras_disponiveis = []

    for l in ALFABETO:
        if l not in letras_sorteadas:
            letras_disponiveis.append(l)

    letra = random.choice(letras_disponiveis)
    letras_sorteadas.append(letra)
    return letra

def contar_pontos(vetor, id):
    x = 3
    if(vetor[id] == ""):
        x = 0
    elif(vetor.count(vetor[id]) > 1):
        x = 1
    pontos[id] = pontos[id] + x
    return x

def analisar_vencedor():
    pontuação_maior = max(pontos)
    id_vencedor = pontos.index(pontuação_maior)
    anuncio_fim = (f"[SERVER] Fim de Jogo!\n[SERVER] O Vencedor foi o: Jogador {id_vencedor} com {pontuação_maior} pontos!\nPONTUAÇÂO:\nJogador 1 = {pontos[1]}\nJogador 2 = {pontos[2]}\n")
    trasmitir(anuncio_fim)

def iniciar_rodada(conn,addr,id):
    global letra_atual
    trasmitir(f"[SERVER] Jogador {addr} ID {id} está conectado!")
    print(f"[SERVER] Jogador {addr} ID {id} está conectado!")

    for x in range(1, NUMERO_RODADAS+1):

        if id == NUMERO_JOGADORES:
            letra_atual = sortear_letra()
            msg_inicio = (f"\n[SERVER] RODADA {x} INICIADA!\n[SERVER] LETRA ESCOLHIDA: {letra_atual}")
            trasmitir(msg_inicio)

        barreira.wait()

        conn.sendall("[SERVER] Rodada Começando em:".encode("utf-8"))
        for x in range(1, 11):
            conn.sendall(f"{11-x}\n".encode("utf-8"))
            time.sleep(1)
    
        conn.sendall("Nome: ".encode("utf-8"))
        nome[id] = conn.recv(1024).decode("utf-8")
        conn.sendall("Cep: ".encode("utf-8"))
        cep[id] = conn.recv(1024).decode("utf-8")
        conn.sendall("Fruta: ".encode("utf-8"))
        fruta[id] = conn.recv(1024).decode("utf-8")

        barreira.wait()

        with semaforo:
            pontos_rodada = contar_pontos(nome,id)
            pontos_rodada += contar_pontos(cep, id)
            pontos_rodada += contar_pontos(fruta, id)

        barreira.wait()

        letra_atual = ""

        msg_fim = (f"[SERVER] Jogador {id} (você) fez {pontos_rodada} pontos nessa rodada\n[SERVER] Pontuação Total: {pontos[id]}")
        conn.sendall(msg_fim.encode("utf-8"))


if id == NUMERO_JOGADORES:
    analisar_vencedor()
        
        


def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para evitar o erro de porta em uso
    server.bind((HOST, PORT))
    server.listen(NUMERO_JOGADORES)

    print(f"[SERVER] Servidor esperando {NUMERO_JOGADORES} Jogadores na porta: {PORT}")

    while len(clientes) < NUMERO_JOGADORES:
        conn, addr = server.accept()

        with semaforo:
            clientes.append(conn)
            id_atual = len(clientes)
        
        print(f"[SERVER] Aguardando {NUMERO_JOGADORES - id_atual} jogadores")

        thread = threading.Thread(target=iniciar_rodada, args=(conn, addr, id_atual))
        thread.start()

    while True:
        pass

    

if __name__ == "__main__":
    iniciar_servidor()
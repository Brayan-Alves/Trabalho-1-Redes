import socket
import threading
import random
import string
import time
from datetime import datetime

HOST = "127.0.0.1"
PORT = 3000
NUMERO_JOGADORES = 2
NUMERO_RODADAS = 2
ALFABETO = list(string.ascii_uppercase)

clientes = []

nomes = [""] * NUMERO_JOGADORES
ips = [""] * NUMERO_JOGADORES

tema_nome = [None] * NUMERO_JOGADORES
tema_cep = [None] * NUMERO_JOGADORES
tema_musica = [None] * NUMERO_JOGADORES
pontos = [0] * NUMERO_JOGADORES
letras_sorteadas = []

semaforo = threading.Semaphore(1)
barreira = threading.Barrier(NUMERO_JOGADORES)
letra_atual = ""

def trasmitir(mensagem):
    for cliente in clientes:
        try:
            cliente.sendall(f"{mensagem}\n".encode("utf-8"))
        except:
            pass

def formatar_mensagem(id_jogador, texto):
    horario = datetime.now().strftime("%H:%M:%S")
    nome = nomes[id_jogador]
    ip = ips[id_jogador]
    return f"[{horario}] {nome} ({ip}): {texto}"

def sortear_letra():
    letras_disponiveis = [l for l in ALFABETO if l not in letras_sorteadas]
    letra = random.choice(letras_disponiveis)
    letras_sorteadas.append(letra)
    return letra

def contar_pontos(vetor, id_jogador, letra):
    resposta = vetor[id_jogador].strip().upper()

    if not resposta or not resposta.startswith(letra):
        return 0
    
    ocorrencias = sum(1 for r in vetor if r.strip().upper() == resposta)

    if ocorrencias > 1:
        pontos[id_jogador] += 1
        return 1
    else:
        pontos[id_jogador] == 3
        return 3

def analisar_vencedor():
    pontuação_maior = max(pontos)
    id_vencedor = pontos.index(pontuação_maior)
    nome_vencedor = nomes[id_vencedor]


    anuncio_fim = (f"\n--- Fim de Jogo! ---\nVencedor: {nome_vencedor} com {pontuação_maior} pontos!\n--- Placar Final ---")
    for i in range(NUMERO_JOGADORES):
        anuncio_fim += f"{nomes[i]} = {pontos[i]} pontos\n"

    trasmitir(anuncio_fim)


def iniciar_rodada(conn,addr,id_jogador):
    global letra_atual

    conn.sendall("Digite seu Nome: ".encode("utf-8"))
    nome_recebido = conn.recv(1024).decode("utf-8").strip()

    with semaforo:
        nomes[id_jogador] = nome_recebido
        ips[id_jogador] = addr[0]

    msg_conexao = formatar_mensagem(id_jogador, "Entrou na partida!")
    trasmitir(msg_conexao)
    print(msg_conexao)

    barreira.wait()

    for x in range(1, NUMERO_RODADAS+1):

        if id_jogador == 0:
            letra_atual = sortear_letra()
            msg_inicio = (f"\n--- Rodada {x} ---\nLetra Escolhida = {letra_atual}")
            trasmitir(msg_inicio)

        barreira.wait()

        conn.sendall("Rodada Começando em...\n".encode("utf-8"))
        for x in range(5, 0, -1):
            conn.sendall(f"{x}\n".encode("utf-8"))
            time.sleep(1)
    
        conn.sendall("NOME: ".encode("utf-8"))
        resp_nome = conn.recv(1024).decode("utf-8")
        conn.sendall("CEP: ".encode("utf-8"))
        resp_cep = conn.recv(1024).decode("utf-8")
        conn.sendall("MÚSICA: ".encode("utf-8"))
        resp_musica = conn.recv(1024).decode("utf-8")

        with semaforo:
            tema_nome[id_jogador] = resp_nome
            tema_cep[id_jogador] = resp_cep
            tema_musica[id_jogador] = resp_musica

        barreira.wait()

        with semaforo:
            pts_rodada = 0
            pts_rodada += contar_pontos(tema_nome, id_jogador, letra_atual)
            pts_rodada += contar_pontos(tema_cep, id_jogador, letra_atual)
            pts_rodada += contar_pontos(tema_musica, id_jogador, letra_atual)
            pontos[id_jogador] = pts_rodada

        barreira.wait()

        msg_fim = formatar_mensagem(id_jogador, f"Fez {pts_rodada} pontos na rodada. Total: {pontos[id_jogador]}")
        conn.sendall(msg_fim.encode("utf-8"))

        with semaforo:
            tema_nome[id_jogador] = ""
            tema_cep[id_jogador] = ""
            tema_musica[id_jogador] = ""

        barreira.wait()

    if id_jogador == 0:
        analisar_vencedor()


if id == NUMERO_JOGADORES:
    analisar_vencedor()
        
    

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para evitar o erro de porta em uso
    server.bind((HOST, PORT))
    server.listen(NUMERO_JOGADORES)

    print(f"[SERVER] Servidor esperando {NUMERO_JOGADORES} Jogadores em  {HOST}:{PORT}")

    while len(clientes) < NUMERO_JOGADORES:
        conn, addr = server.accept()

        with semaforo:
            clientes.append(conn)
            id_atual = len(clientes) - 1
        
        print(f"[SERVER] Conexão recebida de {addr[0]}, aguardando {NUMERO_JOGADORES - (id_atual+1)} jogadores")

        thread = threading.Thread(target=iniciar_rodada, args=(conn, addr, id_atual))
        thread.start()

    while True:
        pass

    

if __name__ == "__main__":
    iniciar_servidor()
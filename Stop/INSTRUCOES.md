# Sistema de STOP

## O quê é esse projeto?

Este sistema foi desenvilvido com o objetivo de criar um jogo STOP usando conhecimentos adquiridos nas aulas de Redes, como sockets e threads. O sistema é composto por dois arquivos, o servidor que atua gerenciando o sorteio de letras, a sincronização do tempo entre os jogadores e o cálculo da pontuação; E o cliente que envia as respostas.

## Arquivos
- **client.py**: Interface para o usuário enviar suas respostas.
- **server.py**: Arquivo que centraliza as conexões, gerencia o sorteio de letras e calcula a pontuação.

## Instruções para rodar o STOP

Primeiramente deve-se verificar se o endereço em `HOST` é o mesmo em todos os arquivos. Após essa verificação você deve:

1. No terminal execute o comando `python3 server.py` para executar o arquivo do servidor.
  ```bash
  python3 server.py
  ```

2. Em seguida execute o comando `python3 client.py` em outro terminal para entrar no jogo como jogador 1.
  ```bash
  python3 client.py
  ```

3. Em seguida execute o comando `python3 client.py` em outro terminal para entrar no jogo como jogador 2.
  ```bash
  python3 client.py
  ```

## Observações
Este arquivo está pré-instanciado para 2 jogadores, caso queira adicionar mais jogadores, entre no arquivo `server.py`, encontre a variavél global `NUMERO_JOGADORES` e altere para a quantidade de jogadores que desejam jogar. Lembre-se que para cada jogador você deve rodar o comando `python3 client.py` em um novo terminal.
  ```bash
  python3 client.py
  ```
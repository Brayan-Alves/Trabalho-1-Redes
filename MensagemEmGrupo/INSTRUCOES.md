# Sistema de Chat

## O quê é este projeto?

Este sistema foi desenvolvido com o objetivo de criar um grupo de conversa usando conhecimentos adquiridos nas aulas de Redes, como sockets e threads. O sistema é composto por três arquivos, sendo um servidor que gerencia as mensagens e dois tipos de clientes, um para envio e outro para visualização.

## Arquivos
- **clientEnv.py**:  Interface para o usuário enviar textos.
- **clientRec.py**: Terminal focado em receber mensagens já formatadas.
- **server.py**: Arquivo que centraliza as conexões e gerencia a fila de mensagens.

## Instruções para rodar Mensagem em Grupo

Primeiramente deve-se verificar se o endereço em `HOST` é o mesmo em todos os arquivos. Após essa verificação você deve:

1. No terminal execute o comando `python3 server.py` para executar o arquivo do servidor.
  ```bash
  python3 server.py
  ```

2. Em seguida execute o comando `python3 clientRec.py` no terminal para abrir a tela de recebimento de mensagens.
  ```bash
  python3 clientRec.py
  ```

3. Agora execute o comando `python3 clienteEnv.py` no terminal, digite um nome e começe a enviar suas mensagens de texto pelo terminal.
  ```bash
  python3 clienteEnv.py
  ```
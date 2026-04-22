# Jogo de STOP

Este projeto implementa uma versão multiplayer do jogo **STOP**, com comunicação cliente-servidor.

O servidor atua como **mestre da partida**, sendo responsável por:

* Sortear as letras
* Sincronizar o tempo entre jogadores
* Avaliar respostas e calcular pontuações

## Estrutura do Projeto

### `server.py`

Responsável por:

* Sortear as letras de cada rodada
* Sincronizar os jogadores (início e fim simultâneo)
* Receber respostas dos clientes
* Calcular e exibir a pontuação

### `client.py`

Interface de terminal para o jogador:

* Recebe a letra sorteada
* Solicita o preenchimento das respostas
* Envia os dados para o servidor

## Configuração

Antes de executar, verifique:

* **HOST**: Defina no `client.py` o IP do servidor
* **Parâmetros do jogo** (no topo dos arquivos):

  * `N_J`: Número de jogadores (padrão: 2)
  * `N_R`: Número de rodadas (padrão: 3)

## Como Executar

### 1. Iniciar o Servidor

No terminal, navegue até a pasta do projeto e execute:

```bash
python3 server.py
```

O servidor ficará aguardando até que todos os jogadores se conectem.

### 2. Iniciar os Clientes

Para cada jogador, abra um novo terminal e execute:

```bash
python3 client.py
```

## Fluxo do Jogo

### Início da Rodada

* Após todos os jogadores conectarem
* O servidor sorteia uma letra e envia para todos

---

###  Preenchimento

Cada jogador deve preencher os seguintes campos:

* **Nome**
* **CEP**
* **Professor**
* **Cor**

---

### Pontuação

Cada resposta é avaliada da seguinte forma:

* **3 pontos** → Resposta válida e única
* **1 ponto** → Resposta válida, mas repetida
* **0 pontos** → Resposta vazia ou inválida

---

### Resultados

* A pontuação acumulada é exibida ao final de cada rodada
* Ao final da última rodada, o vencedor é anunciado

## Observações

* O jogo é sincronizado: todos começam e terminam juntos
* O servidor garante consistência na avaliação das respostas
* Ideal para ser executado em rede local (LAN)
# API de Controle de Botões e Joystick com Flask e SocketIO

Esta API foi desenvolvida para permitir o controle e monitoramento de botões e um joystick, com comunicação em tempo real utilizando Flask e SocketIO. A API é simples e permite que os dados de entrada (status dos botões e coordenadas do joystick) sejam enviados para o servidor e exibidos em um painel web.

## Funcionalidades

- **Recepção de Dados**: A API recebe dados via POST e os transmite em tempo real via WebSocket.
- **Status dos Botões**: Exibe o status dos botões (pressionados ou soltos).
- **Status do Joystick**: Exibe as coordenadas do joystick (X, Y) e a direção.

## Estrutura do Projeto

O projeto possui a seguinte estrutura de arquivos:
/Projeto
├── Procfile # Arquivo utilizado para deploy em plataformas como Heroku
├── app.py # Arquivo principal da API
├── requirements.txt # Dependências do projeto

### Arquivo `Procfile`

O `Procfile` é necessário para deploy em plataformas como o **Heroku**. Ele define o comando de execução do servidor. O conteúdo do arquivo é:

web: python app.py

### Arquivo `app.py`

O arquivo `app.py` contém a lógica principal da API. Ele define as rotas e configura a comunicação entre o servidor e os clientes via HTTP e WebSocket.

### Arquivo `requirements.txt`

Este arquivo lista as bibliotecas Python necessárias para rodar o projeto. O conteúdo do arquivo é:
flask
flask-socketio
eventlet

Essas dependências podem ser instaladas usando o `pip`.

## Como Configurar e Rodar a API

### 1. Instalar as Dependências

Primeiro, instale as dependências do projeto. Certifique-se de que o **pip** esteja instalado em sua máquina.

- Abra um terminal e navegue até o diretório do projeto.
- Instale as dependências com o comando:

```bash
pip install -r requirements.txt
```
Executar o Servidor:
Após a instalação das dependências, inicie o servidor com o comando:
python app.py
O servidor estará rodando localmente na porta 10000 (ou na porta definida pela variável de ambiente PORT).

Testar a API:
POST /dados
Esta rota recebe dados em formato JSON. Os dados enviados serão transmitidos para todos os clientes conectados via WebSocket.
Exemplo de corpo da requisição:
{
  "botao_a": 1,
  "botao_b": 0,
  "x": 50,
  "y": 30,
  "direcao": "Norte"
}
botao_a: Status do Botão A (1 = pressionado, 0 = solto)
botao_b: Status do Botão B (1 = pressionado, 0 = solto)
x: Coordenada X do joystick
y: Coordenada Y do joystick
direcao: Direção do joystick (ex.: "Norte", "Sul", "Leste", "Oeste")

GET /dashboard/botoes
Esta rota exibe o status dos botões (A e B). O status é atualizado em tempo real quando os dados são recebidos na rota /dados.
Para visualizar o status dos botões, acesse:
switchback.proxy.rlwy.net:23445/dashboard/botoes #O localhost é fornecido pela plataforma Railway.

Comunicação em Tempo Real (WebSocket):
Quando os dados são enviados para a rota /dados, todos os clientes conectados ao servidor via WebSocket receberão os dados automaticamente. O servidor envia os dados para os clientes através do evento novo_dado, que é tratado pelo JavaScript no lado do cliente.

Cliente (HTML/JS)
No painel web, o JavaScript escuta o evento novo_dado e atualiza o status dos botões e do joystick em tempo real.
const socket = io();  // Inicia a conexão com o servidor WebSocket

socket.on("novo_dado", function(dado) {
    // Atualiza o status dos botões
    const botaoA = document.getElementById("status_botao_a");
    const botaoB = document.getElementById("status_botao_b");

    updateStatus(botaoA, dado.botao_a);
    updateStatus(botaoB, dado.botao_b);
});

function updateStatus(element, status) {
    element.className = "status";
    if (status === 1) {
        element.innerText = "Pressionado!";
        element.classList.add("pressed");
    } else if (status === 0) {
        element.innerText = "Solto";
        element.classList.add("released");
    } else {
        element.innerText = "N/A";
        element.classList.add("unknown");
    }
}

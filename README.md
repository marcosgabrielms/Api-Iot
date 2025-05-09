# API de Controle de Botões e Joystick

API para controle e monitoramento de botões e joystick com Flask e SocketIO. Os dados de status dos botões e coordenadas do joystick são recebidos e exibidos em tempo real em um painel web.

## Funcionalidades

- **Recepção de Dados**: Recebe dados via POST e transmite via WebSocket.
- **Status dos Botões**: Exibe se os botões estão pressionados ou soltos.
- **Status do Joystick**: Exibe as coordenadas (X, Y) e direção do joystick.

## Estrutura do Projeto
/Projeto
├── Procfile # Arquivo para deploy em plataformas como Heroku
├── app.py # Arquivo principal da API
├── requirements.txt # Dependências do projeto


### Dependências

As dependências necessárias estão no arquivo `requirements.txt`:
flask
flask-socketio
eventlet


Instale as dependências com:

```bash
pip install -r requirements.txt
```
Como Rodar
Instale as dependências com pip install -r requirements.txt.
Execute o servidor com:
python app.py

Endpoints
POST /dados
Recebe os dados dos botões e joystick em formato JSON e transmite via WebSocket.

Exemplo de dados:
{
  "botao_a": 1,
  "botao_b": 0,
  "x": 50,
  "y": 30,
  "direcao": "Norte"
}

GET /dashboard/botoes
Exibe o status dos botões (A e B), que é atualizado em tempo real.

Acesse: switchback.proxy.rlwy.net:23445/dashboard/botoes

WebSocket (Tempo Real)
Os dados enviados via /dados são transmitidos para todos os clientes conectados via WebSocket. A comunicação é feita usando o evento novo_dado e é tratada no cliente com JavaScript.

Código do cliente (HTML/JS):
const socket = io();  // Conecta ao servidor WebSocket

socket.on("novo_dado", function(dado) {
    // Atualiza status dos botões
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

Deploy
Se for usar em Heroku ou outra plataforma, o arquivo Procfile define o comando para iniciar o servidor:
web: python app.py


# Importando as bibliotecas necessárias para o funcionamento do aplicativo
from flask import Flask, request, render_template_string  # Flask é usado para criar o servidor web
from flask_socketio import SocketIO, emit  # SocketIO para comunicação em tempo real via WebSockets
import os  # Para manipulação de variáveis de ambiente (como a porta)

# Criando uma instância do Flask para o servidor web
app = Flask(__name__)
# Configurando o SocketIO para o aplicativo Flask
socketio = SocketIO(app, cors_allowed_origins="*")

# Variável global para armazenar o último dado recebido via POST
ultimo_dado = {}

# Rota para receber dados via POST
@app.route('/dados', methods=['POST'])
def receber_dados():
    global ultimo_dado
    # Recebendo os dados em formato JSON
    data = request.json
    ultimo_dado = data  # Atualizando os dados recebidos
    print(f"Dados recebidos: {data}")  # Exibindo no console
    # Emitindo os dados para os clientes conectados via WebSocket
    socketio.emit('novo_dado', data)
    # Retornando resposta de sucesso
    return {"Status": "ok"}, 200

# Rota para exibir o status dos botões
@app.route('/dashboard/botoes')
def dashboard_botoes():
    global ultimo_dado
    # HTML para exibição do status dos botões
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Status dos Botões</title>
        <script src="https://cdn.socket.io/4.4.1/socket.io.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background-color: #ffffff;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 400px;
                width: 100%;
            }
            h1 {
                color: #333;
            }
            .status {
                font-weight: bold;
                color: #007BFF;
            }
            .pressed { color: #28a745; }
            .released { color: #dc3545; }
            .unknown { color: #6c757d; }
        </style>
        <script>
            const socket = io();  // Iniciando a conexão WebSocket

            socket.on("novo_dado", function(dado) {
                // Atualizando o status dos botões com base nos dados recebidos
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
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Status dos Botões</h1>
            <p><strong>Botão A:</strong> <span id="status_botao_a" class="status">--</span></p>
            <p><strong>Botão B:</strong> <span id="status_botao_b" class="status">--</span></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

# Rota para exibir o status do joystick
@app.route('/dashboard/joystick')
def dashboard_joystick():
    global ultimo_dado
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Status do Joystick</title>
        <meta http-equiv="refresh" content="1">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .box {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                padding: 30px 40px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h1 { color: #333333; }
            p { font-size: 1.2em; color: #555555; }
            strong { color: #0077cc; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Status do Joystick</h1>
            <p><strong>X:</strong> {{ x }}</p>
            <p><strong>Y:</strong> {{ y }}</p>
            <p><strong>Direção:</strong> {{ direcao }}</p>
        </div>
    </body>
    </html>
    """
    # Pegando os dados do joystick
    x = ultimo_dado.get("x", "N/A")
    y = ultimo_dado.get("y", "N/A")
    direcao = ultimo_dado.get("direcao", "N/A")

    return render_template_string(html, x=x, y=y, direcao=direcao)

# Rodando o servidor
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Usando a porta especificada ou 10000 como padrão
    socketio.run(app, host='0.0.0.0', port=port)  # Iniciando o SocketIO para comunicação em tempo real

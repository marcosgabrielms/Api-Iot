from flask import Flask, request, render_template_string
from flask_socketio import SockeIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

ultimo_dado = {}

@app.route('/dados', methods = ['POST'])

def receiver():
    global ultimo_dado
    data= request.json
    ultimo_dado = data
    print(f"Dados recebidos: {data}")
    return{"Status": "ok"}, 200

@app.route('/dashboard/botoes')
def dashboard_botoes():
    global ultimo_dado
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
            transition: transform 0.3s ease;
        }

        .container:hover {
            transform: translateY(-5px);
        }

        h1 {
            color: #333;
            margin-bottom: 24px;
            font-size: 28px;
        }

        p {
            font-size: 18px;
            color: #555;
        }

        .status {
            font-weight: bold;
            color: #007BFF;
            transition: color 0.3s ease;
        }

        .pressed {
            color: #28a745;
        }

        .released {
            color: #dc3545;
        }

        .unknown {
            color: #6c757d;
        }
    </style>
    <script>
        const socket = io();

        socket.on("novo_dado", function(dado) {
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
        h1 {
        color: #333333;
        margin-bottom: 20px;
        }
        p {
        font-size: 1.2em;
        color: #555555;
        margin: 10px 0;
        }
        strong {
        color: #0077cc;
        }
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

    x =  ultimo_dado.get("x", "N/A")
    y = ultimo_dado.get("y", "N/A")
    direcao =  ultimo_dado.get("direcao", "N/A")

    return render_template_string(html, x=x, y=y, direcao=direcao)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host= '0.0.0.0', port=port)


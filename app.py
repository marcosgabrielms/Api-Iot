from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

ultimo_dado = {}

@app.route('/dados', methods = ['POST'])

def receiver():
    global ultimo_dado
    data= request.json
    ultimo_dado = data
    print(f"Dados recebidos: {data}")
    return{"Status": "ok"}, 200

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
    port = int(os.environ.get("PORT, 10000"))
    app.run(host= '0.0.0.0', port=port)


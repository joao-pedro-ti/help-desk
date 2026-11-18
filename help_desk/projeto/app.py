# app.py — 1 única função (a rota). Tudo inline.
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.secret_key = "chave_secreta_chamados"
CORS(app)


MENU = [
    "1- Não consigo abrir o aplicativo da loja.",
    "2- O aplicativo da loja está fora do ar.",
    "3- Não consigo enviar um anexo por meio do aplicativo da loja."
]


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chamado", methods=["POST"])
def chamado():
    data = request.get_json() or {}
    abrir_chamado = bool(data.get("abrir_chamado", False))
    duvida = data.get("duvida", None)
    etapa = data.get("etapa", "inicio")

    if etapa == "inicio":
        if not abrir_chamado:
            return jsonify({"status": "encerrado", "mensagem": "Programa encerrado."})
        return jsonify({
            "status": "menu",
            "mensagem": "Olá, usuário (a)! Qual é a sua dúvida? Selecione uma das opções abaixo:",
            "opcoes": MENU
        })

    if not abrir_chamado:
        return jsonify({"status": "encerrado", "mensagem": "Programa encerrado."})

    try:
        duvida = int(duvida)
    except (ValueError, TypeError):
        duvida = -1

    if etapa in ("menu", "aninhado"):

        if duvida == 1:
            solucao = ("A solução é: Verifique se o aplicativo da loja está instalado "
                       "corretamente e atualizado. Reinicie o dispositivo, confira se há "
                       "espaço de armazenamento disponível e tente abrir novamente. Se o "
                       "erro persistir, desinstale e reinstale o app pela loja oficial.")
            try:
                db = mysql.connector.connect(host="localhost", user="root",
                                             password="sua_senha", database="chamados_db")
                cursor = db.cursor()
                cursor.execute("INSERT INTO chamados (duvida, solucao) VALUES (%s, %s)",
                               (duvida, solucao))
                db.commit(); cursor.close(); db.close()
            except Exception as e:
                print(f"Erro DB: {e}")
            return jsonify({"status": "solucao", "solucao": solucao, "mensagem": solucao,
                            "perguntar_novo": True,
                            "pergunta_novo": "Você deseja abrir um novo chamado?:"})

        elif duvida == 2:
            solucao = ("A solução é: O aplicativo da loja está fora do ar por manutenção "
                       "ou instabilidade nos servidores. Aguarde alguns minutos e tente "
                       "novamente. Você pode acompanhar o status oficial pelos canais de "
                       "comunicação da loja.")
            try:
                db = mysql.connector.connect(host="localhost", user="root",
                                             password="sua_senha", database="chamados_db")
                cursor = db.cursor()
                cursor.execute("INSERT INTO chamados (duvida, solucao) VALUES (%s, %s)",
                               (duvida, solucao))
                db.commit(); cursor.close(); db.close()
            except Exception as e:
                print(f"Erro DB: {e}")
            return jsonify({"status": "solucao", "solucao": solucao, "mensagem": solucao,
                            "perguntar_novo": True,
                            "pergunta_novo": "Você deseja abrir um novo chamado?:"})

        elif duvida == 3:
            solucao = ("A solução é: Verifique o tamanho e o formato do arquivo (há limite "
                       "de tamanho e extensões permitidas). Confirme se sua conexão com a "
                       "internet está estável, se o aplicativo tem permissão de acesso aos "
                       "arquivos e tente enviar novamente. Se o problema continuar, envie "
                       "o anexo por outro canal de atendimento.")
            try:
                db = mysql.connector.connect(host="localhost", user="root",
                                             password="sua_senha", database="chamados_db")
                cursor = db.cursor()
                cursor.execute("INSERT INTO chamados (duvida, solucao) VALUES (%s, %s)",
                               (duvida, solucao))
                db.commit(); cursor.close(); db.close()
            except Exception as e:
                print(f"Erro DB: {e}")
            return jsonify({"status": "solucao", "solucao": solucao, "mensagem": solucao,
                            "perguntar_novo": True,
                            "pergunta_novo": "Você deseja abrir um novo chamado?:"})

        else:
            if etapa == "menu":
                return jsonify({"status": "erro", "mensagem": "Erro! Tente novamente.",
                                "menu_mensagem": "Olá, usuário (a)! Qual é a sua dúvida? Selecione uma das opções abaixo:",
                                "opcoes": MENU, "proxima_etapa": "aninhado"})
            return jsonify({"status": "erro_final", "mensagem": "Erro! Tente novamente.",
                            "menu_mensagem": "Olá, usuário (a)! Qual é a sua dúvida? Selecione uma das opções abaixo:",
                            "opcoes": MENU, "proxima_etapa": "aninhado"})

    if etapa == "novo":
        if abrir_chamado:
            return jsonify({"status": "menu",
                            "mensagem": "Olá, usuário (a)! Qual é a sua dúvida? Selecione uma das opções abaixo:",
                            "opcoes": MENU, "proxima_etapa": "menu"})
        return jsonify({"status": "encerrado", "mensagem": "Programa encerrado."})

    return jsonify({"status": "encerrado", "mensagem": "Programa encerrado."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
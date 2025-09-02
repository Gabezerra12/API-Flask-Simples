from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

usuarios = []
id_atual = 1
_id_lock = threading.Lock()

def gerar_id():
    global id_atual
    with _id_lock:
        atual = id_atual
        id_atual += 1
        return atual

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "API ativa. Use /users para operar."}), 200

@app.route("/users", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400

    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()

    if not nome or not email:
        return jsonify({"erro": "Campos 'nome' e 'email' são obrigatórios"}), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"erro": "Email inválido"}), 400

    for u in usuarios:
        if u.get("email") == email:
            return jsonify({"erro": "E-mail já cadastrado"}), 400

    novo_usuario = {
        "id": gerar_id(),
        "nome": nome,
        "email": email
    }
    usuarios.append(novo_usuario)
    return jsonify(novo_usuario), 201

@app.route("/users", methods=["GET"])
def listar_usuarios():
    return jsonify(usuarios), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def buscar_usuario(user_id):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return jsonify(usuario), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route("/users/<int:user_id>", methods=["PUT"])
def atualizar_usuario(user_id):
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400

    if not any(k in dados for k in ("nome", "email")):
        return jsonify({"erro": "É necessário informar ao menos 'nome' ou 'email'"}), 400

    for usuario in usuarios:
        if usuario["id"] == user_id:
            if "email" in dados:
                novo_email = (dados.get("email") or "").strip().lower()
                if not novo_email:
                    return jsonify({"erro": "Email inválido"}), 400
                if "@" not in novo_email or "." not in novo_email.split("@")[-1]:
                    return jsonify({"erro": "Email inválido"}), 400
                for u in usuarios:
                    if u.get("email") == novo_email and u["id"] != user_id:
                        return jsonify({"erro": "E-mail já cadastrado por outro usuário"}), 400
                usuario["email"] = novo_email

            if "nome" in dados:
                novo_nome = (dados.get("nome") or "").strip()
                if not novo_nome:
                    return jsonify({"erro": "Nome inválido"}), 400
                usuario["nome"] = novo_nome

            return jsonify(usuario), 200

    return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def deletar_usuario(user_id):
    for i, usuario in enumerate(usuarios):
        if usuario["id"] == user_id:
            usuarios.pop(i)
            return jsonify({"mensagem": "Usuário excluído com sucesso"}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)

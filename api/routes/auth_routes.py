from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database_manager import add_user_app, login_user_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['nome', 'cpf', 'email', 'senha']
    
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Todos os campos sao obrigatorios"}), 400

    senha_hash = generate_password_hash(data['senha'])
    add_user_app(data['nome'], data['email'], data['cpf'], senha_hash)

    return jsonify({"message": "Usuario cadastrado com sucesso"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"error": "Email e senha sao obrigatorios"}), 400

    if not login_user_app(email, senha):
        return jsonify({"error": "Email ou senha invalidos"}), 401

    return jsonify({"message": "Login realizado com sucesso!"}), 200

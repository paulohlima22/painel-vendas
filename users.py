import json
import os
from werkzeug.security import generate_password_hash

USERS_FILE = 'users.json'

def carregar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    with open(USERS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=4)

# Código utilitário para terminal
if __name__ == '__main__':
    senha = input("Digite a nova senha: ")
    email = input("Email do usuário: ")
    usuarios = carregar_usuarios()
    usuarios[email] = generate_password_hash(senha)
    salvar_usuarios(usuarios)
    print("Senha cadastrada ou atualizada com sucesso.")

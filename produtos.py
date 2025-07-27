import json
import os

ARQUIVO = 'produtos.json'

def carregar_produtos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_produtos(produtos):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

def adicionar_produto(nome, preco, descricao, link):
    produtos = carregar_produtos()
    novo_produto = {
        'nome': nome,
        'preco': preco,
        'descricao': descricao,
        'link': link
    }
    produtos.append(novo_produto)
    salvar_produtos(produtos)

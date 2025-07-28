import json
import os

ARQUIVO = 'anuncios.json'

# Carrega todos os anúncios do arquivo
def carregar_anuncios():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

# Salva a lista de anúncios atualizada
def salvar_anuncios(anuncios):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(anuncios, f, ensure_ascii=False, indent=4)

# Adiciona um novo anúncio à lista
def adicionar_anuncio(nome_produto, anunciante, descricao, link, imagem, email):
    anuncios = carregar_anuncios()
    novo_anuncio = {
        'nome_produto': nome_produto,
        'anunciante': anunciante,
        'descricao': descricao,
        'link': link,
        'imagem': imagem,       # nome do arquivo da imagem
        'email': email          # quem cadastrou o anúncio
    }
    anuncios.append(novo_anuncio)
    salvar_anuncios(anuncios)

# Retorna apenas anúncios cadastrados por um usuário específico
def anuncios_por_usuario(email):
    return [a for a in carregar_anuncios() if a.get('email') == email]

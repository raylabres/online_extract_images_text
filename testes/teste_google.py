import requests

def chat_google(pergunta):
    api_key = "AIzaSyAJUhVyf0DPEzzyp8f6GkK7h6XLBOt-khc"  # Substitua com sua chave da API Google
    search_engine_id = "620059450bef245a5"  # Substitua com o ID do mecanismo de busca
    endpoint = "https://www.googleapis.com/customsearch/v1"

    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': pergunta,
    }

    resposta = requests.get(endpoint, params=params)
    resultado = resposta.json()

    # Extrai os títulos e links dos resultados
    resposta_formatada = ""
    if 'items' in resultado:
        for i, item in enumerate(resultado['items'][:5]):
            resposta_formatada += f"{i + 1}. {item['title']}\n{item['link']}\n\n"
    else:
        resposta_formatada = "Nenhum resultado encontrado."

    print(f'\033[1;34m{resposta_formatada}')
    return resposta_formatada

# Exemplo de uso
chat_google("O que é Python?")

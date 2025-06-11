import os
import numpy as np
import shutil
from fpdf import FPDF
from PIL import Image, ImageEnhance
import requests
import json
import ast

# Variáveis úteis
base_diretorio = f"{os.getcwd()}"
diretorio_imagens = f"{base_diretorio}/1_imagens_baixadas/"
diretorio_convertidas = f"{base_diretorio}/2_imagens_convertidas/"
diretorio_tratadas = f"{base_diretorio}/3_imagens_tratadas/"
diretorio_resultados = f"{base_diretorio}/4_resultados_ocr/"
diretorio_saneamentos = f"{base_diretorio}/5_resultados_saneados/"
diretorio_documentos = f"{base_diretorio}/6_documentos_gerados/"
caminho_fonte = f"{base_diretorio}/fonts/DejaVuSans.ttf"
caminho_arquivo_credenciais = f"{base_diretorio}/credenciais/credenciais.json"

# Garante que a pasta credenciais existe
caminho_pasta_credenciais = os.path.join(base_diretorio, "credenciais")
os.makedirs(caminho_pasta_credenciais, exist_ok=True)

# Garante que o arquivo credenciais.json existe com as chaves corretas e valores vazios
caminho_arquivo_credenciais = os.path.join(caminho_pasta_credenciais, "credenciais.json")
if not os.path.exists(caminho_arquivo_credenciais):
    credenciais_vazias = {
        "url": "",
        "apiKey": ""
    }
    with open(caminho_arquivo_credenciais, "w") as f:
        json.dump(credenciais_vazias, f, indent=4)


def gerar_resposta_gpt(prompt, caminho_arquivo_credenciais):

    with open(caminho_arquivo_credenciais, 'r') as f:
        credenciais = json.load(f)
    
    url = credenciais["url"]
    apiKey = credenciais["apiKey"]

    texto = prompt
    params = {
        'modelOverride': 'gpt-4o',
        'max_tokens': 4096
    }
    headers = {"X-Api-Key": apiKey}
    data = {
        "inputs": {
            "entrada_py": texto,
        }
    }
    response = requests.post(
        url,
        json=data,
        headers=headers,
        params=params,
        timeout=120
    )
    
    resposta = response.text
    
    return resposta


def main():
    # Realizando saneamento nos resultados
    prompt_utilidades = ""
    conteudos = list()
    arquivos = os.listdir(diretorio_resultados)
    for pos, arquivo in enumerate(arquivos):
        caminho_arquivo = os.path.join(diretorio_resultados, arquivo)
        if os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo_txt:
                conteudo = arquivo_txt.read()
                conteudos.append(f"Texto: {pos+1}: '{conteudo}'")
                prompt = f"{pos+1} Estou utilizando este serviço como microserviço de verificação de utilidade textual. O conteúdo analisado foi extraído aleatoriamente de uma imagem, portanto, não possui contexto. Avalie se o texto a seguir: '{conteudo}', de forma geral, é útil. A resposta deve ser 'SIM' ou 'NÃO', considerando apenas os casos em que seja possível extrair uma percepção significativa (insight) da informação apresentada e se o conteúdo constitui ao menos uma frase completa."
                prompt_utilidades += f"\n{prompt}"

    prompt_utilidades += "\nResponda apenas com a lista Python, sem explicações, por exemplo: ['SIM', 'NÃO']."
    resposta_gpt_utilidade = gerar_resposta_gpt(prompt_utilidades, caminho_arquivo_credenciais)

    try:
        lista_respostas = ast.literal_eval(resposta_gpt_utilidade)
    except Exception:
        print("Erro ao converter resposta do modelo para lista Python.")
        lista_respostas = []

    lista_respostas = lista_respostas[:len(arquivos)]

    indices = [i for i, resp in enumerate(lista_respostas) if "N" not in str(resp).upper()]

    # Salvando os resultados saneados
    arquivos_resultados = np.array(arquivos)
    arquivos_resultados = arquivos_resultados[indices]
    for arquivo in arquivos_resultados:
        caminho_origem = os.path.join(diretorio_resultados, arquivo)
        caminho_destino = os.path.join(diretorio_saneamentos, arquivo)
        if os.path.isfile(caminho_arquivo):
            shutil.copy(caminho_arquivo, caminho_destino)

    #Analisando os conteúdos
    conteudos = np.array(conteudos)
    conteudos = conteudos[indices]
    prompt_analise = ""
    for texto in conteudos:
        prompt_analise += f"\n{texto}"
    prompt_analise += f"Retorne somente um JSON, com as informações de cada texto. Estrutura do JSON para cada texto: 'titulo', 'publico_alvo', 'objetivo', 'analise_detalhada',  'texto_corrigido', 'original'. Na analise faça detalhada e profunda, mostre números se tiver, informações relevantes, porém não quebre em tópicos. No texto_corrigo, somente corrija erros"
    resposta_gpt_analise = gerar_resposta_gpt(prompt_analise, caminho_arquivo_credenciais)

    # Limpeza da resposta do modelo para garantir que seja um JSON válido
    resposta_gpt_analise = resposta_gpt_analise.strip()
    if resposta_gpt_analise.startswith("```"):
        resposta_gpt_analise = resposta_gpt_analise.lstrip("`")
    if resposta_gpt_analise.startswith("json"):
        resposta_gpt_analise = resposta_gpt_analise[4:].lstrip()
    if resposta_gpt_analise.endswith("```"):
        resposta_gpt_analise = resposta_gpt_analise.rstrip("`")

    try:
        resposta_gpt_analise = json.loads(resposta_gpt_analise)
    except Exception:
        print("Erro ao converter resposta do modelo para lista de dicionários.")
        resposta_gpt_analise = []

    # Gerando documentos
    for pos, texto in enumerate(resposta_gpt_analise):
        titulo = texto['titulo']
        publico_alvo = texto['publico_alvo']
        objetivo = texto['objetivo']
        analise = texto['analise_detalhada']
        corrigido = texto['texto_corrigido']
        original = texto['original']
        
        # Obtendo nome do arquivo
        nome = str(arquivos_resultados[pos])
        nome = nome.split(".")
        nome = nome[0]

        # Obtendo o altura da imagem
        imagem = Image.open(f'{diretorio_convertidas}{nome}.png')
        largura, altura = imagem.size
        largura_pdf = largura
        altura_pdf = altura
        #print(largura, altura)

        if altura > 200:
            altura = 200

        # Configurações do PDF
        pdf = FPDF() # Criando o objetivo
        pdf.add_page() # Adicionando uma página
        pdf.add_font('DejaVu', '', caminho_fonte, uni=True) # Obtendo fonte
        pdf.add_font('DejaVu', 'B', caminho_fonte, uni=True) # Obtendo fonte

        # Inserindo registros no PDF
        pdf.set_font('Arial', 'B', 14) # Definindo a fonte para o texto
        pdf.multi_cell(190, 10, "Imagem: ")
        pdf.image(f'{diretorio_convertidas}{nome}.png', x=10, y=20, w=190, h=altura) # Inserindo imagem
        pdf.set_y(altura + 20) # Adicionado espaços
        pdf.multi_cell(190, 10, "Título: ")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(190, 10, titulo)
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(190, 10, "Público-alvo: ")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(190, 10, publico_alvo)
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(190, 10, "Objetivo: ")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(190, 10, objetivo)
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(190, 10, "Analise: ")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(190, 10, analise)
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(190, 10, "Texto corrigido: ")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(190, 10, corrigido)
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(190, 10, "Texto original: ")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(190, 10, original)
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(190, 10, "Dimensões: ")
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(190, 10, f"{largura_pdf}X{altura_pdf}")
        pdf.output(f"{diretorio_documentos}{nome}.pdf") # Salvando PDF
    
    print("Documentos gerados com sucesso!")

    return None
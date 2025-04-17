# Esse script é responsável por fazer upload das imagens que tem (img), todas as imagens que existem no site são baixadas (exceto logos)

from bs4 import BeautifulSoup
from time import sleep
import requests
from urllib.parse import urljoin
import os
import easyocr
from time import sleep
from PIL import Image, ImageEnhance
import pytesseract
import cairosvg

# Variáveis úteis
base_diretorio = f"{os.getcwd()}/2024_2025"
diretorio_imagens = f"{base_diretorio}/1_imagens_baixadas/"
diretorio_convertidas = f"{base_diretorio}/2_imagens_convertidas/"
diretorio_tratadas = f"{base_diretorio}/3_imagens_tratadas/"
diretorio_resultados = f"{base_diretorio}/4_resultados_ocr/"
diretorio_saneamentos = f"{base_diretorio}/5_resultados_saneados/"
diretorio_documentos = f"{base_diretorio}/6_documentos_gerados/"

#Lista
pillow_supported_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".ico"]

cairo_svg_supported_extensions = [".svg"]

def apagar_antigos_arquivos(caminho):
    arquivos = os.listdir(caminho)
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(caminho, arquivo)
        if os.path.isfile(caminho_arquivo):
            os.remove(caminho_arquivo)

# Apagando antigos arquivos
apagar_antigos_arquivos(diretorio_imagens)
apagar_antigos_arquivos(diretorio_convertidas)
apagar_antigos_arquivos(diretorio_tratadas)
apagar_antigos_arquivos(diretorio_resultados)
apagar_antigos_arquivos(diretorio_saneamentos)
apagar_antigos_arquivos(diretorio_documentos)

# Funções úteis
def convert_image_pillow():
    """
        Convertendo imagens em PNG que são suportadas pela biblioteca PILLOW
    """
    try:
        arquivos = os.listdir(diretorio_imagens)
        arquivos = sorted(arquivos, key=lambda x: int(x.split('.')[0]))
        for pos, arquivo in enumerate(arquivos):
            nome_arquivo = str(arquivo).split(".")
            nome_arquivo = nome_arquivo[0]
            tipo_arquivo = str(arquivo).split(".")
            tipo_arquivo = f".{tipo_arquivo[-1]}"
            caminho_arquivo_convertido = f"{diretorio_convertidas}{nome_arquivo}.png"
            caminho_arquivo = os.path.join(diretorio_imagens, arquivo)
            if tipo_arquivo in pillow_supported_extensions:
                img = Image.open(caminho_arquivo)
                img.save(caminho_arquivo_convertido, format="PNG")
    except Exception as erro:
        erro = erro
        print(f"Não foi possível converter imagem para PNG, erro: {erro}")
    
    return None


def convert_image_svg():
    """
        Converter imagens de SVG para PNG utilizando cairosvg
    """
    try:
        arquivos = os.listdir(diretorio_imagens)
        arquivos = sorted(arquivos, key=lambda x: int(x.split('.')[0]))
        for pos, arquivo in enumerate(arquivos):
            nome_arquivo = str(arquivo).split(".")
            nome_arquivo = nome_arquivo[0]
            tipo_arquivo = str(arquivo).split(".")
            tipo_arquivo = f".{tipo_arquivo[-1]}"
            caminho_arquivo = os.path.join(diretorio_imagens, arquivo)
            caminho_arquivo_convertido = f"{diretorio_convertidas}{nome_arquivo}.png"
            if tipo_arquivo in cairo_svg_supported_extensions:
                cairosvg.svg2png(url=caminho_arquivo, write_to=caminho_arquivo_convertido)
    except Exception as erro:
        erro = erro
        print(f"Não foi possível converter imagem para PNG, erro: {erro}")

    return None


def treat_image():
    """
        Função responsável por tratar as imagens convertidas, aumentando o contraste
    """
    arquivos = os.listdir(diretorio_convertidas)
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(diretorio_convertidas, arquivo)
        imagem = Image.open(caminho_arquivo)
        if imagem.mode not in ['RGB', 'L']: # Verificando se a imagem está no padrão RGB
            imagem = imagem.convert('RGB')
        if os.path.isfile(caminho_arquivo):
            # Aumentar o contraste
            fator_contraste = 2.0
            enhancer = ImageEnhance.Contrast(imagem)
            image_with_contrast = enhancer.enhance(fator_contraste)
            image_with_contrast.save(f"{diretorio_tratadas}/{arquivo}")

    return None
    
    
# Web Scraping
site = "https://brasilescola.uol.com.br/redacao/genero-textual-infografico.htm#:~:text=O%20infogr%C3%A1fico%20%C3%A9%20uma%20uni%C3%A3o,de%20publicidade%20e%20no%20jornalismo"
#site = "https://www.mercadolivre.com.br/"

resposta = requests.get(site)
if resposta.status_code == 200:
    conteudo = BeautifulSoup(resposta.text, "html.parser")
    imagens = conteudo.find_all("img")
    
    if imagens:
        for pos, imagem in enumerate(imagens):
            try:
                endereco_imagem = imagem["src"]
                endereco_imagem_completo = urljoin(site, endereco_imagem)
                resposta_imagem = requests.get(endereco_imagem_completo)
                tipo_arquivo = str(endereco_imagem_completo).split("/")
                tipo_arquivo = tipo_arquivo[-1]
                tipo_arquivo = str(tipo_arquivo).split(".")
                tipo_arquivo = tipo_arquivo[-1]
                if resposta_imagem.status_code == 200 and "logo" not in str(endereco_imagem_completo):
                    with open(f"{diretorio_imagens}/{pos+1}.{tipo_arquivo}", "wb") as arquivo_imagem:
                        arquivo_imagem.write(resposta_imagem.content)
            except Exception as erro:
                erro = erro
                #print(f"Erro na Download da imagem, erro: {erro}")

        print(f"A página tem {len(imagens)} imagens ao total")

    else:
        print("A página não tem imagens")

# Removendo arquivos que não são imagens
arquivos = os.listdir(diretorio_imagens)
arquivos = sorted(arquivos, key=lambda x: int(x.split('.')[0]))
for pos, arquivo in enumerate(arquivos):
    tipo_arquivo = str(arquivo).split(".")
    tipo_arquivo = f".{tipo_arquivo[-1]}"
    caminho_arquivo = os.path.join(diretorio_imagens, arquivo)
    if tipo_arquivo not in pillow_supported_extensions and tipo_arquivo not in cairo_svg_supported_extensions:
        os.remove(caminho_arquivo)

# Converter imagens para PNG
convert_image_pillow()
convert_image_svg()

# Tratando as imagens
treat_image()

#Aplicando OCR\
arquivos = os.listdir(diretorio_tratadas)
arquivos = sorted(arquivos, key=lambda x: int(x.split('.')[0]))
leitor = easyocr.Reader(['pt']) #leitor com os idiomas desejados
for pos, arquivo in enumerate(arquivos):
    caminho_arquivo = os.path.join(diretorio_tratadas, arquivo)
    if os.path.isfile(caminho_arquivo):
        try:
            resultados = ""
            try:
                leitura = leitor.readtext(caminho_arquivo) # OCR em uma imagem
            except Exception as erro:
                erro = erro
                print(f"Erro na aplicação do OCR erro: {erro}")

            for valor in leitura:
                resultados += f" {valor[1]}"
            
            if len(resultados) >= 1: # Verificando se o arquivo tem texto
                print(resultados)
                tipo_arquivo = str(arquivo).split(".")
                tipo_arquivo = tipo_arquivo[-1]
                with open(f"{diretorio_resultados}/{str(arquivo).replace(f'.{tipo_arquivo}', '.txt')}", "w", encoding="utf-8") as arquivo_txt:
                    arquivo_txt.write(resultados)
            else:
                os.remove(caminho_arquivo)

        except Exception as erro:
            erro = erro
            print(f"Erro no processamento: {erro}")
    else:
        os.remove(caminho_arquivo)
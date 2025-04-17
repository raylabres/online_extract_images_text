from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Carregue a imagem
imagem = Image.open(r'resposta.png')  # Substitua pelo caminho da sua imagem

# Use o pytesseract para fazer OCR na imagem
texto = pytesseract.image_to_string(imagem, lang='eng')  # Substitua 'eng' pelo código do idioma desejado

# Exiba o texto reconhecido
texto = str(texto).split("Gerando respostas")
texto = texto[1].split("Saiba mais")
texto = texto[0].split("\n")
texto = texto[2:]

texto_final = ""
for parte in texto:
    if len(parte) >= 1:
        texto_final += f"\n{parte}"

texto_final = texto_final.strip()
print(texto_final)
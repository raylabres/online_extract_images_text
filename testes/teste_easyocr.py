import easyocr

texto = ""

leitor = easyocr.Reader(['pt'])
leitura = leitor.readtext(r'teste.png')

for valor in leitura:
    texto += f" {valor[1]}"

print(texto)

import cv2
import numpy as np

# Carregar a imagem
imagem = cv2.imread(r'C:\Desenvolvimento\Projetos\iniciacao_cientifica_ceusnp\2024_2025\2_imagens_convertidas\9.png')

# 1. Converter para escala de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# 2. Aumentar o contraste com CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
imagem_contraste = clahe.apply(imagem_cinza)

# 3. Aplicar filtro de nitidez
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
imagem_nitida = cv2.filter2D(imagem_contraste, -1, kernel)

# 4. Binarizar a imagem
_, imagem_bin = cv2.threshold(imagem_nitida, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Salvar a imagem processada
cv2.imwrite(r'C:\Desenvolvimento\Projetos\iniciacao_cientifica_ceusnp\2024_2025\3_imagens_tratadas\9.png', imagem_bin)


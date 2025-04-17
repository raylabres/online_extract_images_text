from fpdf import FPDF

# Criando o objeto PDF
pdf = FPDF()

# Adicionando uma página
pdf.add_page()

# Definindo a fonte para o texto
pdf.set_font('Arial', '', 12)

# Texto de exemplo
texto = """[
  {
    "titulo": "Funções e Características de um Infográfico",
    "publico_alvo": "Público em geral, profissionais de design, marketing e comunicaçãodsfsdfsdfsdfsdfsdfsdfsdfdsf",
"""

# Usando multi_cell para texto com quebra automática de linha
# A largura (w) está definida como 190, para garantir que o texto ocupe um espaço menor que a largura da página
# A altura (h) é a altura de cada linha de texto (10 unidades)
#pdf.image(r'C:\Desenvolvimento\Projetos\iniciacao_cientifica_ceusnp\2024_2025\1_imagens_baixadas\1.jpg', x=10, y=100, w=50, h=50)
pdf.image(r'C:\Desenvolvimento\Projetos\iniciacao_cientifica_ceusnp\2024_2025\1_imagens_baixadas\1.jpg', x=10, y=10, w=190)

# Ajustando a posição inicial do texto abaixo da imagem
# Aqui, `y` é calculado como a altura da imagem (digamos 50) mais uma margem adicional (10).
pdf.set_y(50)  # 50 (altura da imagem) + 10 (margem)

pdf.multi_cell(190, 10, texto)
pdf.multi_cell(190, 10, texto)
pdf.multi_cell(190, 10, texto)
# Salvando o PDF
pdf.output('exemplo_pdf_com_texto_quebra_automatica.pdf')

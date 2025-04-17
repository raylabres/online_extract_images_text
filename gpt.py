import os
import numpy as np
import shutil
from fpdf import FPDF
from PIL import Image, ImageEnhance

# Variáveis úteis
base_diretorio = f"{os.getcwd()}/2024_2025"
diretorio_imagens = f"{base_diretorio}/1_imagens_baixadas/"
diretorio_convertidas = f"{base_diretorio}/2_imagens_convertidas/"
diretorio_tratadas = f"{base_diretorio}/3_imagens_tratadas/"
diretorio_resultados = f"{base_diretorio}/4_resultados_ocr/"
diretorio_saneamentos = f"{base_diretorio}/5_resultados_saneados/"
diretorio_documentos = f"{base_diretorio}/6_documentos_gerados/"
caminho_fonte = f"{base_diretorio}/fonts/DejaVuSans.ttf"

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
            prompt = f"{pos+1} chat estou utilizando você como microserviço para verificação. Esse texto foi extraído de uma imagem aleatória, não existe nenhum contexto. Responda somente com SIM ou NÃO, este texto: '{conteudo}' de forma geral é útil? Porém só considere é possível extrair um inshit dessa informação e se é pelo menos uma frase completa"
            prompt_utilidades += f"\n{prompt}"

prompt_utilidades += "\nRetorne uma lista em Python ['']"
#print(prompt_utilidades)
resposta_gpt_utilidade = ['SIM', 'NÃO', 'NÃO', 'SIM', 'NÃO', 'SIM', 'NÃO', 'SIM', 'NÃO', 'SIM', 'NÃO']


# Obtendo indíces para filtrar
indices = list()
for pos, resposta in enumerate(resposta_gpt_utilidade):
    if "N" not in str(resposta).upper():
        indices.append(pos)

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
#print(prompt_analise)
resposta_gpt_analise = [
  {
    "titulo": "Funções e Como Fazer Infográfico",
    "publico_alvo": "Público em geral, interessados em criar infográficos",
    "objetivo": "Guiar na criação de infográficos claros, atrativos e bem organizados",
    "analise_detalhada": "O texto descreve funções e características para a criação de um infográfico. Ele destaca a necessidade de transmitir informações de forma clara e atraente, com o uso de texto e elementos visuais. A recomendação de escolher um único tema é importante para a clareza e foco do conteúdo. É sugerido o uso de ferramentas como Canvas, Word ou PowerPoint para a elaboração do infográfico. A principal falha no texto é a falta de clareza e erros gramaticais em termos como 'lopicallzadas' (deveria ser 'localizadas'). O texto também poderia ser mais coeso e explicativo, detalhando mais sobre o uso de cada ferramenta sugerida.",
    "texto_corrigido": "Funções: Transmitir informações. Ser atrativo ao público-alvo. Ser claro e preciso. Infográfico. Características: (texto e elementos visuais). Linguagem verbal e não verbal. Informações bem organizadas ou localizadas. Único tema. Como fazer: Escolha um tema. Defina o visual e o texto da mensagem. Utilize ferramentas (Canvas, Word, PowerPoint, etc.). Revise o texto e a parte visual.",
    "original": "Funções: Transmitir informaçoes Ser atrativo a0 público-alvo Ser claro preciso Infográfico Caracteristicas: (texto elementos visuais) Linguagem verbal não verbal Informações bem organizadas elou lopicallzadas Único tema Como fazer: Escolha tema Defina visual texto da mensagem Utilize ferramentas (Canvas, Word, PowerPoint etc ) Revise texto parte"
  },
  {
    "titulo": "Cuidados em Casa - Coronavírus",
    "publico_alvo": "Público em geral, com foco em pessoas de 60 anos ou mais e pacientes com sintomas de Covid-19",
    "objetivo": "Orientar sobre cuidados dentro de casa para prevenir a propagação do coronavírus",
    "analise_detalhada": "Este texto tem como foco a orientação de cuidados para pessoas que estão isoladas em casa devido ao coronavírus. Ele destaca a importância do isolamento social, especialmente para pessoas com mais de 60 anos ou com sintomas de gripe. O texto traz orientações sobre distanciamento social, ventilação do ambiente, e uso exclusivo de objetos pessoais. A presença de erros ortográficos como 'soclal' (deveria ser 'social') e 'fosto' (deveria ser 'posto') pode prejudicar a compreensão. Além disso, a estrutura do texto é confusa, com falhas na pontuação e falta de clareza em algumas instruções, o que pode gerar insegurança nas pessoas que buscam informações claras e diretas.",
    "texto_corrigido": "#CORONAVÍRUS CUIDADOS DENTRO DE CASA Recomendação de Isolamento social é essencial para conter a circulação do vírus e a propagação de casos de Covid-19. QUEM DEVE FICAR EM CASA: Pessoas acima de 60 anos, pacientes com confirmação de gripe ou resfriado (grupo mais vulnerável de Covid-19). Devem ficar em casa até desaparecerem os sintomas. Procure um posto de saúde se houver piora (dificuldade para respirar ou cansaço). RECOMENDAÇÕES EM CASA: Permaneça em casa até desaparecerem os sintomas. Fique, de preferência, em um quarto individual bem ventilado. Evite compartilhar objetos de higiene pessoal e talheres. Não receba visitas. Manter distância de pelo menos 1 metro da pessoa infectada e manter o ambiente bem ventilado.",
    "original": "#CORONAVÍRUS CUIDADOS DENTRO DE CASA Recomendação de Isolamento soclal é essenclal para conter circulação do vÍrus e a propagação de casos de Covid-19 QUEM DEVE FICAR EM CASA 60+ Pessoas Paciente com Pessoas com sintomas acima de 60 anos confirmação de gripe ou resfriado (grupo mais de Covid-19 (devem ficar em casa vulneravel (devem (lcar em casa por 14 dlas) doença) até desaparecerem Procure UM fosto 05 sintomas) De Saude Se HOUVER PIORA (DiFIcULDADE PARA respirar € CANSAÇO) RECOMENDAÇÕES EM CASA Permaneça em casa De preferência; fique Evite compartilhar até desaparecerem os em quarto individual objetos de higiene sintomas por completo bem ventilado pessoal talheres 1 MEIRO Não receba Manter distância de Mantenha visitas pelo menos metro ambiente da pessoa infectada ventilado"
  },
  {
    "titulo": "Fases do Plano SP",
    "publico_alvo": "Público em geral, especialmente moradores do estado de São Paulo",
    "objetivo": "Informar sobre as fases do Plano SP para a retomada econômica e a segurança sanitária no estado",
    "analise_detalhada": "O texto descreve as fases do plano de retomada econômica do estado de São Paulo, destacando que o estado foi dividido em 22 regiões. Cada região deve seguir os protocolos de saúde definidos pela fase em que se encontra, sendo ajustados conforme a evolução dos casos de Covid-19. A análise dos dados para mudança de fase inclui a capacidade do sistema de saúde, número de internações e óbitos. O texto apresenta problemas significativos de ortografia e pontuação, como 'Rlbelrão' (deveria ser 'Ribeirão') e 'Marflla' (deveria ser 'Mairiporã'). Esses erros dificultam a leitura e a compreensão de informações importantes, como a divisão das regiões e o critério de mudança de fase.",
    "texto_corrigido": "AS FASES DO PLANO SP Entenda quais são e como são calculadas as etapas para a retomada consciente e segura da economia no estado. O estado foi dividido em 22 regiões. Cidades devem seguir os protocolos estabelecidos de acordo com a fase que a região está. Franca, Ribeirão Preto, São José do Rio Preto, Araraquara, São Carlos, Araçatuba, São João da Boa Vista, Piracicaba, Presidente Prudente, Campinas, Marília, Taubaté, Sub-região Leste RMSP, Bauru, Sub-região Norte RMSP, Sub-região Sudeste RMSP, Sorocaba, Município de São Paulo, Sub-região Sudoeste RMSP, Sub-região Oeste RMSP, Baixada Santista. Fases são calculadas de acordo com a situação das regiões, acompanhando indicadores de saúde. Uma região só avança de fase se houver melhora no número de casos, internações e óbitos. Se houver piora, a região volta para a fase anterior.",
    "original": "AS FASES DO PLANO SP Entenda quais são e como são calculadas as etapas para retomada consciente e segura da economia no estado ESTADO FOI DIVIDIDO EM 22 REGIÕES Cidades devem seguir os protocolos estabelecidos de acordo com a fase que a região está Franca VIII  Bauetos Rlbelrão Preto XIII } São José do Rlo Preto Ararquara Sho Carlos _ I Aracatuba Sáo João da Boa Vlsta Piracicaba Presldente Prudente Camplnas  vII Marflla Iaubaté xvI Sub-reRião Leste RMSP Bauru Sub-reglão Norte RMSP Sub rsgifo Sudeste RMSP Sorocaba Munlcipio de Sao Paule Sub-repino Sudoeste RMSP xII_ Reglstro Sub-região Oeste RMSP Balxada Santista Fases são calculadas A situação das Uma região Se houver piora, de acordo com regiões só avança de fase região volta capacidade do sistema acompanhada se registra para fase anterior de saúde evolução diariamente melhora do nª de casos, pelo Governo dos indicadores internaçoes óbitos"
  },
  {
    "titulo": "Divulgação de Obras Literárias - Unicentro (PR)",
    "publico_alvo": "Estudantes interessados em vestibulares, professores, e interessados em literatura",
    "objetivo": "Divulgar as obras literárias da Unicentro para os vestibulares de 2026 e 2027",
    "analise_detalhada": "Este texto tem como objetivo informar sobre a divulgação de obras literárias pela Unicentro (PR) para os vestibulares de 2026 e 2027. No entanto, o texto está incompleto e apresenta uma frase truncada, o que dificulta a compreensão do conteúdo completo. A falta de contexto e detalhes impede a análise profunda da informação, mas a menção aos vestibulares torna claro o público-alvo e o objetivo de divulgação. Seriam necessárias mais informações sobre as obras literárias e a forma de acesso aos materiais.",
    "texto_corrigido": "Unicentro (PR) divulga obras literárias para os vestibulares de 2026 e 2027.",
    "original": "Unicentro (PR) divulga obras literárias Brisil dos Vestibulares 2026 2027 ESCOE"
  },
  {
    "titulo": "Vestibular UEG 2025 via ENEM",
    "publico_alvo": "Estudantes interessados no vestibular da UEG para 2025, via ENEM",
    "objetivo": "Informar sobre a realização do vestibular da UEG em 2025, por meio da nota do ENEM",
    "analise_detalhada": "O texto menciona o vestibular da Universidade Estadual de Goiás (UEG) para o ano de 2025, que será realizado utilizando a nota do ENEM. A informação é breve, sem muitos detalhes, e não há menção de datas ou requisitos específicos. A simples menção do nome da universidade e a referência ao ENEM são suficientes para atrair a atenção dos estudantes interessados, mas o texto carece de informações adicionais sobre o processo seletivo.",
    "texto_corrigido": "Vestibular UEG 2025 via ENEM.",
    "original": "Oeurg UEG UEG VESTIBULAR 2025 VIA ENEM"
  }
]

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
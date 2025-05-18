import os
import numpy as np
import shutil
from fpdf import FPDF
from PIL import Image, ImageEnhance

# Variáveis úteis
base_diretorio = os.getcwd()
diretorio_imagens = f"{base_diretorio}/1_imagens_baixadas/"
diretorio_convertidas = f"{base_diretorio}/2_imagens_convertidas/"
diretorio_tratadas = f"{base_diretorio}/3_imagens_tratadas/"
diretorio_resultados = f"{base_diretorio}/4_resultados_ocr/"
diretorio_saneamentos = f"{base_diretorio}/5_resultados_saneados/"
diretorio_documentos = f"{base_diretorio}/6_documentos_gerados/"
caminho_fonte = f"{base_diretorio}/fonts/DejaVuSans.ttf"

def apagar_antigos_arquivos(caminho):
    arquivos = os.listdir(caminho)
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(caminho, arquivo)
        if os.path.isfile(caminho_arquivo):
            os.remove(caminho_arquivo)

# Apagando antigos arquivos
apagar_antigos_arquivos(diretorio_saneamentos)
apagar_antigos_arquivos(diretorio_documentos)

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
resposta_gpt_utilidade = ['SIM', 'SIM', 'NÃO', 'SIM', 'NÃO', 'NÃO', 'NÃO', 'NÃO', 'NÃO', 'NÃO']


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
    "titulo": "Cuidados dentro de casa durante a pandemia de Covid-19",
    "publico_alvo": "População em geral, especialmente pessoas acima de 60 anos, pessoas com sintomas gripais ou com confirmação de Covid-19",
    "objetivo": "Orientar a população sobre cuidados domiciliares durante a pandemia, com foco na prevenção da propagação do coronavírus e nas recomendações para grupos de risco",
    "analise_detalhada": "O texto aborda a importância do isolamento social como medida essencial para conter a circulação do coronavírus, conforme amplamente recomendado por autoridades de saúde desde o início da pandemia em 2020. As orientações são direcionadas a públicos vulneráveis, como idosos (60+), pacientes com confirmação de Covid-19 e pessoas com sintomas de gripe ou resfriado. Reforça-se o tempo mínimo de isolamento (14 dias), além da necessidade de permanecer em ambientes ventilados, manter o distanciamento social e evitar o compartilhamento de objetos pessoais. O texto também destaca que, em casos de piora dos sintomas (como dificuldade para respirar ou cansaço excessivo), deve-se procurar uma unidade de saúde. Apesar da importância das informações, há erros ortográficos e de digitação que podem comprometer a clareza, além de uma estrutura desorganizada que dificulta a leitura rápida. Não há dados numéricos no conteúdo original, mas o tema se relaciona diretamente com estatísticas de contágio e mortalidade por Covid-19, especialmente entre os grupos de risco.",
    "texto_corrigido": "#CORONAVÍRUS\nCUIDADOS DENTRO DE CASA\nA recomendação de isolamento social é essencial para conter a circulação do vírus e a propagação de casos de Covid-19.\n\nQUEM DEVE FICAR EM CASA:\n• Pessoas acima de 60 anos (grupo mais vulnerável à doença)\n• Pacientes com confirmação de Covid-19 (devem ficar em casa por 14 dias)\n• Pessoas com sintomas de gripe ou resfriado (devem ficar em casa até desaparecerem os sintomas)\n\nProcure um posto de saúde se houver piora (dificuldade para respirar e cansaço).\n\nRECOMENDAÇÕES EM CASA:\n• Permaneça em casa até desaparecerem os sintomas por completo\n• De preferência, fique em quarto individual e bem ventilado\n• Evite compartilhar objetos de higiene pessoal e talheres\n• Não receba visitas\n• Mantenha distância de pelo menos 1 metro\n• Mantenha o ambiente ventilado",
    "original": " #CORONAVÍRUS CUIDADOS DENTRO DE CASA Recomendação de Isolamento soclal é essenclal para conter circulação do vÍrus e a propagação de casos de Covid-19 QUEM DEVE FICAR EM CASA 60+ Pessoas Paciente com Pessoas com sintomas acima de 60 anos confirmação de gripe ou resfriado (grupo mais de Covid-19 (devem ficar em casa vulneravel (devem (lcar em casa por 14 dlas) doença) até desaparecerem Procure UM fosto 05 sintomas) De Saude Se HOUVER PIORA (DiFIcULDADE PARA respirar € CANSAÇO) RECOMENDAÇÕES EM CASA Permaneça em casa De preferência; fique Evite compartilhar até desaparecerem os em quarto individual objetos de higiene sintomas por completo bem ventilado pessoal talheres 1 MEIRO Não receba Manter distância de Mantenha visitas pelo menos metro ambiente da pessoa infectada ventilado"
  },
  {
    "titulo": "As fases do Plano SP",
    "publico_alvo": "População do estado de São Paulo, especialmente gestores municipais, empresários e cidadãos interessados na retomada econômica",
    "objetivo": "Explicar as fases do Plano São Paulo para reabertura econômica gradual com base em indicadores de saúde pública e estrutura hospitalar",
    "analise_detalhada": "O texto trata da divisão do estado de São Paulo em 22 regiões administrativas para o controle da pandemia de Covid-19 e a retomada econômica consciente. A classificação em fases (de mais restritiva à mais flexível) considera indicadores como número de casos, internações e óbitos, além da capacidade hospitalar. Uma região só avança se houver melhora contínua nos indicadores, sendo monitorada diariamente pelo Governo do Estado. Em caso de piora, a região retorna à fase anterior, destacando o caráter dinâmico e adaptativo do plano. A estratégia foi essencial durante os momentos críticos da pandemia para balancear saúde pública e atividade econômica. A linguagem do texto original é confusa em alguns trechos, especialmente com nomes de cidades aglutinados ou mal pontuados, o que compromete a compreensão. Além disso, não há visualização clara das fases nem dados quantitativos, o que poderia enriquecer o conteúdo.",
    "texto_corrigido": "AS FASES DO PLANO SP\nEntenda quais são e como são calculadas as etapas para retomada consciente e segura da economia no estado.\n\nO ESTADO FOI DIVIDIDO EM 22 REGIÕES:\nAs cidades devem seguir os protocolos estabelecidos de acordo com a fase em que a região está.\n\nExemplos de regiões:\n• Franca\n• Ribeirão Preto\n• São José do Rio Preto\n• Araraquara\n• São Carlos\n• Araçatuba\n• São João da Boa Vista\n• Piracicaba\n• Presidente Prudente\n• Campinas\n• Marília\n• Taubaté\n• Sorocaba\n• Registro\n• Baixada Santista\n• Sub-regiões da RMSP: Norte, Sul, Sudeste, Sudoeste, Oeste, Leste\n\nCOMO FUNCIONA:\nAs fases são calculadas de acordo com a capacidade do sistema de saúde. Uma região só avança se houver melhora dos indicadores (casos, internações e óbitos), monitorados diariamente pelo Governo. Se houver piora, a região retorna à fase anterior.",
    "original": " AS FASES DO PLANO SP Entenda quais são e como são calculadas as etapas para retomada consciente e segura da economia no estado ESTADO FOI DIVIDIDO EM 22 REGIÕES Cidades devem seguir os protocolos estabelecidos de acordo com a fase que a região está Franca VIII  Bauetos Rlbelrão Preto XIII } São José do Rlo Preto Ararquara Sho Carlos _ I Aracatuba Sáo João da Boa Vlsta Piracicaba Presldente Prudente Camplnas  vII Marflla Iaubaté xvI Sub-reRião Leste RMSP Bauru Sub-reglão Norte RMSP Sub rsgifo Sudeste RMSP Sorocaba Munlcipio de Sao Paule Sub-repino Sudoeste RMSP xII_ Reglstro Sub-região Oeste RMSP Balxada Santista Fases são calculadas A situação das Uma região Se houver piora, de acordo com regiões só avança de fase região volta capacidade do sistema acompanhada se registra para fase anterior de saúde evolução diariamente melhora do nª de casos, pelo Governo dos indicadores internaçoes óbitos"
  },
  {
    "titulo": "Infográfico: Funções, características e como fazer",
    "publico_alvo": "Estudantes, profissionais de comunicação e design, e qualquer pessoa interessada em produzir infográficos informativos",
    "objetivo": "Explicar de maneira didática como construir um infográfico eficaz, destacando suas funções, características e etapas de elaboração",
    "analise_detalhada": "O texto apresenta os principais elementos que compõem um infográfico eficiente. Entre as funções destacadas, estão: transmitir informações de forma clara e ser visualmente atrativo ao público-alvo. As características incluem o uso combinado de linguagem verbal e não verbal, organização e foco em um único tema. A estrutura orienta sobre o processo de criação: escolha do tema, definição da mensagem visual e textual e revisão do material. O conteúdo é didático e sintetiza bem o processo, embora haja erros ortográficos (como 'preciso' sem acento ou 'elou' no lugar de 'e/ou') e estrutura gramatical desorganizada. A linguagem é voltada para iniciantes, com sugestões acessíveis como o uso do Canva, Word ou PowerPoint. A ausência de exemplos visuais ou métricas sobre a eficácia dos infográficos limita a profundidade do conteúdo.",
    "texto_corrigido": "Funções:\n• Transmitir informações\n• Ser atrativo ao público-alvo\n• Ser claro e preciso\n\nInfográfico – Características:\n• Texto e elementos visuais (linguagem verbal e não verbal)\n• Informações bem organizadas e/ou tematizadas\n• Foco em um único tema\n\nComo fazer:\n• Escolha o tema\n• Defina o visual e o texto da mensagem\n• Utilize ferramentas (Canva, Word, PowerPoint etc.)\n• Revise o texto",
    "original": " Funções: Transmitir informaçoes Ser atrativo a0 público-alvo Ser claro preciso Infográfico Caracteristicas: (texto elementos visuais) Linguagem verbal não verbal Informações bem organizadas elou lopicallzadas Único tema Como fazer: Escolha tema Defina visual texto da mensagem Utilize ferramentas (Canvas, Word, PowerPoint etc ) Revise texto parte"
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
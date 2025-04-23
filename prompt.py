import os
import numpy as np
import shutil
from fpdf import FPDF
from PIL import Image, ImageEnhance

# Variáveis úteis
base_diretorio = f"{os.getcwd()}"
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
            prompt = f"{pos+1} Estou utilizando este serviço como microserviço de verificação de utilidade textual. O conteúdo analisado foi extraído aleatoriamente de uma imagem, portanto, não possui contexto. Avalie se o texto a seguir: '{conteudo}', de forma geral, é útil. A resposta deve ser 'SIM' ou 'NÃO', considerando apenas os casos em que seja possível extrair uma percepção significativa (insight) da informação apresentada e se o conteúdo constitui ao menos uma frase completa."
            prompt_utilidades += f"\n{prompt}"

prompt_utilidades += "\nRetorne o resultado como uma lista em Python, por exemplo: ['SIM'] ou ['NÃO']."
#print(prompt_utilidades)
resposta_gpt_utilidade = ['SIM', 'SIM', 'NÃO', 'SIM', 'NÃO', 'NÃO', 'NÃO', 'NÃO', 'NÃO', 'NÃO', 'NÃO']


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
    "titulo": "As Fases do Plano SP",
    "publico_alvo": "População do estado de São Paulo, especialmente gestores municipais e cidadãos interessados nas diretrizes de reabertura econômica durante a pandemia de Covid-19.",
    "objetivo": "Informar sobre o funcionamento do Plano São Paulo, incluindo como são determinadas as fases de reabertura da economia e os critérios utilizados para essa definição.",
    "analise_detalhada": "O texto apresenta uma explicação sobre as fases do Plano SP, um programa criado pelo Governo do Estado de São Paulo durante a pandemia de Covid-19 para permitir uma reabertura econômica gradual e baseada em dados de saúde pública. A utilidade do conteúdo está na sua aplicação prática: cada região do estado foi dividida em 22 regiões de saúde, e a progressão ou regressão entre as fases depende de indicadores como número de casos, internações e óbitos por Covid-19, além da capacidade hospitalar. Essas informações ajudam a população e autoridades locais a entenderem porque determinadas medidas estão sendo aplicadas. Apesar de apresentar falhas de digitação e estrutura, é possível extrair um insight relevante: a descentralização da gestão da pandemia por meio de critérios técnicos e regionais. O texto reforça que as decisões são baseadas em monitoramento diário.",
    "texto_corrigido": "AS FASES DO PLANO SP — Entenda quais são e como são calculadas as etapas para a retomada consciente e segura da economia no estado. O estado foi dividido em 22 regiões. Cidades devem seguir os protocolos estabelecidos de acordo com a fase em que a região está. Franca, Ribeirão Preto, São José do Rio Preto, Araraquara, São Carlos, Araçatuba, São João da Boa Vista, Piracicaba, Presidente Prudente, Campinas, Marília, Taubaté, Sub-região Leste RMSP, Bauru, Sub-região Norte RMSP, Sub-região Sudeste RMSP, Sorocaba, Município de São Paulo, Sub-região Sudoeste RMSP, Registro, Sub-região Oeste RMSP, Baixada Santista. Fases são calculadas de acordo com a capacidade do sistema de saúde. Uma região só avança de fase se registra evolução nos indicadores (número de casos, internações, óbitos), acompanhada diariamente pelo Governo. Se houver piora, a região volta para a fase anterior.",
    "original": "AS FASES DO PLANO SP Entenda quais são e como são calculadas as etapas para retomada consciente e segura da economia no estado ESTADO FOI DIVIDIDO EM 22 REGIÕES Cidades devem seguir os protocolos estabelecidos de acordo com a fase que a região está Franca VIII  Bauetos Rlbelrão Preto XIII } São José do Rlo Preto Ararquara Sho Carlos _ I Aracatuba Sáo João da Boa Vlsta Piracicaba Presldente Prudente Camplnas  vII Marflla Iaubaté xvI Sub-reRião Leste RMSP Bauru Sub-reglão Norte RMSP Sub rsgifo Sudeste RMSP Sorocaba Munlcipio de Sao Paule Sub-repino Sudoeste RMSP xII_ Reglstro Sub-região Oeste RMSP Balxada Santista Fases são calculadas A situação das Uma região Se houver piora, de acordo com regiões só avança de fase região volta capacidade do sistema acompanhada se registra para fase anterior de saúde evolução diariamente melhora do nª de casos, pelo Governo dos indicadores internaçoes óbitos"
  },
  {
    "titulo": "Infográfico - Características e Como Fazer",
    "publico_alvo": "Estudantes, educadores e profissionais de comunicação e design interessados em aprender sobre a criação de infográficos.",
    "objetivo": "Explicar de forma didática o que é um infográfico, suas funções, características e as etapas para produzi-lo.",
    "analise_detalhada": "Este texto traz orientações práticas e conceituais sobre infográficos, que são ferramentas de comunicação visual amplamente utilizadas para sintetizar e transmitir informações de forma atrativa. A função central é informar, atrair o público-alvo e garantir clareza e precisão na mensagem. A presença de elementos verbais e não verbais bem organizados em torno de um único tema é destacada como essencial. O texto também lista ferramentas comuns para a produção (como Canva e PowerPoint) e reforça a importância de revisão. Apesar de erros de digitação e estrutura, o conteúdo fornece insights claros sobre o processo criativo de um infográfico e seus critérios de eficácia.",
    "texto_corrigido": "Funções: Transmitir informações, ser atrativo ao público-alvo, ser claro e preciso. Infográfico - Características: texto + elementos visuais. Linguagem verbal e não verbal. Informações bem organizadas e/ou localizadas. Único tema. Como fazer: escolha o tema, defina o visual e o texto da mensagem. Utilize ferramentas (Canva, Word, PowerPoint etc.). Revise o texto e a parte visual.",
    "original": "Funções: Transmitir informaçoes Ser atrativo a0 público-alvo Ser claro preciso Infográfico Caracteristicas: (texto elementos visuais) Linguagem verbal não verbal Informações bem organizadas elou lopicallzadas Único tema Como fazer: Escolha tema Defina visual texto da mensagem Utilize ferramentas (Canvas, Word, PowerPoint etc ) Revise texto parte"
  },
  {
    "titulo": "Cuidados Dentro de Casa - Covid-19",
    "publico_alvo": "População em geral, especialmente grupos de risco e pessoas com casos confirmados ou suspeitos de Covid-19.",
    "objetivo": "Orientar sobre medidas de prevenção e cuidados no ambiente doméstico durante o isolamento social por causa da Covid-19.",
    "analise_detalhada": "Este texto é altamente informativo e útil, especialmente durante períodos de alta transmissão da Covid-19. Fornece instruções sobre quem deve permanecer em casa (idosos, pessoas com sintomas gripais, casos confirmados), reforçando a necessidade de isolamento e precauções no ambiente doméstico. O texto também destaca ações práticas, como uso de quarto individual ventilado, não compartilhamento de itens de higiene, distanciamento mínimo de 1 metro e manutenção do ambiente arejado. O insight importante é que o controle da pandemia também depende de medidas adotadas dentro do lar. Apesar de conter erros ortográficos e de formatação, é possível compreender claramente a intenção e a importância do conteúdo.",
    "texto_corrigido": "#CORONAVÍRUS — CUIDADOS DENTRO DE CASA. A recomendação de isolamento social é essencial para conter a circulação do vírus e a propagação de casos de Covid-19. QUEM DEVE FICAR EM CASA: Pessoas com 60 anos ou mais (grupo mais vulnerável), pacientes com confirmação de Covid-19 (devem ficar em casa por 14 dias), pessoas com sintomas de gripe ou resfriado (devem ficar em casa até desaparecerem os sintomas). Procure um posto de saúde se houver piora (dificuldade para respirar e cansaço). RECOMENDAÇÕES EM CASA: Permaneça em casa até desaparecerem os sintomas por completo. De preferência, fique em quarto individual bem ventilado. Evite compartilhar objetos de higiene pessoal e talheres. Não receba visitas. Mantenha distância de pelo menos 1 metro e mantenha o ambiente ventilado.",
    "original": "#CORONAVÍRUS CUIDADOS DENTRO DE CASA Recomendação de Isolamento soclal é essenclal para conter circulação do vÍrus e a propagação de casos de Covid-19 QUEM DEVE FICAR EM CASA 60+ Pessoas Paciente com Pessoas com sintomas acima de 60 anos confirmação de gripe ou resfriado (grupo mais de Covid-19 (devem ficar em casa vulneravel (devem (lcar em casa por 14 dlas) doença) até desaparecerem Procure UM fosto 05 sintomas) De Saude Se HOUVER PIORA (DiFIcULDADE PARA respirar € CANSAÇO) RECOMENDAÇÕES EM CASA Permaneça em casa De preferência; fique Evite compartilhar até desaparecerem os em quarto individual objetos de higiene sintomas por completo bem ventilado pessoal talheres 1 MEIRO Não receba Manter distância de Mantenha visitas pelo menos metro ambiente da pessoa infectada ventilado"
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
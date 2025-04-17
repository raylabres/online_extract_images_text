import requests
from bs4 import BeautifulSoup
import re

def extract_text_from_infographic(url):
    
    # Possíveis tags e classes
    possible_tags = ['div', 'section', 'article', 'figure', 'img']
    
    possible_classes = ['infografico', 'info-grafico', 'grafico', 'visualizacao-de-dados', 
                        'grafico-de-dados', 'visual', 'estatisticas', 'grafico-estatistico',
                        'infographic', 'info-graphic', 'graphic', 'data-visualization', 
                        'chart', 'visual', 'stats', 'data-chart', 'visualization', 'viz']
    
    possible_alts = ['infografico', 'infographic', 'grafico', 'chart', 'visualizacao', 'visualization']

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())
    for tag in possible_tags:
        infographic_classes = soup.find(tag, class_=lambda class_: class_ in possible_classes)
        
        if infographic_classes:
            print("Infográfico Classes encontrado")
        
        infographic_alt = soup.find(tag, alt=lambda alt: alt and any(keyword in alt.lower() for keyword in possible_alts))
        print(infographic_alt)
        if infographic_alt:
            print("Infográfico alt encontrado")
        
        # else:
        #     return "Infográfico não encontrado"

# Exemplo de uso
url = "https://www.gov.br/pt-br/noticias/financas-impostos-e-gestao-publica/2021/03/cerca-de-70-milhoes-de-pessoas-acessaram-o-portal-do-governo-federal-em-fevereiro/WhatsAppImage20210323at09.29.30.jpeg/view"
text = extract_text_from_infographic(url)
print(text)
# Online Extract Images Text

## 📋 Descrição do Projeto
Este projeto de Iniciação Científica Online Extract Images Text, automatiza o fluxo completo de captura, conversão, tratamento e extração de texto de imagens presentes em páginas web utilizando técnicas de web scraping e OCR (Reconhecimento Óptico de Caracteres).

## ⚙️ Funcionalidades

- **Download de imagens**: Captura todas as imagens de uma página web (exceto logos) e organiza em pasta dedicada.
- **Conversão de formatos**: Converte arquivos suportados pelo Pillow para PNG e SVG para PNG usando CairoSVG.
- **Tratamento de imagens**: Ajusta contraste das imagens convertidas para melhorar a legibilidade.
- **Reconhecimento de texto (OCR)**: Aplica EasyOCR para extrair texto de cada imagem tratada e salva o resultado em arquivos `.txt`.
- **Limpeza e saneamento**: Remove automaticamente arquivos antigos e imagens sem texto detectado.
- **Geração de documentos**: Organiza os resultados extraídos no diretório de resultados para análise posterior.

## 📂 Estrutura de Diretórios

```
├── 1_imagens_baixadas/      # Armazena as imagens originais baixadas
├── 2_imagens_convertidas/   # Imagens convertidas para PNG
├── 3_imagens_tratadas/      # Imagens com contraste aumentado
├── 4_resultados_ocr/        # Arquivos de texto gerados pelo OCR
├── 5_resultados_saneados/   # (Opcional) Resultados pós-saneamento
├── 6_documentos_gerados/    # Relatórios e documentos finais
├── app.py                   # Código-fonte principal
└── README.md                # Este arquivo
```  

## 🚀 Tecnologias e Bibliotecas

- **Python 3.8+**
- **Requests**: captura de conteúdo HTML e imagens via HTTP.
- **BeautifulSoup4**: parsing de HTML para localizar tags `<img>`.
- **Pillow (PIL)**: abertura e conversão de imagens.
- **CairoSVG**: conversão de SVG para PNG.
- **EasyOCR**: extração de texto de imagens.
- **Pytesseract** (opcional): alternativa para OCR.
- **OS** e **Urllib**: manipulação de arquivos e URLs.

## 🔧 Requisitos de Instalação

1. Clone este repositório:
   ```bash
   git clone https://seu-repositorio.git
   cd seu-repositorio
   ```
2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate   # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. (Opcional) Configure o Tesseract se for usar `pytesseract`:
   - [Instalação do Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## ▶️ Como Executar

No diretório raiz do projeto, execute:
```bash
python app.py
```
O script irá:
1. Limpar pastas antigas.
2. Baixar todas as imagens da URL configurada em `site`.
3. Filtrar e remover arquivos não suportados.
4. Converter e tratar imagens.
5. Aplicar OCR nas imagens tratadas.
6. Gerar arquivos de texto em `4_resultados_ocr/`.

## 🔄 Personalização
- **URL alvo**: altere a variável `site` no topo do `app.py`.
- **Ajuste de contraste**: modifique `fator_contraste` em `treat_image()`.
- **Idiomas OCR**: configure `easyocr.Reader(['pt', 'en'])` conforme necessidade.

## 🤝 Contribuição
Pull requests são bem-vindos! Para modificar ou estender funcionalidades:
1. Fork deste repositório.
2. Crie uma branch feature: `git checkout -b feature/nome-feature`
3. Commit suas alterações: `git commit -m "feat: descrição da feature"`
4. Envie para o repositório remoto: `git push origin feature/nome-feature`
5. Abra um Pull Request.

## 📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

> Desenvolvido com foco em pesquisa para Iniciação Científica Ceunsp.

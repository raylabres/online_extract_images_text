from transformers import pipeline

# Especificando o modelo e tokenizador corretos
summarizer = pipeline("summarization", model="google/pegasus-large", tokenizer="google/pegasus-large")

# Texto de exemplo
texto = "Python é uma linguagem de programação de alto nível, amplamente usada para desenvolvimento web, automação, análise de dados e aprendizado de máquina."

# Resumindo o texto
resultado = summarizer(texto, max_length=50, min_length=25, do_sample=False)
print("\nResumo do Texto:", resultado[0]['summary_text'])
